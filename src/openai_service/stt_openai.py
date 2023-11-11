# create 2023-11-11 dohyeon kwon(playdev7@gmail.com)

from openai import OpenAI
import speech_recognition as sr
from openai_config import get_openai_object

# API KEY LOAD
get_openai_object()

Recognizer = sr.Recognizer()
mic = sr.Microphone()
client = OpenAI()
print("audio ready")

while True:
  with mic as source:
      audio = Recognizer.listen(source, timeout=2).get_wav_data()

  with open("temp.wav", "wb") as f:
      f.write(audio)

  audio_file = open("temp.wav", "rb")

  transcript = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file, 
    response_format="text"
  )

  print(transcript)