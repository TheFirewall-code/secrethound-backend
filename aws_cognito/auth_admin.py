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

my_values = os.getenv('ADMIN_VALUES')

# Convert the comma-separated string to a Python list
if my_values:
    my_values_list = my_values.split(',')
else:
    my_values_list = []


def auth_admin():
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request,*args, **kwargs):
            credentials = request.headers.get("Authorization", None) # Bearer token
            if credentials:
                try:
                    claims = auth.verify_token(credentials.split(' ')[1])
                    print(claims)
                    if claims["email"] not in my_values_list :
                        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
                except Exception as e:
                    print(e)
                    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
            else:
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

            return await func(request,*args, **kwargs)

        return wrapper

    return decorator