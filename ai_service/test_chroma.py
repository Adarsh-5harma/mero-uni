import sys
sys.path.append(".")

from vector_store import ingest_pdf_to_vector_store, search_vector_store

# 1. Ingest the PDF (using resource_id=99 for testing)
ingest_pdf_to_vector_store("sample.pdf", resource_id=99)

# 2. Search for something inside the book!
print("\n🔍 Searching for 'What is generative AI?'...")
results = search_vector_store("What is generative AI?", n_results=2)

print("\n--- SEARCH RESULTS ---")
for i, doc in enumerate(results['documents'][0]):
    print(f"\nResult {i+1} (Page {results['metadatas'][0][i]['page']}):")
    print(doc[:300] + "...") # Print first 300 chars