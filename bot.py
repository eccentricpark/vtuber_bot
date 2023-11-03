# https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models
# https://learn.microsoft.com/ko-kr/azure/machine-learning/how-to-create-component-pipelines-ui?view=azureml-api-2#register-component-in-your-workspace
# https://learn.microsoft.com/ko-kr/azure/ai-services/openai/quickstart?tabs=command-line&pivots=rest-api
from twitchio.ext import commands
import datetime
import asyncio
import os

from src.config.libaray_config import get_twitch_access_token
from src.chat_gpt import generate_chat_completion
from src.text_to_speech import TextToSpeech
from src.config.read_json import read_json_file

import warnings
warnings.filterwarnings('ignore')

mao = os.getenv("PROMPT_METADATA")

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=get_twitch_access_token(), prefix='', initial_channels=['enqlqkr'])
        self.messages = read_json_file('./mao3.json')
        self.last_request_time = datetime.datetime.now()
        self.text_to_speech = TextToSpeech()
        self.is_speak = False
        print("성공적으로 받아왔습니다.")

    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        if self.is_speak:
            return
        
        user_content = message.content.lower()
        print(f"user : {user_content}")
        # 메시지를 컨텍스트에 추가
        # GPT 입력 형식을 맞추기 위한 용도
        self.messages.append({"role": "user", "content": user_content})  
        self.is_speak = True
        
        # GPT 답변 생성
        assistant_content = await generate_chat_completion(prompt=self.messages, temperature=0.8)
        
        print(f"GPT: {assistant_content}")

        # pitch : 음의 높낮이
        # rate : 빠르기
        tts_task = asyncio.create_task(self.text_to_speech.speak(assistant_content, pitch='+15%', rate="+20%"))
        await tts_task  # TTS 출력을 기다림
        self.is_speak = False
        self.messages.append({"role": "assistant", "content": assistant_content})