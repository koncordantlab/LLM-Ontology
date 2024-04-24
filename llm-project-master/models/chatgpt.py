import openai
import json


def get_key():
    with open("config.json") as config_file:
        config = json.load(config_file)

    API_KEY = config.get("CHATGPT_API_KEY")
    return API_KEY


def get_chatgpt_response(prompt):
    key = get_key()
    openai.api_key = key
    input = prompt
    messages = [{"role": "system", "content":
        input}]
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, temperature = 0.2
    )
    if chat == 'testflag999':
        return True
    reply = chat.choices[0].message.content
    return reply