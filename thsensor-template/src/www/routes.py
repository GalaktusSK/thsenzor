from microdot import Microdot, send_file, Response


app = Microdot()
Response.default_content_type = 'text/html'


@app.route('/static/<path:path>')
async def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file(f'/www/static/{path}', max_age=86400)


@app.route('/')
async def index(request):
    return 'Hello, world!'
