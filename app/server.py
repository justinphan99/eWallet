import os

from http.server import BaseHTTPRequestHandler
from app.routes.main import routes
from app.response.jsonHandler import JsonHandler
from app.response.stringHandler import StringHandler
from app.response.badRequestHandler import BadRequestHandler
from app.response.successResponse import SuccessResponse
import json
from app.controller.accountController import AccountTokenController, AccountTopupController
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
                token_data = decode_auth_token(data)
                print(token_data)
                handler = JsonHandler()
                handler.jsonParse(data)

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
        accountId = ''
        token = str(self.headers['Authorization'])
        if self.path.split("/")[2] and len(self.path.split("/")[2]) == 36:
            accountId_URL = str(self.path.split("/")[2])
            if self.path.split("/")[3] and self.path.split("/")[3] == 'topup':
                print(token)
                if token:
                    accountId = decode_auth_token(token)
                    print(">>>accountID: "+ str(accountId))
                    temp = AccountTopupController()
                    temp.method = "POST"
                    accountType = temp.get_accountType(accountId)
                    if accountType == 'issuer':
                        response = temp.operation(post_data,accountId)
                        if response == "200":
                            handler = JsonHandler()
                            handler.jsonParse(response)
                        else:
                            handler = BadRequestHandler()
                    else:
                        handler = BadRequestHandler()
                else:
                    handler = BadRequestHandler()
        elif self.path in routes and token:
            temp = routes[self.path]
            print(self.path)
            temp.method = "POST"
            data = temp.operation(post_data, token)
            handler = JsonHandler()
            handler.jsonParse(data)

        elif self.path in routes:
            temp = routes[self.path]
            temp.method = "POST"
            handler = JsonHandler()
            handler.jsonParse(temp.operation(post_data, accountId))
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