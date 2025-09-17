import os 
from django.conf import settings

from openai import OpenAI

api_key = settings.OPENAI_API_KEY
# client = OpenAI(api_key=settings.OPENAI_API_KEY)

def ask_llm(prompt: str) -> str:
        
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-4",
        input=[
            {
                "role": "system",
                "content": "You are a travel assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_output_tokens=500,
        temperature=0.7,
    )
    return response.output_text