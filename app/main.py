import aiohttp
import time
import jwt
import uvicorn
from datetime import date
from urllib.parse import urljoin
from fastapi import FastAPI, Request


TARGET_ENDPOINT = 'http://127.0.0.1:5000'
SECRET_KEY = 'a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf '
USER_PARAM = 'user'
USERNAME_PARAM = 'username'
JWT_HEADER = 'x-my-jwt'
CONTENT_TYPE_PARAM = 'CONTENT-TYPE'
DEFAULT_CONTENT_TYPE = 'application/json'
IAT_PARAM = 'iat'
DATE_PARAM = 'date'
ALGORITHM = "HS512"

HOST = '0.0.0.0'
PORT = 8000

app = FastAPI()


@app.post("/demo")
async def proxy_request(request: Request):
    target_url = urljoin(TARGET_ENDPOINT, request.url.path)
    post_data = await request.json()
    username = post_data[USERNAME_PARAM]
    jwt_token = create_jwt_token(username)
    headers = {JWT_HEADER: jwt_token, CONTENT_TYPE_PARAM: DEFAULT_CONTENT_TYPE}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(target_url, json=post_data) as res:
            res_body = await res.json()
    res_status = res.status
    response = {"status": res_status, "message": res_body}
    return response


def create_jwt_token(username):
    today = date.today()
    today_date = today.strftime("%Y-%m-%d")
    payload = {IAT_PARAM: int(time.time()), USER_PARAM: username, DATE_PARAM: today_date}
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
