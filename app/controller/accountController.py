from app.services.accountService import *

class AccountController():
    def __init__(self):
        self.method = None
        self.data = None
        
    def operation(self,data):
        if self.method == "GET":
            return select_all_account()
        elif self.method == "POST":
            data = str(data['accountType'])
            print(data)
            return create_a_account(data)
        return