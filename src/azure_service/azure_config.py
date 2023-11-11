import os
import openai
from dotenv import load_dotenv
load_dotenv(verbose=True)

openai.api_type = os.getenv("AZURE_OPENAI_API_TYPE")
openai.api_base = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
openai.api_key = os.getenv("AZURE_OPENAI_API_BASE")

def get_tts_values():
  return (os.getenv('AZURE_TTS_KEY'), os.getenv("AZURE_TTS_REGION"))

def get_openai_object():
  return openai

def get_stt_values():
  return (os.getenv('AZURE_STT_SPEECH_KEY'), os.getenv('AZURE_STT_SPEECH_REGION'))