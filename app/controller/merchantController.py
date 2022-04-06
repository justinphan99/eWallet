from app.services.merchantService import *

class MerchantController():
    def __init__(self):
        self.method = None
        self.data = None
        self.accountId = None
        
    def operation(self,data,accountId):
        if self.method == "GET":
            return select_a_merchant()
        elif self.method == "POST":
            print("POST merchant")
            return create_a_merchant(data)