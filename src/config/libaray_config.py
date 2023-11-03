import os
import openai
from dotenv import load_dotenv
load_dotenv(verbose=True)

openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

twitch_access_token = os.getenv("TWITCH_ACCESS_TOKEN")

tts_azure_key = os.getenv('TTS_AZURE_KEY')
tts_azure_region = os.getenv("TTS_AZURE_REGION")
stt_speech_key = os.getenv('STT_SPEECH_KEY')
stt_speech_region = os.getenv('STT_SPEECH_REGION')

def get_tts_values():
  return (tts_azure_key, tts_azure_region)

def get_openai_object():
  return openai

def get_twitch_access_token():
  return twitch_access_token

def get_stt_values():
  return (stt_speech_key, stt_speech_region)