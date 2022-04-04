from app.services.test import GetHello, PostHello

class HelloClassController():
    def __init__(self):
        self.method = None
        self.data = None
        
    def operation(self,data):
        if self.method == "GET":
            return GetHello()
        elif self.method == "POST":
            return PostHello(data)