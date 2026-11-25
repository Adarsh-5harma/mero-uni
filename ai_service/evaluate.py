import sys
sys.path.append(".")

import time
import ollama
from schemas import ResourceMetadata

def run_evaluation(runs=5):
    print(f"--- Starting Evaluation: {runs} runs ---")
    
    text = """
    Course: CSIT 5th Semester
    Subject: Object Oriented Programming
    This lab manual covers how to create classes and objects in Python. 
    """

    success_count = 0
    total_time = 0

    for i in range(runs):
        start_time = time.time()
        print(f"Run {i+1} started...", end="", flush=True)
        
        try:
            # WE ARE ADDING think=False HERE
            response = ollama.chat(
                model='qwen3.5:4b',
                messages=[
                    {'role': 'system', 'content': 'You are a JSON extraction bot. Output ONLY valid JSON.'},
                    {'role': 'user', 'content': f'Extract metadata from this text: {text}'}
                ],
                format=ResourceMetadata.model_json_schema(),
                options={'num_predict': 500, 'temperature': 0.0},
                think=False # <--- THE MAGIC FIX
            )
            
            metadata = ResourceMetadata.model_validate_json(response['message']['content'])
            success_count += 1
            print(f" ✅ PASS", end="")
            
        except Exception as e:
            print(f" ❌ FAIL: {str(e)[:50]}", end="")
            
        end_time = time.time()
        elapsed = end_time - start_time
        total_time += elapsed
        
        print(f" ({elapsed:.2f}s)")

    print("\n--- EVALUATION RESULTS ---")
    print(f"Success Rate: {success_count}/{runs} ({(success_count/runs)*100:.1f}%)")
    print(f"Average Time: {total_time/runs:.2f} seconds per run")

if __name__ == "__main__":
    run_evaluation(runs=5)