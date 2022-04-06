from app.controller.hellocontroller import HelloClassController
from app.controller.accountController import AccountController, AccountTokenController
from app.controller.merchantController import MerchantController
from app.controller.transactionController import *

routes = {
    "/hello": HelloClassController(),
    "/account" : AccountController(),
    "/merchant/signup": MerchantController(),
    "/account/{accountId}/token": AccountTokenController(),
    "/transaction/create": TransactionCreateController(),
    "/transaction/confirm": TransactionConfirmController(),
    "/transaction/verify": TransactionVerifyController(),
    "/transaction/cancel": TransactionCancelController()
}