import requests
import os
import time

def extract_pdf_metadata(file_path):
    """
    Sends a PDF file to the FastAPI AI microservice.
    Returns the extracted metadata JSON or None if it fails.
    """
    # The URL of your running FastAPI server
    FASTAPI_URL = "http://127.0.0.1:8000/extract"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None

    print(f"🚀 Sending {os.path.basename(file_path)} to AI Service...")
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'application/pdf')}
            
            # Send the file (timeout is set to 60 seconds because local AI is slow)
            response = requests.post(FASTAPI_URL, files=files, timeout=120)
            
        if response.status_code == 200:
            print("✅ AI Extraction successful!")
            return response.json()
        else:
            print(f"❌ AI Service Error {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Is the FastAPI server running on port 8000?")
        return None
    except requests.exceptions.Timeout:
        print("❌ Timeout: The AI took too long to process the PDF.")
        return None
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return None






def search_ai_service(query, n_results=3):
    """
    Sends a query to the FastAPI AI microservice to get semantic search results.
    """
    FASTAPI_URL = "http://127.0.0.1:8000/search"
    
    print(f"🔍 Asking AI Service for: {query}")
    
    try:
        response = requests.post(
            FASTAPI_URL, 
            json={"query": query}, 
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('results', [])
        else:
            print(f"❌ AI Search Error: {response.text}")
            return []
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Is FastAPI running?")
        return []
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return []