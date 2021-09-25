from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param

def get_token(request: Request):    
    authorization: str = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    #token = param
    return param