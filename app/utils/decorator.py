from functools import wraps
import app.services.authService as auth
from ..response.unauthorizedRequestHandler import UnauthorizedRequestHandler

def tokenRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authToken = args[0]
        response = auth.getLoggedInAccount(authToken)
        print(">>> UnauthorizedRequestHandler")
        if response == None:
            return 401
        return f(*args, **kwargs)

    return decorated


def tokenIssuerRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authToken = args[0]
        response = auth.getLoggedInAccount(authToken)
        print(">>> UnauthorizedRequestHandler")
        if response == None or response['accountType'] != 'issuer':
            return 401
        return f(*args, **kwargs)

    return decorated


def tokenPersonalRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authToken = args[0]
        response = auth.getLoggedInAccount(authToken)
        print(">>> UnauthorizedRequestHandler")
        if response == None or response['accountType'] != 'personal':
            print("UnauthorizedRequestHandler")
            return 401
        return f(*args, **kwargs)

    return decorated


def tokenMerchantRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authToken = args[0]
        response = auth.getLoggedInAccount(authToken)
        print(">>> UnauthorizedRequestHandler")
        if response == None or response['accountType'] != 'merchant':
            print("UnauthorizedRequestHandler")
            return 401
        return f(*args, **kwargs)

    return decorated
