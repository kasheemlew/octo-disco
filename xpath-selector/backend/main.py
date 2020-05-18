import asyncio
from aiohttp import web
from utils import crawl


async def index(request):
    return web.Response(text='ok')


async def xpaths(request):
    data = await request.json()
    print(data)
    await crawl(data['url'], data['xpaths'])
    return web.Response(text='ok')

app = web.Application()
app.add_routes([
    web.get('/', index),
    web.post('/xpaths', xpaths)
])

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=5000)
