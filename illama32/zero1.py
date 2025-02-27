import requests
import json
import os
import time

PROMPT_TEMPLATES = {
    "zero_shot": "Explain the following basic Python programs to a beginner:\n\n"
                 "1. Swapping Two Numbers\n"
                 "2. Addition, Subtraction, and Multiplication\n"
                 "3. Checking if a String is a Palindrome\n\n"
                 "Provide detailed explanations for a first-time programmer along with example code.\n\n"
                 "{user_query}"
}

def create_payload(model, user_query, technique="zero_shot", **kwargs):
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

    print("\n---- Zero-Shot Prompt ----")
    payload_zero = create_payload(model="llama3.2:latest", user_query=MESSAGE, technique="zero_shot", temperature=0.7, max_tokens=500)
    time_taken, response_zero = model_req(payload=payload_zero)
    print(response_zero)
    print(f'Time taken: {time_taken}s\n')
