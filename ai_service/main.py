from vector_store import search_vector_store
from schemas import SearchQuery

import sys
import os
import shutil
sys.path.append(".")

from fastapi import FastAPI, UploadFile, File, HTTPException
import pymupdf
import ollama
from schemas import ResourceMetadata

app = FastAPI(title="MeroUni AI Service")

@app.get("/")
def health_check():
    return {"status": "AI Service is running"}

@app.post("/extract", response_model=ResourceMetadata)
async def extract_metadata(file: UploadFile = File(...)):
    # 1. Check if the file is a PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # 2. Save the uploaded file temporarily to disk
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 3. Read the PDF using PyMuPDF
        doc = pymupdf.open(temp_file_path)
        if len(doc) == 0:
            raise HTTPException(status_code=400, detail="PDF is empty.")

        # Get text from Page 1 and 2 (skip page 0 if it's a cover image, but let's just grab first 2)
        text = ""
        for page_num in range(min(2, len(doc))):
            text += doc[page_num].get_text()
        
        if len(text.strip()) < 50:
            raise HTTPException(status_code=400, detail="No readable text found. PDF might be a scanned image.")

        # 4. Send to Local Ollama
        response = ollama.chat(
            model='qwen3.5:4b',
            messages=[
                {
                    'role': 'user', 
                    'content': f'Extract metadata from this text: {text[:1500]}'
                }
            ],
            format=ResourceMetadata.model_json_schema(),
            options={
                'num_predict': 300, 
                'temperature': 0.0, 
            },
            think=False 
        )
        
        # 5. Validate the output with Pydantic
        metadata = ResourceMetadata.model_validate_json(response['message']['content'])
        
        return metadata

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Close the PyMuPDF document to release the Windows file lock
        try:
            doc.close()
        except:
            pass
        
        # Now it's safe to delete the temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/search")
async def search_documents(request: SearchQuery):
    """
    Receives a student's search query, finds the best chunks in ChromaDB, 
    and returns them.
    """
    print(f"🔍 Searching for: {request.query}")
    
    try:
        results = search_vector_store(request.query, n_results=3)
        
        # Format the response so it's easy for Django to read
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                "text": results['documents'][0][i],
                "page": results['metadatas'][0][i]['page'],
                "resource_id": results['metadatas'][0][i]['resource_id'],
                "distance": results['distances'][0][i] # Lower is better
            })
            
        return {"results": formatted_results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from pydantic import BaseModel

class IngestRequest(BaseModel):
    file_path: str
    resource_id: int

@app.post("/ingest")
async def ingest_document(request: IngestRequest):
    """
    Receives a file path and resource_id, and adds it to ChromaDB.
    """
    print(f"📥 Received ingest request for Resource ID: {request.resource_id}")
    
    try:
        # We import the function we wrote earlier
        from vector_store import ingest_pdf_to_vector_store
        
        ingest_pdf_to_vector_store(request.file_path, request.resource_id)
        return {"status": "success", "message": "Document ingested to vector store"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))