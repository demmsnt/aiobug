from aiohttp import web
import tempfile

__version__ = '1.0'

async def show_form(request):
    text = """<html><body>
    <form action="/" method="post" enctype="multipart/form-data">
    <input type="file" name="fileToUpload">
    <input type="submit">
    </form>
    </body></html>"""
    return web.Response(text=text,
                        content_type="text/html")

async def file_upload(request):
    print("Start file upload")
    reader = await request.multipart()
    file_handler = await reader.next()
    filename = file_handler.filename

    # You cannot relay on Content-Length if transfer is chunked.
    size = 0
    with tempfile.TemporaryFile() as f:
        while True:
            chunk = await file_handler.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)
    print("End file upload. {} bytes received".format(size))
    return web.Response(text='{} sized of {} successfully stored'
                             ''.format(filename, size))

def main(*args):
    app = web.Application()
    app.router.add_get('/', show_form)
    app.router.add_post('/', file_upload)
    web.run_app(app)
