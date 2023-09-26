# https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models
# https://learn.microsoft.com/ko-kr/azure/machine-learning/how-to-create-component-pipelines-ui?view=azureml-api-2#register-component-in-your-workspace
# https://learn.microsoft.com/ko-kr/azure/ai-services/openai/quickstart?tabs=command-line&pivots=rest-api
from twitchio.ext import commands
import datetime
import json
import random
import asyncio

from src.config.libaray_config import get_twitch_access_token
from src.chat_gpt import generate_chat_completion
from src.text_to_speech import TextToSpeech
from src.chat_filter import ChatFilter
from src.rigging import check_rigging

from xml.sax.saxutils import escape


import warnings
warnings.filterwarnings('ignore')

class Bot(commands.Bot):
    def __init__(self):
        # super().__init__(token=twitch_access_token, prefix='', initial_channels=['kirisakirai'])
        super().__init__(token=get_twitch_access_token(), prefix='', initial_channels=['enqlqkr'])
        self.messages = [{"role": "system", "content": "당신은 사람입니다. 연인과 대화하듯이 대화하세요."}]
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

        if self.is_too_long(filtered_user_content) or self.is_too_short(filtered_user_content):
            print("GPT : 너무 짧아 무시됐습니다.")
            return

        # 혐오표현 필터링
        if self.filter_bad_word(filtered_user_content):
            await self.text_to_speech.speak("필터링", pitch='+15%', rate="+20%")
            print("GPT: 필터링처리됐습니다.")
            return

        
        current_time = datetime.datetime.now()
        time_diff = current_time - self.last_request_time
        if time_diff.total_seconds() < random.randint(5, 10):
            return

        # GPT 답변 생성
        assistant_content = await generate_chat_completion(prompt=self.messages)

        # 시간 최신화를 안 해주면 GPT가 임의로 대본을 생성해버린다.
        self.last_request_time = datetime.datetime.now()
        response_data = {"prompt": filtered_user_content, "completion": assistant_content}
        self.write_chat_data(response_data)

        print(f"GPT: {assistant_content}")

        # 일부 특수문자 처리
        escaped_content = escape(assistant_content)
        tts_task = asyncio.create_task(self.text_to_speech.speak(escaped_content, pitch='+15%', rate="+20%"))
        check_rigging(filtered_user_content)
        await tts_task  # TTS 출력을 기다림

        self.messages.append({"role": "assistant", "content": assistant_content})


    def is_too_long(self, user_content):
        return len(user_content) > 200
    
    def is_too_short(self, user_content):
        return len(user_content) == 1
    
    def filter_bad_word(self, content):
        return content == "필터링"

    # 사용자 채팅 내역 저장
    def write_chat_data(self, response_data):
        with open('gpt_responses.jsonl', 'a', encoding='utf-8') as f:
            f.write(json.dumps(response_data, ensure_ascii=False) + '\n')