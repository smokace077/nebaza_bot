from aiohttp import web

async def handle(request):
    return web.Response(text="Hello, world!")

app = web.Application()
app.router.add_get('/', handle)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)
