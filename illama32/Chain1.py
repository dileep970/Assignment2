import requests
import json
import os
import time

PROMPT_TEMPLATES = {
    "chain_of_thought": "Let's break down basic Python programming concepts step by step:\n\n"
                        "Step 1: Understand what swapping two numbers means.\n"
                        "Step 2: Learn how addition, subtraction, and multiplication work.\n"
                        "Step 3: Implement a function to check if a string is a palindrome.\n\n"
                        "Now explain these programs to a complete beginner:\n{user_query}"
}

def create_payload(model, user_query, technique="chain_of_thought", **kwargs):
    if technique not in PROMPT_TEMPLATES:
        raise ValueError(f"Invalid technique: {technique}. Choose from {list(PROMPT_TEMPLATES.keys())}")

    prompt = PROMPT_TEMPLATES[technique].format(user_query=user_query)

    return {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": kwargs
    }

def model_req(payload=None):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}

    start_time = time.time()
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    delta = round(time.time() - start_time, 3)

    return delta, response.json().get("response", "No response")

if __name__ == "__main__":
    MESSAGE = "Explain these Python programs step by step for beginners."

    print("\n---- Chain of Thought Prompt ----")
    payload_cot = create_payload(model="llama3.2:latest", user_query=MESSAGE, technique="chain_of_thought", temperature=0.6, max_tokens=600)
    time_taken, response_cot = model_req(payload=payload_cot)
    print(response_cot)
    print(f'Time taken: {time_taken}s\n')
