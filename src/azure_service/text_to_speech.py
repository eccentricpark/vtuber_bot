import azure.cognitiveservices.speech as speechsdk
import asyncio
from src.azure_service.azure_config import get_tts_values

#Creates an instance of a speech config with specified subscription key and service region.
key, region = get_tts_values()

class TextToSpeech:
    def __init__(self):
        # 환경 변수에서 "SPEECH_KEY"와 "SPEECH_REGION"을 가져와서 SpeechConfig 객체를 생성합니다.
        self.speech_config = speechsdk.SpeechConfig(
            subscription=key,
            region=region
        )
        # 음성 합성에 사용할 언어와 목소리를 설정합니다.
        self.speech_config.speech_synthesis_voice_name = 'ko-KR-SoonBokNeural'  # 한국어 여성 목소리

        # 기본 스피커로 음성을 재생합니다.
        self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    async def speak(self, text, pitch='+15%', rate='+25%'):
        ssml = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='ko-KR'>
            <voice name='ko-KR-SoonBokNeural'>
                <prosody pitch='{pitch}' rate='{rate}'>{text}</prosody>
            </voice>
        </speak>
        """

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config,
                                                         audio_config=self.audio_config)

        speech_synthesis_result = await asyncio.get_event_loop().run_in_executor(None, lambda: speech_synthesizer.speak_ssml_async(ssml).get())

        if speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")
