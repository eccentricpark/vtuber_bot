from aiohttp import web
from controller import websocket_handler
from service import VTubeStudioHandler


# 메인 애플리케이션 설정
vtube_handler = VTubeStudioHandler()

app = web.Application()
app['vtube_handler'] = vtube_handler
app.router.add_get('/', websocket_handler)
# app.router.add_route('*','/', websocket_handler)

web.run_app(app, host='localhost', port=8001)


