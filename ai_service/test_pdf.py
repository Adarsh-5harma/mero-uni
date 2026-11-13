import sys
sys.path.append(".")

import pymupdf
import ollama
from schemas import ResourceMetadata

print("Reading PDF (Page 2)...")
try:
    doc = pymupdf.open("sample.pdf")
    
    # Read page 2 (index 1), because page 1 is the cover
    text = doc[1].get_text()[:1500] 
    
    if len(text) < 50:
        print("❌ Error: Page 2 has no text.")
        sys.exit(1)
        
    print(f"✅ Extracted {len(text)} characters.")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print("Sending to Local Ollama (Please wait 5-10 seconds)...")

try:
    response = ollama.chat(
        model='qwen3.5:4b',
        messages=[
            {
                'role': 'user', 
                'content': f'Extract metadata from this text: {text}'
            }
        ],
        format=ResourceMetadata.model_json_schema(),
        options={
            'num_predict': 300, 
            'temperature': 0.0, 
        },
        think=False 
    )
    
    print("\n✅ RAW AI OUTPUT:")
    print(response['message']['content'])
    
    # Validate with Pydantic
    metadata = ResourceMetadata.model_validate_json(response['message']['content'])
    print("\n✅ SUCCESS! Validated Data:")
    print(metadata.model_dump_json(indent=2))

except Exception as e:
    print("\n❌ FAILED:")
    print(e)