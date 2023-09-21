from twitchio.ext import commands
import datetime
import json
import random
import openai
import asyncio
import os
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
        filtered_user_content = self.chat_filter.filter_sensitive_words(user_content)

        # 메시지를 컨텍스트에 추가
        self.messages.append({"role": "user", "content": filtered_user_content})  

        # 문장이 너무 길거나 짧으면 무시
        if self.is_ignore(filtered_user_content):
            print("GPT : 너무 짧아 무시됐습니다.")
            return

        # 혐오표현 필터링
        if self.is_filter(filtered_user_content):
            await self.text_to_speech.speak("필터링", pitch='+15%', rate="+20%")
            print("GPT: 필터링처리됐습니다.")
            return

        
        current_time = datetime.datetime.now()
        time_diff = current_time - self.last_request_time
        if time_diff.total_seconds() < random.randint(5, 10):
            return

        # GPT 답변 생성
        assistant_content = await self.generate_chat_completion(filtered_user_content)


        # 시간 최신화를 안 해주면 GPT가 임의로 대본을 생성해버린다.
        self.last_request_time = datetime.datetime.now()
        response_data = {"prompt": filtered_user_content, "completion": assistant_content}
        self.write_chat_data(response_data)

        print(f"GPT: {assistant_content}")

        # 일부 특수문자 처리
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

    # 필터링 처리
    def is_filter(self, content):
        return content == "필터링"
    
    # 문장이 너무 길거나 짧으면 무시
    def is_ignore(self, content):
        return self.is_too_long(content) or self.is_too_short(content)

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