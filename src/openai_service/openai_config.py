import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(verbose=True)

def get_openai_object():
    openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return openai