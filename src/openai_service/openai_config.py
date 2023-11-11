import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(verbose=True)

def get_openai_object():
    api_key = os.getenv("OPENAI_API_KEY")
    openai = OpenAI(api_key=api_key)
    return openai