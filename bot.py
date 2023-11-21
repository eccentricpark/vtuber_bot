from twitchio.ext import commands
import datetime
import asyncio
import time
import json

from src.config.twitch_config import get_twitch_access_token
from src.config.read_json import read_json_file, write_json
from src.openai_service.open_ai import get_ai_response, get_announce_ai_response
from src.azure_service.text_to_speech import TextToSpeech
from src.websocket.controller import act_rigging, act_roll_back, act_kalimba

from src.play_instrument import play_sound

import warnings
warnings.filterwarnings('ignore')
    
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=get_twitch_access_token(), prefix='', initial_channels=['enqlqkr'])
        self.messages = read_json_file('./mao11_07_V4.json')
        self.last_request_time = datetime.datetime.now()
        self.text_to_speech = TextToSpeech()
        self.is_speak = False
        self.is_announce = False
        print("성공적으로 받아왔습니다.")

    async def event_ready(self):
        print(f'Ready | {self.nick}')


    async def event_message(self, message):
        user_content = message.content
        if user_content == "!발표모드":
            self.is_announce = True
        elif user_content == "!발표모드해제":
            self.is_announce = False

        if(self.is_announce):
            await self.execute_announce_mode(user_content)
        else:
            await self.execute_normal_mode(user_content)
        
    # 일반 자유 대화 모드
    async def execute_normal_mode(self, message):
        if self.is_speak:
            return
        user_content = message
        print(f"user : {user_content}")
        
        # 메시지를 컨텍스트에 추가
        # GPT 입력 형식을 맞추기 위한 용도
        self.messages.append({"role": "user", "content": user_content})  
        self.is_speak = True
    
        # 악기 연주 프롬프트가 들어 오면 실행
        if(self.check_listen_instrument(user_content)):
            assistant_content = "아직 이것 밖에 할 줄 모르지만, 이 곡이라도 연주해볼게."
            print(f"MAO : {assistant_content}")

            await self.gpt_response(assistant_content)
            await act_kalimba()
            play_sound(f"musics/달빛에그려지는.WAV")
        else:
            # GPT 답변 생성
            assistant_content = get_ai_response(self.messages)
            print(f"MAO : {assistant_content}")
            await self.gpt_response(assistant_content)
            await act_roll_back()

        write_json(user_content, assistant_content)  

    # 발표 모드
    async def execute_announce_mode(self, message):
        if self.is_speak:
            return
        user_content = message
        print(f"user : {user_content}")
        
        # 메시지를 컨텍스트에 추가
        # GPT 입력 형식을 맞추기 위한 용도
        self.messages.append({"role": "user", "content": user_content})  
        self.is_speak = True
    
        # GPT 답변 생성
        assistant_content = get_announce_ai_response(self.messages)
        print(f"MAO : {assistant_content}")
        await self.gpt_response(assistant_content)
        await act_roll_back()

        write_json(user_content, assistant_content)  
        
    def check_listen_instrument(self, user_content):
        want_listen = ["악기 연주 해줘", "악기연주 해줘", "악기연주해줘", "악기연주 해 줘", "악기 연주 해 줘"]
        # 조건에 따라 변수 값 변경
        return user_content in want_listen
            
    async def gpt_response(self, assistant_content):
        # pitch : 음의 높낮이
        # rate : 빠르기
        tts_task = asyncio.create_task(self.text_to_speech.speak(assistant_content, pitch='+15%', rate="+25%"))
        await act_rigging(assistant_content)
        await tts_task  # TTS 출력을 기다림
        self.is_speak = False
        
        # 이게 있어야 GPT 답변을 토대로 기억함.
        self.messages.append({"role": "assistant", "content": assistant_content})