import requests
import json
import os
import time

PROMPT_TEMPLATES = {
    "few_shot": "Below are explanations of basic Python programs for beginners:\n\n"

                "### Example 1: Swapping Two Numbers\n"
                "**Concept**: Swap values of two variables without using a third variable.\n"
                "**Code**:\n"
                "```python\n"
                "a, b = 5, 10\n"
                "a, b = b, a\n"
                "print(a, b)  # Output: 10, 5\n"
                "```\n"
                "**Explanation**: This method swaps `a` and `b` using tuple unpacking.\n\n"

                "**Now, using the same format, explain the following Python programs:**\n{user_query}"
}


def create_payload(model, user_query, technique="few_shot", **kwargs):
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

    print("\n---- Few-Shot Prompt ----")
    payload_few = create_payload(model="mistral:latest", user_query=MESSAGE, technique="few_shot", temperature=0.7, max_tokens=600)
    time_taken, response_few = model_req(payload=payload_few)
    print(response_few)
    print(f'Time taken: {time_taken}s\n')
