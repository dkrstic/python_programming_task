import aiohttp
import starlette
import time
import jwt
import uvicorn
from fastapi import FastAPI, Request
from datetime import date
from urllib.parse import urljoin
from httpx import Response


TARGET_ENDPOINT = 'http://127.0.0.1:5000'
SECRET_KEY = 'a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01 d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf'

HOST = '0.0.0.0'
PORT = 8000

app = FastAPI()


@app.post("/demo")
async def proxy_request(request: Request):
    target_url = urljoin(TARGET_ENDPOINT, request.url.path)
    post_data = request.json()
    username = post_data["username"]
    print(request.url.path)
    print(target_url)
    jwt_token = create_jwt_token(username)
    headers = {"x-my-jwt": jwt_token, 'CONTENT-TYPE': 'application/json'}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(target_url, json=post_data) as res:
            res_status = await res.status
    return res_status


def create_jwt_token(username):
    today = date.today()
    today_date = today.strftime("%Y-%m-%d")
    payload = {"iat": int(time.time()), "user": username, "date": today_date}
    return jwt.encode(payload, SECRET_KEY, "HS512")


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
