import asyncio
import json
import random
import os
from websockets import connect
from dotenv import load_dotenv
load_dotenv(verbose=True)

# 토큰 인증 유무 검사
token_authentication_check = {
    "apiName": "VTubeStudioPublicAPI",
    "apiVersion": "1.0",
    "requestID": "Authentication_MAO_02",
    "messageType": "AuthenticationRequest",
    "data": {
            "pluginName": "MAO_Plugin",
            "pluginDeveloper": "Mind_of_MAO",
            "authenticationToken": "5ca81c03741d4beccb4a5865877f04a7b896473f9fa00d5000c3a9a5b5353f68"
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
        "requestID": "normal_motion",
        "messageType": "HotkeyTriggerRequest",
        "data": {
                "hotkeyID": "9ef1915d7ad140919a00336b6b2e7a0e",
                "itemInstanceID": ""
        }
    },
    {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "talk1",
        "messageType": "HotkeyTriggerRequest",
        "data": {
                "hotkeyID": "e717a12197ef41d5bf479d5ca65e64b8",
                "itemInstanceID": ""
        }
    },
    {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "talk2",
        "messageType": "HotkeyTriggerRequest",
        "data": {
                "hotkeyID": "2ae5103dac9949318bf33f5a4c27b167",
                "itemInstanceID": ""
        }
    },
    {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "bad_motion",
        "messageType": "HotkeyTriggerRequest",
        "data": {
                "hotkeyID": "6e74b7378f0045e29ed13b5f5d200751",
                "itemInstanceID": ""
        }
    },
    {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "interest",
        "messageType": "HotkeyTriggerRequest",
        "data": {
                "hotkeyID": "2022f6b365be44eab85f6343f1006401",
                "itemInstanceID": ""
        }
    },
    {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "heart_magic",
        "messageType": "HotkeyTriggerRequest",
        "data": {
                "hotkeyID": "43a739238c1e4d04917f23ff0d75c607",
                "itemInstanceID": ""
        }
    },
    {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "heart_magic_failure",
        "messageType": "HotkeyTriggerRequest",
        "data": {
                "hotkeyID": "2ca71b056ee54ff7983f3b241a02b1e5",
                "itemInstanceID": ""
        }
    },
    {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "rabbit_horolololol",
        "messageType": "HotkeyTriggerRequest",
        "data": {
                "hotkeyID": "91b5b1d5dbc64a03aff2a1f154d70dbd",
                "itemInstanceID": ""
        }
    },
    {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "kalimba",
        "messageType": "HotkeyTriggerRequest",
        "data": {
                "hotkeyID": "81b8adf227c544c69720941b8da739fd",
                "itemInstanceID": ""
        }
    }
]
async def act_kalimba():
    # VTube Studio API 웹소켓 서버의 URI
    ws_uri = os.getenv('VTUBE_URI')
    async with connect(ws_uri) as websocket:
        await websocket.send(json.dumps(token_authentication_check))
        response = await websocket.recv()

        await websocket.send(json.dumps(model_load_request))
        response = await websocket.recv()
        
        await websocket.send(json.dumps(model_hotkey_list_request))
        response = await websocket.recv()

        await websocket.send(json.dumps(model_hotkey_execute_request[8]))
        response = await websocket.recv()

async def act_rigging(response_message):
    # VTube Studio API 웹소켓 서버의 URI
    ws_uri = os.getenv('VTUBE_URI')
    async with connect(ws_uri) as websocket:
        await websocket.send(json.dumps(token_authentication_check))
        response = await websocket.recv()

        await websocket.send(json.dumps(model_load_request))
        response = await websocket.recv()
        
        await websocket.send(json.dumps(model_hotkey_list_request))
        response = await websocket.recv()

        index = get_index(response_message)
        await websocket.send(json.dumps(model_hotkey_execute_request[index]))
        response = await websocket.recv()

async def act_roll_back():
    # VTube Studio API 웹소켓 서버의 URI
    ws_uri = os.getenv('VTUBE_URI')
    async with connect(ws_uri) as websocket:
        await websocket.send(json.dumps(token_authentication_check))
        response = await websocket.recv()

        await websocket.send(json.dumps(model_load_request))
        response = await websocket.recv()
        
        await websocket.send(json.dumps(model_hotkey_list_request))
        response = await websocket.recv()

        await websocket.send(json.dumps(model_hotkey_execute_request[0]))
        response = await websocket.recv()

def get_index(response_message):
    index = 0
    index = random.randint(1, 2)
    return index

# mao motion 메타데이터 가져오기
async def get_metadata():
    ws_uri = os.getenv('VTUBE_URI')
    async with connect(ws_uri) as websocket:
        await websocket.send(json.dumps(token_authentication_check))
        response = await websocket.recv()
        print(response)

        await websocket.send(json.dumps(model_load_request))
        response = await websocket.recv()
        print(response)

        await websocket.send(json.dumps(model_hotkey_list_request))
        response = json.loads(await websocket.recv())
        hotkeyList = response["data"]["availableHotkeys"]
        write_json(hotkeyList)

# json 파일로 저장하기
def write_json(response):
    # JSON 파일로 저장
    with open("mao_metadata.json", "w") as json_file:
        json.dump(response, json_file, indent=4)

# asyncio.run(get_metadata())