# pyautogui 라이브러리 설치
# pip install pyautogui

import pyautogui
import time
import numpy as np

# VTube Studio 창으로 이동 (창의 좌표는 시스템에 따라 다를 수 있습니다)


# 단축키를 시뮬레이션 (예: Ctrl + T)
# pyautogui.hotkey('N1')

hello_keywords = ['안녕', '반가워', '반갑다', '하이', 'ㅎㅇ', 'hi', 'hello']
happy_keywords = ['기뻐', '너무 기쁘다', '행복해', '행복하다', '행복']
shy_keywords = ['사랑', '사랑해']


# 키워드 포함 유무 확인
def is_contain_action(content, target):
  return target in content


# 상태값에 따라 키 코드 반환
def get_key_code(state_code):
  key_code = '0'

  if(state_code == 'ACTION_HELLO'):
    key_code = '3'

  elif(state_code == 'ACTION_HAPPY'):
    key_code = '2'

  elif(state_code == 'ACTION_SHY'):
    key_code = '4'

  return key_code


# 리깅 동작을 결정하는 키워드 유무 확인
# 반복문으로 리스트 순회
# 추후, 딕셔너리 하나로 순회하게끔 변경 예정
def get_state(content):
  for keyword in hello_keywords:
    if is_contain_action(content, keyword):
      return 'ACTION_HELLO'
    
  for keyword in happy_keywords:
    if is_contain_action(content, keyword):
      return 'ACTION_HAPPY'
    
  for keyword in shy_keywords:
    if is_contain_action(content, keyword):
      return 'ACTION_SHY'


# 키코드로 리깅 제어
def press(state_code):
  key_code = get_key_code(state_code)

  # 0은 입력 안함 (필요 없음)
  if(key_code == '0'):
    return
  
  pyautogui.moveTo(400, 500)
  pyautogui.click()
  
  pyautogui.keyDown(key_code)
  time.sleep(0.1)
  pyautogui.keyUp(key_code)
  # pyautogui.press(key_code)


def check_rigging(input):
  state_code = get_state(input)
  press(state_code)
