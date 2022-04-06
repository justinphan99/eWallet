import os

from http.server import BaseHTTPRequestHandler
from app.routes.main import routes
from app.response.jsonHandler import JsonHandler
from app.response.stringHandler import StringHandler
from app.response.badRequestHandler import BadRequestHandler
import json
from app.controller.accountController import AccountAccountIdController, AccountTokenController
from app.utils.baseFunc import decode_auth_token

class Server(BaseHTTPRequestHandler):

    def do_HEAD(self):
        return

    def do_GET(self):
        print(self.path)
        if self.path.split("/")[2] and len(self.path.split("/")[2]) == 36:
            accountId = str(self.path.split("/")[2])
            if self.path.split("/")[3] and self.path.split("/")[3] == 'token':
                temp = AccountTokenController()
                temp.method = 'GET'
                data = temp.operation('',accountId)
                handler = StringHandler()
                handler.stringParse(data)
            elif self.path.split("/")[3] and self.path.split("/")[3] == 'topup':
                token = str(self.headers['Authorization'])
                accountId = decode_auth_token(token)
                
        elif self.path in routes:
            accountId = ''
            temp = routes[self.path]
            temp.method = 'GET'
            handler = JsonHandler()
            handler.jsonParse(temp.operation('',accountId))
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
        accountId = ''

        if self.path in routes:
            a = routes[self.path]
            a.method = "POST"
            handler = JsonHandler()
            handler.jsonParse(a.operation(post_data, accountId))
        else:
            handler = BadRequestHandler()

        self.respond({
            'handler': handler
        })

    def handle_http(self, handler):
        status_code = handler.getStatus()
        self.send_response(status_code)

        if status_code == 200:
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