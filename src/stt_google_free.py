# create 2023-11-11 dohyeon kwon(playdev7@gmail.com)

import speech_recognition as sr

Recognizer = sr.Recognizer()
mic = sr.Microphone()

def stt_google():
  print("audio ready")
  with mic as source:
      audio = Recognizer.listen(source, phrase_time_limit=15, timeout=4)
      # audio = Recognizer.listen(source)
      
  prompt = Recognizer.recognize_google(audio, language="ko-KR")
  return prompt