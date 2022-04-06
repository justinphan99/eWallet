from app.controller.hellocontroller import HelloClassController
from app.controller.accountController import AccountController, AccountTokenController
from app.controller.merchantController import MerchantController

routes = {
    "/hello": HelloClassController(),
    "/account" : AccountController(),
    "/merchant/signup": MerchantController(),
    "/account/{accountId}/token": AccountTokenController()
}