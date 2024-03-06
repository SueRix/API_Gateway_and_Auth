import json
import time

import aiohttp
import jwt
from fastapi import FastAPI, Request, Response, HTTPException, status
from jwt import PyJWTError
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from settings import Settings, settings

SECRET_KEY = "Cj9Ndq9c2mSPaI6zHHkdWwEXpudGUlYf1234567890abcdefgijklmnopqrstuvwxyz"
ALGORITHM = "HS512"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('services_config.json', 'r') as config_file:
    gateway_config = json.load(config_file)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


@app.api_route("/{public_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", ])
async def gateway_route(public_path: str, request: Request):
    service_config = None
    call_headers = {}
    query_params_dict = dict(request.query_params)

    for route in gateway_config["routes"]:
        if public_path == route["public_path"]:
            service_config = route
            break

    if not service_config:
        raise HTTPException(status_code=404, detail="Service not found")

    user_id = None

    if service_config.get("required_validation_token"):
        if auth_header := request.headers.get("Authorization"):
            call_headers["Authorization"] = auth_header
        else:
            raise HTTPException(status_code=401, detail="Authorization header is missing")

        token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None
        if not token:
            raise HTTPException(status_code=401, detail="Token not provided")

        decoded_token = decode_jwt(token)
        user_id = decoded_token.get("user_id")

        if decoded_token["exp"] < time.time():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired")

        if decoded_token.get("token_type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

        if not user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User ID not found in token")

    method = request.method
    body = None
    if 'create' in public_path:
        if request.headers.get("content-type") == "application/json":
            body = await request.json()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Request is invalid, because it not in JSON format")

        if isinstance(body, dict):
            body["userId"] = str(user_id)
        else:
            pass
    if method != "GET":
        if request.headers.get("content-type") == "application/json":
            body = await request.json()
        else:
            body = await request.body()

    if user_id and 'calendarNote' in public_path:
        query_params_dict["userId"] = user_id

    query_string = "&".join([f"{key}={value}" for key, value in query_params_dict.items()])
    service_url = getattr(settings, service_config['service_url'])
    full_url = f"{service_url}/{public_path}?{query_string}"

    async with aiohttp.ClientSession() as session:
        async with session.request(method, full_url, headers=call_headers,
                                   json=body if isinstance(body, dict) else None) as response:
            try:  # FIXME
                response_content = await response.json()
                return JSONResponse(content=response_content, status_code=response.status)
            except ValueError:  # TODO: add 1 more error in except aiohttp network error(error could be reproduced by delete specify allowed host)
                response_content = await response.read()
                return Response(content=response_content, status_code=response.status)
