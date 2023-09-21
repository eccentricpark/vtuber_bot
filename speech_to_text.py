from google.cloud import speech
from google.oauth2 import service_account
import sys
from microphone_stream import MicrophoneStream, RATE, CHUNK
import asyncio
import re
from xml.sax.saxutils import escape

credentials = service_account.Credentials.from_service_account_file(
    "./google_credentials.json"
)


class SpeechToText:
    def __init__(self, bot):
        self.bot = bot
        self.stream = None
        self.language_code = "ko-KR"
        self.client = speech.SpeechClient(credentials=credentials)
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=self.language_code,
        )
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config, interim_results=True
        )

    async def start_stt(self):
        self.stream = MicrophoneStream(RATE, CHUNK)
        audio_generator = self.stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        with self.stream:
            responses = self.client.streaming_recognize(self.streaming_config, requests)
            await self.listen_print_loop(responses)

    def stop_stt(self):
        if self.stream is not None:
            self.stream.stop()
            self.stream = None

    async def listen_print_loop(self, responses):
        num_chars_printed = 0
        for response in responses:
            if not response.results:
                continue
            result = response.results[0]
            if not result.alternatives:
                continue
            transcript = result.alternatives[0].transcript
            overwrite_chars = " " * (num_chars_printed - len(transcript))

            if not result.is_final:
                sys.stdout.write(transcript + overwrite_chars + "\r")
                sys.stdout.flush()
                num_chars_printed = len(transcript)
            else:
                print(transcript + overwrite_chars)
                self.bot.messages.append({"role": "user", "content": transcript})
                assistant_content = await self.bot.generate_chat_completion(transcript)
                print(f"GPT: {assistant_content}")

                # TTS와 애니메이션을 동시에 실행
                escaped_content = escape(assistant_content)
                await self.bot.text_to_speech.speak(escaped_content, pitch='+15%', rate="+20%")

                self.bot.messages.append({"role": "assistant", "content": assistant_content})

                if re.search(r"\b(exit|quit)\b", transcript, re.I):
                    print("Exiting..")
                    break
                num_chars_printed = 0
