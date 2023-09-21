from twitchio.ext import commands
import datetime
import json
import random
import openai
import asyncio
import os
from speech_to_text import SpeechToText
from text_to_speech import TextToSpeech
from chat_filter import ChatFilter
from xml.sax.saxutils import escape
from dotenv import load_dotenv
load_dotenv(verbose=True)

import warnings
warnings.filterwarnings('ignore')

openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

twitch_access_token = os.getenv("TWITCH_ACCESS_TOKEN")


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=twitch_access_token, prefix='', initial_channels=['kirisakirai'])
        self.messages = [{"role": "system", "content": "당신은 사람입니다.연인과 대화하듯이 대화하세요."}]
        # self.messages = [{"role": "system", "content": "당신은 예수님입니다. 사람들에게 가르침을 전파하듯이 대화하세요."}]
        self.last_request_time = datetime.datetime.now()
        self.speech_to_text = SpeechToText(self)
        self.text_to_speech = TextToSpeech()
        self.chat_filter = ChatFilter()
        self.is_stt_active = False
        print("성공적으로 받아왔습니다.")


    async def event_ready(self):
        print(f'Ready | {self.nick}')


    async def event_message(self, message):

        if message.echo or self.is_stt_active:
            return

        user_content = message.content.lower()
        filtered_user_content = await self.filter(user_content)

        # 시간차? 시간차가 왜 있지
        current_time = datetime.datetime.now()
        time_diff = current_time - self.last_request_time
        if time_diff.total_seconds() < random.randint(5, 10):
            return

        self.messages.append({"role": "user", "content": filtered_user_content})  # 사용자 메시지를 컨텍스트에 추가

        # GPT 답변 생성
        assistant_content = await self.generate_chat_completion(filtered_user_content)
        assistant_content = self.chat_filter.filter_sensitive_words(assistant_content)

        self.last_request_time = datetime.datetime.now()
        response_data = {"prompt": filtered_user_content, "completion": assistant_content}
        self.write_chat_data(response_data)

        print(f"GPT: {assistant_content}")

        escaped_content = escape(assistant_content)
        tts_task = asyncio.create_task(self.text_to_speech.speak(escaped_content, pitch='+15%', rate="+20%"))

        await tts_task  # TTS 출력을 기다림

        self.messages.append({"role": "assistant", "content": assistant_content})


    def is_too_long(self, user_content):
        return len(user_content) > 100
    

    def is_too_short(self, user_content):
        return len(user_content) == 1

    # 사용자 채팅 내역 저장
    def write_chat_data(self, response_data):
        with open('gpt_responses.jsonl', 'a', encoding='utf-8') as f:
            f.write(json.dumps(response_data, ensure_ascii=False) + '\n')


    # 혐오표현이나 문장이 너무 길거나 짧으면 필터링처리
    async def filter(self, user_content):
        filtered_user_content = self.chat_filter.filter_sensitive_words(user_content)

        if filtered_user_content == "필터링":
            await self.text_to_speech.speak("필터링", pitch='+15%', rate="+20%")
            return  # 컨텍스트에 메시지를 추가하지 않고 반환
        
        # 토큰이 너무 길거나 짧으면 무시해버리기
        if (self.is_too_long(filtered_user_content) or self.is_too_short(filtered_user_content)):
            filtered_user_content = ''
            return

        return filtered_user_content

    async def generate_chat_completion(self, prompt, model="vtuber_test", temperature=1, max_tokens=200):
        current_messages = self.messages

        # 컨텍스트 메시지 출력
        print("Current messages (context):")
        for message in current_messages:
            print(f"Role: {message['role']} - Content: {message['content']}")

        response = openai.ChatCompletion.create(
            engine=model,
            messages=current_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        if response['choices'][0].get('finish_reason') == 'content_filter':
            print("Content filtered by OpenAI.")
            assistant_content = "필터링"  # 필터링된 경우의 기본 응답
        else:
            assistant_content = response['choices'][0]['message']['content']

        return assistant_content