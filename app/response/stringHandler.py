import json
from app.response.requestHandler import RequestHandler

class StringHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.contentType = 'application/json'

    def stringParse(self, data):
        try:
            self.contents = data
            self.setStatus(200)
            return True
        except:
            self.setStatus(404)
            return False