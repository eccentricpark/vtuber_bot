import asyncio
import websockets
import json
# from src.config.websocket_service import WebsocketService
# from src.config.libaray_config import get_websocket_url

from config.websocket_service import WebsocketService
from config.libaray_config import get_websocket_url

hello_keywords = ['안녕', '반가워', '반갑다', '하이', 'ㅎㅇ', 'hi', 'hello']
happy_keywords = ['기뻐', '너무 기쁘다', '행복해', '행복하다', '행복']
shy_keywords = ['사랑', '사랑해']

# api 상태 확인
api_state_request = {
    "apiName": "VTubeStudioPublicAPI",
    "apiVersion": "1.0",
    "requestID": "requestMyState",
    "messageType": "APIStateRequest"
}

# 토큰 생성
token_create_request = {
    "apiName": "VTubeStudioPublicAPI",
    "apiVersion": "1.0",
    "requestID": "Authentication_MAO_01",
    "messageType": "AuthenticationTokenRequest",
    "data": {
            "pluginName": "MAO_Plugin",
            "pluginDeveloper": "Mind_of_MAO",
            "pluginIcon": ""
    }
}

# 토큰 인증 유무 검사
token_authentication_check = {
    "apiName": "VTubeStudioPublicAPI",
    "apiVersion": "1.0",
    "requestID": "Authentication_MAO_02",
    "messageType": "AuthenticationRequest",
    "data": {
            "pluginName": "MAO_Plugin",
            "pluginDeveloper": "Mind_of_MAO",
            "authenticationToken": "token"
    }
}

# 현재 표시된 모델 정보 불러오기
model_load_request = {
    "apiName": "VTubeStudioPublicAPI",
    "apiVersion": "1.0",
    "requestID": "Load_Model_MAO",
    "messageType": "CurrentModelRequest"
}

# 모델의 핫키 정보 불러오기
model_hotkey_list_request = {
    "apiName": "VTubeStudioPublicAPI",
    "apiVersion": "1.0",
    "requestsID": "Hotkeys_List_MAO_02",
    "messageType": "HotkeysInCurrentModelRequest",
    "data": {
            "modelID": ""
    }
}

model_hotkey_execute_request = {
    "apiName": "VTubeStudioPublicAPI",
    "apiVersion": "1.0",
    "requestID": "MAO_Test",
    "messageType": "HotkeyTriggerRequest",
    "data": {
            "hotkeyID": "43a739238c1e4d04917f23ff0d75c607",
            "itemInstanceID": ""
    }
}

url = get_websocket_url()

async def execute_websocket():
    websocket_service = WebsocketService()
    async with websockets.connect(url) as websocket:
        authentication_token = await websocket_service.get_authentication_token(token_create_request, websocket)
        modified_token_authentication = websocket_service.modify_authentication_token(token_authentication_check, authentication_token)
        token_check_response = await websocket_service.get_json_by_response(json.loads(modified_token_authentication), websocket)
        print(token_check_response)

        api_state_check_response = await websocket_service.get_json_by_response(api_state_request, websocket)
        print(api_state_check_response)

        model_id = await websocket_service.get_model_id(model_load_request, websocket)
        modified_model_hotkey_list_request = websocket_service.modify_model_id(model_hotkey_list_request, model_id)
        action_list = await websocket_service.get_json_by_response(json.loads(modified_model_hotkey_list_request), websocket)
        print(action_list)

        action = await websocket_service.get_json_by_response(model_hotkey_execute_request, websocket)
        print(action)

tasks = [ asyncio.ensure_future(execute_websocket()) ]

asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))