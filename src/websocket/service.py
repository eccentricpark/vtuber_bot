# 비즈니스 로직 계층
import json
api_state_request = {
    "apiName": "VTubeStudioPublicAPI",
    "apiVersion": "1.0",
    "requestID": "requestMyState",
    "messageType": "APIStateRequest"
}
class VTubeStudioHandler:
    def __init__(self):
        self.clients = set()

    async def connect(self, websocket):
        self.clients.add(websocket)
        await websocket.send_str(json.dumps(api_state_request))

    def disconnect(self, websocket):
        self.clients.remove(websocket)

    async def handle_message(self, message):
        # 특정 키워드가 포함되어 있는지 확인
        print(message)
        if "특정 키워드" in message:
            await self.special_function()

    async def special_function(self):
        # 특정 키워드가 감지될 때 실행할 함수
        print("특정 키워드가 감지되었습니다!")