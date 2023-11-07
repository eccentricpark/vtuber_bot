import json
from typing import Dict, List

class WebsocketService:
    def __init__ (self):
        pass
    """
    get_response는 딕셔너리에 요청 정보를 담아 응답 정보를 가져 온다.

    print_json은 json 형태로 전환하여 출력한다.
    깔끔한 구조로 출력되게 하기 위해 print_json 함수가 필요하다.

    그러나, 두 함수를 계속 호출하는 코드는 번거롭다.

    만약 print_json의 파라미터 개수나 타입을 변경해야 한다면 어떨까?
    호출하는 모든 곳을 변경해야 한다.

    때문에, 하나로 묶어 사용하기 위한 get_json_by_response 만들어 처리하자.
    """
    async def get_json_by_response(self, dictionary, websocket):
        api_response = await self.get_response(dictionary, websocket)
        return self.convert_json_pretty(api_response)


    # 들여쓰기를 적용하여 JSON 데이터를 깔끔하게 출력
    def convert_json_pretty(self, json_string):
        data = json.loads(json_string)
        return json.dumps(data, indent=4, ensure_ascii=False)
    

    # 요청 정보 가져오기
    async def get_response(self, dictionary : Dict, websocket):
        json_request = json.dumps(dictionary)
        await websocket.send(json_request)
        response = await websocket.recv()
        return response


    # vtube API 사용을 위한 인증 토큰 발급
    async def get_authentication_token(self, dictionary, websocket):
        response = await self.get_response(dictionary, websocket)
        token = json.loads(response)['data']['authenticationToken']
        return token
    

    # 토큰 수정
    def modify_authentication_token(self, dictionary, token):
        dictionary['data']['authenticationToken'] = token
        return json.dumps(dictionary)
    

    # 모델 ID 받아오기
    async def get_model_id(self, dictionary, websocket):
        response = await self.get_response(dictionary, websocket)
        model_id = json.loads(response)['data']['modelID']
        return model_id


    # 모델 ID 수정
    def modify_model_id(self, dictionary, model_id):
        dictionary['data']['modelID'] = model_id
        return json.dumps(dictionary)

    
    # 모델 핫키 추가하기
    def modify_hotkey_id(self, dictionary, hotkeyID):
        dictionary['data']['hotkeyID'] = hotkeyID
        return json.dumps(dictionary)