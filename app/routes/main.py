from app.controller.hellocontroller import HelloClassController
from app.controller.accountController import AccountController

routes = {
    "/hello": HelloClassController(),
    "/account" : AccountController()
}