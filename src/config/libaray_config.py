import os
import openai
from dotenv import load_dotenv
load_dotenv(verbose=True)

openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_object():
  return openai