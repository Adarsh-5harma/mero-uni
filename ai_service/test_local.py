import sys
import os
sys.path.append(".") # <-- This is the magic line

from openai import OpenAI
from schemas import ResourceMetadata

# Connect to your local Ollama instance
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama" 
)

MODEL = "qwen3.5:4b"

sample_text = """
Course: CSIT 5th Semester
Subject: Object Oriented Programming
This lab manual covers how to create classes and objects in Python. 
Students will learn about inheritance, polymorphism, and file handling.
"""

print("Sending to Local Ollama...")

try:
    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful data extraction assistant."},
            {"role": "user", "content": f"Extract metadata from this text: {sample_text}"}
        ],
        response_format=ResourceMetadata,
    )
    
    metadata = response.choices[0].message.parsed
    print("\n✅ SUCCESS! Validated Data:")
    print(metadata.model_dump_json(indent=2))

except Exception as e:
    print("\n❌ FAILED TO VALIDATE:")
    print(e)