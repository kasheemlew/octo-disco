from aiohttp import web, WSMessage
from aiohttp.web_request import BaseRequest

from garbanzo.controller import MainController

routes = web.RouteTableDef()
controller = MainController()


@routes.get('/{name}')
async def handle(request):
    name = request.match_info.get('name', 'Anonymous')
    text = f'Hello, {name}'
    return web.json_response(dict(text=text))


@routes.get('/echo')
async def wshandle(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    msg: WSMessage
    async for msg in ws:
        if msg.type == web.WSMsgType.text:
            await ws.send_str(f'Hello, {msg.data}')
        elif msg.type == web.WSMsgType.binary:
            await ws.send_str(msg.data)
        elif msg.type == web.WSMsgType.close:
            break
    return ws


@routes.post('/crawl')
async def crawl(request: BaseRequest):
    post = await request.post()
    await controller.run(post.get('data'))
    return web.json_response({'msg': 'success'})


app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app)
