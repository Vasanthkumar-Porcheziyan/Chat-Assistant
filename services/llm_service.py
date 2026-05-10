import os
from openai import OpenAI

def generate_bot_response(messages, model, settings):
    """Generate bot response using selected model and settings"""
    client = OpenAI(
        base_url=os.getenv("NVIDIA_BASE_URL"),
        api_key=os.getenv("NVIDIA_API_KEY")
    )

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=settings["temperature"],
        top_p=settings["top_p"],
        max_tokens=settings["max_tokens"],
        stream=True
    )

    bot_response = ""
    for chunk in completion:
        if chunk.choices and chunk.choices[0].delta.content is not None:
            bot_response += chunk.choices[0].delta.content
    return bot_response
