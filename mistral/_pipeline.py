import requests
import json
import os
import time

# Define different Prompt Engineering Templates for Requirement Analysis
PROMPT_TEMPLATES = {
    "structured": "You are an AI Requirement Analyst. Extract the following from the user input:\n"
                  "- Functional Requirements\n- Non-Functional Requirements\n- Constraints\n- User Goals\n\n"
                  "Input:\n{user_query}",

    "chain_of_thought": "Analyze the requirement step-by-step. Identify functional and non-functional requirements.\n\n"
                        "User Query:\n{user_query}",

    "role_based": "As a Software Architect, provide a detailed requirement analysis for the following request:\n{user_query}"
}

def load_config():
    """
    Load configuration from `_config.env` for Ollama.
    """
    config_locations = [
        "./_config.env",          
        "prompt-eng/_config.env", 
        "../_config.env"
    ]
    
    config_path = None
    for location in config_locations:
        if os.path.exists(location):
            config_path = location
            break
    
    if not config_path:
        raise FileNotFoundError("Configuration file '_config.env' not found.")

    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()


def create_payload(model, user_query, technique="structured", **kwargs):
    """
    Creates the request payload for Ollama.
    """
    if technique not in PROMPT_TEMPLATES:
        raise ValueError(f"Invalid technique: {technique}. Choose from {list(PROMPT_TEMPLATES.keys())}")

    prompt = PROMPT_TEMPLATES[technique].format(user_query=user_query)

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": kwargs  # Allow customization of parameters
    }

    return payload


def model_req(payload=None):
    """
    Sends a request to the Ollama API and retrieves the response.
    """
    try:
        load_config()
    except:
        return -1, "!!ERROR!! Problem loading configuration"

    url = os.getenv('URL_GENERATE', None)
    api_key = os.getenv('API_KEY', None)
    delta = None

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        start_time = time.time()
        response = requests.post(url, data=json.dumps(payload) if payload else None, headers=headers)
        delta = time.time() - start_time
    except Exception as e:
        return -1, f"!!ERROR!! Request failed: {str(e)}"

    if response is None:
        return -1, "!!ERROR!! No response received."
    elif response.status_code == 200:
        result = ""
        delta = round(delta, 3)

        response_json = response.json()
        if 'response' in response_json:
            result = response_json['response']
        else:
            result = response_json 
        
        return delta, result
    elif response.status_code == 401:
        return -1, "!!ERROR!! Authentication issue. Check API_KEY configuration."
    else:
        return -1, f"!!ERROR!! HTTP Response={response.status_code}, {response.text}"


def automated_prompt_refinement(user_query, model="llama3.2:latest"):
    """
    Implements automated refinement for requirement analysis using chained prompts.
    """
    initial_prompt = f"Extract high-level requirements from the following:\n{user_query}"
    
    payload1 = create_payload(model=model, user_query=initial_prompt, technique="structured")
    _, high_level_requirements = model_req(payload=payload1)
    
    refined_prompt = f"Based on the extracted high-level requirements, break them down into functional and non-functional requirements:\n{high_level_requirements}"
    
    payload2 = create_payload(model=model, user_query=refined_prompt, technique="chain_of_thought")
    _, detailed_requirements = model_req(payload=payload2)
    
    return detailed_requirements


### DEBUG: Running Ollama-based prompt engineering
if __name__ == "__main__":
    MESSAGE = "what is a ER diagram."

    print("---- Structured Prompt ----")
    payload_structured = create_payload(model="llama3.2:latest", user_query=MESSAGE, technique="structured", temperature=0.7, max_tokens=400)
    time_taken, response_structured = model_req(payload=payload_structured)
    print(response_structured)
    print(f'Time taken: {time_taken}s\n')

    print("---- Chain of Thought Prompt ----")
    payload_cot = create_payload(model="llama3.2:latest", user_query=MESSAGE, technique="chain_of_thought", temperature=0.5, max_tokens=500)
    time_taken, response_cot = model_req(payload=payload_cot)
    print(response_cot)
    print(f'Time taken: {time_taken}s\n')

    print("---- Role-Based Prompt ----")
    payload_role = create_payload(model="llama3.2:latest", user_query=MESSAGE, technique="role_based", temperature=0.3, max_tokens=600)
    time_taken, response_role = model_req(payload=payload_role)
    print(response_role)
    print(f'Time taken: {time_taken}s\n')

    print("---- Automated Prompt Refinement ----")
    refined_response = automated_prompt_refinement(MESSAGE)
    print(refined_response)
