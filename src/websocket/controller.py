import asyncio
import json
from websockets import connect
import random

# 토큰 인증 유무 검사
token_authentication_check = {
    "apiName": "VTubeStudioPublicAPI",
    "apiVersion": "1.0",
    "requestID": "Authentication_MAO_02",
    "messageType": "AuthenticationRequest",
    "data": {
            "pluginName": "MAO_Plugin",
            "pluginDeveloper": "Mind_of_MAO",
            "authenticationToken": "e5cb1643a0c4810a5fe8125d9396824a87802f982eb4e17ace856680bc2ad8b1"
    }
}

# 현재 표시된 모델 정보 불러오기
model_load_request = {
    "apiName": "VTubeStudioPublicAPI",
    "apiVersion": "1.0",
    "requestID": "Load_Model_MAO",
    "messageType": "CurrentModelRequest"
}


model_hotkey_list_request = {
    "apiName": "VTubeStudioPublicAPI",
    "apiVersion": "1.0",
    "requestsID": "Hotkeys_List_MAO_02",
    "messageType": "HotkeysInCurrentModelRequest",
    "data": {
            "modelID": "d459a40b36624849ab5cd607849d4675"
    }
}


model_hotkey_execute_request = [
    {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "MAO_Test",
        "messageType": "HotkeyTriggerRequest",
        "data": {
                "hotkeyID": "9ef1915d7ad140919a00336b6b2e7a0e",
                "itemInstanceID": ""
        }
    },
    {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "MAO_Test",
        "messageType": "HotkeyTriggerRequest",
        "data": {
                "hotkeyID": "e717a12197ef41d5bf479d5ca65e64b8",
                "itemInstanceID": ""
        }
    },
    {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "MAO_Test",
        "messageType": "HotkeyTriggerRequest",
        "data": {
                "hotkeyID": "2ae5103dac9949318bf33f5a4c27b167",
                "itemInstanceID": ""
        }
    },
    {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "MAO_Test",
        "messageType": "HotkeyTriggerRequest",
        "data": {
                "hotkeyID": "6e74b7378f0045e29ed13b5f5d200751",
                "itemInstanceID": ""
        }
    },
    {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "MAO_Test",
        "messageType": "HotkeyTriggerRequest",
        "data": {
                "hotkeyID": "2022f6b365be44eab85f6343f1006401",
                "itemInstanceID": ""
        }
    },
    {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "MAO_Test",
        "messageType": "HotkeyTriggerRequest",
        "data": {
                "hotkeyID": "43a739238c1e4d04917f23ff0d75c607",
                "itemInstanceID": ""
        }
    }
]

async def get_rigging():
    # VTube Studio API 웹소켓 서버의 URI
    ws_uri = 'ws://localhost:8001'
    async with connect(ws_uri) as websocket:
        await websocket.send(json.dumps(token_authentication_check))
        response = await websocket.recv()

        await websocket.send(json.dumps(model_load_request))
        response = await websocket.recv()

        await websocket.send(json.dumps(model_hotkey_list_request))
        response = await websocket.recv()

        index = get_index_random(0, 5)
        await websocket.send(json.dumps(model_hotkey_execute_request[index]))
        response = await websocket.recv()
        print(response)
        # await authenticate_and_listen(ws_uri)


def get_index_random(min, max):
    """
    min : 최소 인덱스
    max : 최대 인덱스
    """
    return random.randint(min, max)