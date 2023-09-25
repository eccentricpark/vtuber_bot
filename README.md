# AI 버튜버 테스트

방송 가능한 AI 유튜버 프로젝트입니다.
<br><br><br><br><br>

## 1. 설치
requirements.txt 내 파일 정보를 토대로 라이브러리들을 설치하세요.

```
pip install -r requirements.txt
```

만약 설치 중 오류가 나타날 경우, 

번거롭겠지만 requirements.txt에서 오류가 나는 부분을 지우고, 따로 설치해주세요.
<br><br><br><br><br>

## 2. .env는 직접 구성하세요.
모든 설정 정보는 .env 파일에 들어 가 있습니다.
때문에, 그냥 실행하면 오류가 발생합니다.

아래는 .env 파일의 예시입니다.

```
OPENAI_API_TYPE=YOUR_OPENAI_API_TYPE
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
OPENAI_API_VERSION=YOUR_OPENAI_API_VERSION
OPENAI_API_BASE=YOUR_OPENAI_API_BASE_URL

TWITCH_ACCESS_TOKEN=YOUR_TWITCH_ACCESS_TOKEN
TWITCH_GENERATE_ID=YOUR_TWITCH_GENERATE_ID
TWITCH_SECRET_ID=YOUR_TWITCH_SECRET_ID

TTS_AZURE_KEY=YOUR_TTS_KEY
TTS_AZURE_REGION=YOUR_TTS_REGION
```
<br><br><br><br><br>

## 3. Anaconda의 경우, 가상환경을 만들어 작업하세요.

Anaconda에서도 작업 가능합니다.

그러나 되도록이면 따로 가상환경을 만들어서 처리하세요.<br><br>

아래 명령어로 anaconda의 가상환경 목록을 볼 수 있습니다.

```
conda env list
```


만약, anaconda로 가상환경을 새로 만들고 싶다면 아래와 같이 입력하세요.

이 프로젝트는 오직 파이썬3.8 버전에서만 실행됩니다. 

(나머지 버전은 호환성 이슈가 발생합니다.)

```
conda create -n your_environment_name python=3.8
```