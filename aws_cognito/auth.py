from functools import wraps
from typing import List

from fastapi import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from aws_cognito.jwt_bearer import CognitoAuthenticator
import os


auth = CognitoAuthenticator(
    pool_region=os.getenv("POOL_REGION"),
    pool_id=os.getenv("POOL_ID"),
    client_id=os.getenv("CLIENT_ID"),
)

def auth_required():
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request,*args, **kwargs):
            credentials = request.headers.get("Authorization", None) # Bearer token
            if credentials:
                try:
                    claims = auth.verify_token(credentials.split(' ')[1])
                    print(claims)
                except Exception as e:
                    print(e)
                    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
            else:
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

            return await func(request,*args, **kwargs)

        return wrapper

    return decorator