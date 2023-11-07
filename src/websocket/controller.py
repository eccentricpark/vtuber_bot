from aiohttp import web

# 프레젠테이션 계층
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    await request.app['vtube_handler'].connect(ws)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            await request.app['vtube_handler'].handle_message(msg.data)
        elif msg.type == web.WSMsgType.ERROR:
            print(f'ws connection closed with exception {ws.exception()}')
        else:
            print("에러가 발생했습니다.")

    request.app['vtube_handler'].disconnect(ws)
    print('websocket connection closed')

    return ws

