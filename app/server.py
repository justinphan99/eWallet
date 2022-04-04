import os

from http.server import BaseHTTPRequestHandler
from app.routes.main import routes
from app.response.jsonHandler import JsonHandler
from app.response.badRequestHandler import BadRequestHandler
import json

class Server(BaseHTTPRequestHandler):

    def do_HEAD(self):
        return

    def do_GET(self):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]
        if self.path in routes:
            temp = routes[self.path]
            temp.method = 'GET'
            handler = JsonHandler()
            handler.jsonParse(temp.operation(''))
        else:
            handler = BadRequestHandler()
        self.respond({
            'handler': handler
        })

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length) 
        post_data = json.loads(post_data.decode().replace("'", '"'))
        print(type(post_data))
        print(post_data)
        split_path = os.path.splitext(self.path)

        if self.path in routes:
            a = routes[self.path]
            a.method = "POST"
            handler = JsonHandler()
            a.operation(post_data)
            handler.jsonParse(a.operation(post_data))
        else:
            handler = BadRequestHandler()

        self.respond({
            'handler': handler
        })

    def handle_http(self, handler):
        status_code = handler.getStatus()
        self.send_response(status_code)

        if status_code is 200:
            content = handler.getContents()
            self.send_header('Content-type', handler.getContentType())
        else:
            content = json.dumps({
                "status": 404,
                "message": "404 Not Found"
            })
        self.end_headers()

        return content.encode()

    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)