from llamaapi import LlamaAPI
import json

def get_key():
    with open("config.json") as config_file:
        config = json.load(config_file)

    API_KEY = config.get("LLAMA_API_KEY")
    return API_KEY

def get_llama_response(prompt):
    # Initialize the llamaapi with your api_token
    key = get_key()
    llama = LlamaAPI(key)
    input = prompt
    api_request_json = {
        "messages": [
            {"role": "user", "content": input},
        ],
        "stream": False,
        "temperature": 0.1
    }
    # Make your request and handle the response
    response = llama.run(api_request_json)
    if response == "testflag999":
        return True
    reply = response.json()["choices"][0]["message"]["content"]
    print("reply:\n\n")
    print(reply)
    return reply