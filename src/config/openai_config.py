import os
import openai
from dotenv import load_dotenv
load_dotenv(verbose=True)

def get_openai_object():
    openai.api_key = os.getenv("OPENAI_API_KEY_GPT4")
    return openai
