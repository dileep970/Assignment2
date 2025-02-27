import requests
import json
import os
import time

PROMPT_TEMPLATES = {
    "prompt_template": "Use this structured template for explaining basic Python programs to a beginner:\n\n"
                       "- **Title**: Understanding Basic Python Programs\n\n"
                       "- **Explanation**: Explain these fundamental concepts step by step:\n"
                       "  1. Swapping Two Numbers\n"
                       "  2. Addition, Subtraction, and Multiplication\n"
                       "  3. Checking if a String is a Palindrome\n\n"
                       "- **Example Code**:\n"
                       "  ```python\n"
                       "  # Swapping Two Numbers\n"
                       "  a, b = 5, 10\n"
                       "  a, b = b, a\n"
                       "  print(a, b)  # Output: 10, 5\n"
                       "\n"
                       "  # Addition, Subtraction, and Multiplication\n"
                       "  a, b = 4, 2\n"
                       "  print(a + b, a - b, a * b)  # Output: 6, 2, 8\n"
                       "\n"
                       "  # Palindrome Checking\n"
                       "  def is_palindrome(s):\n"
                       "      return s == s[::-1]\n"
                       "  print(is_palindrome('madam'))  # Output: True\n"
                       "  ```\n\n"
                       "- **Step-by-Step Execution**:\n"
                       "  - Explain each code snippet in detail.\n"
                       "  - Show variable assignments and changes in values.\n"
                       "  - Explain how slicing works in palindrome checking.\n\n"
                       "- **Expected Output**: \n"
                       "  - Demonstrate what will be printed when each code is executed.\n"
}

def create_payload(model, user_query, technique="prompt_template", **kwargs):
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

    print("\n---- Prompt Template ----")
    payload_template = create_payload(model="llama3.2:latest", user_query=MESSAGE, technique="prompt_template", temperature=0.5, max_tokens=600)
    time_taken, response_template = model_req(payload=payload_template)
    print(response_template)
    print(f'Time taken: {time_taken}s\n')
