import chromadb
import pymupdf

# Initialize ChromaDB (it will save data to the /chroma_db folder)
client = chromadb.PersistentClient(path="./chroma_db")

# We use the default embedding function (which uses a free, local model under the hood)
collection = client.get_or_create_collection(name="merouni_docs")

def ingest_pdf_to_vector_store(file_path: str, resource_id: int):
    """
    Reads a PDF, chunks it, and saves the chunks to ChromaDB.
    """
    print(f"📄 Ingesting {file_path} into Vector DB...")
    doc = pymupdf.open(file_path)
    
    chunks = []
    metadatas = []
    ids = []
    
    chunk_size = 500 # characters per chunk
    chunk_overlap = 50
    
    chunk_index = 0
    for page_num, page in enumerate(doc):
        text = page.get_text()
        if not text.strip():
            continue
            
        # Simple chunking logic
        for i in range(0, len(text), chunk_size - chunk_overlap):
            chunk = text[i:i + chunk_size]
            if len(chunk.strip()) > 20: # Ignore tiny chunks
                chunks.append(chunk)
                metadatas.append({
                    "resource_id": resource_id,
                    "page": page_num + 1
                })
                ids.append(f"res_{resource_id}_chunk_{chunk_index}")
                chunk_index += 1
                
    if chunks:
        collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        print(f"✅ Saved {len(chunks)} chunks to ChromaDB.")
    else:
        print("⚠️ No readable text found to chunk.")

def search_vector_store(query: str, n_results: int = 3):
    """
    Searches ChromaDB for the most relevant chunks.
    """
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results