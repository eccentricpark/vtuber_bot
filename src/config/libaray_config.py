import os
import openai
from dotenv import load_dotenv
load_dotenv(verbose=True)

openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_tts_values():
  return (os.getenv('TTS_AZURE_KEY'), os.getenv("TTS_AZURE_REGION"))

def get_openai_object():
  return openai

def get_twitch_access_token():
  return os.getenv("TWITCH_ACCESS_TOKEN")

def get_stt_values():
  return (os.getenv('STT_SPEECH_KEY'), os.getenv('STT_SPEECH_REGION'))

def get_websocket_url():
  return os.getenv("WEBSOCKET_URL")