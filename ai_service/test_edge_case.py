import sys
sys.path.append(".")

import ollama
from schemas import ResourceMetadata

# A text with NO semester mentioned
text = """
This is a general guide to Python programming. 
It covers loops, functions, and basic data structures. 
No specific semester is mentioned here.
"""

print("Sending edge case to Local Ollama...")

try:
    response = ollama.chat(
        model='qwen3.5:4b',
        messages=[
            {'role': 'system', 'content': 'You are a JSON extraction bot. Output ONLY valid JSON.'},
            {'role': 'user', 'content': f'Extract metadata from this text: {text}'}
        ],
        format=ResourceMetadata.model_json_schema(),
        options={'num_predict': 500, 'temperature': 0.0},
        think=False
    )
    
    print("\n✅ RAW AI OUTPUT:")
    print(response['message']['content'])
    
    metadata = ResourceMetadata.model_validate_json(response['message']['content'])
    print("\n✅ VALIDATED SUCCESSFULLY!")

except Exception as e:
    print("\n❌ FAILED TO VALIDATE:")
    print(e)