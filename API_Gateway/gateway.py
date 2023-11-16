from fastapi import FastAPI, Request, HTTPException
import requests
import json

app = FastAPI()

with open('services_config.json', 'r') as config_file:
    gateway_config = json.load(config_file)


@app.api_route("/{public_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway_route(public_path: str, request: Request):
    service_config = None
    for route in gateway_config["routes"]:
        if public_path == route["public_path"]:
            service_config = route
            break

    if service_config:
        method = request.method
        body = await request.json() if request.headers.get("Content-Type", "").startswith(
            "application/json") else await request.body()

        full_url = f"{service_config['service_url']}/{public_path}"

        headers = {key: value for key, value in request.headers.items()}
        response = requests.request(method, full_url, headers=headers, json=body if isinstance(body, dict) else None)

        return response.content, response.status_code
    else:
        raise HTTPException(status_code=404, detail="Service not found")