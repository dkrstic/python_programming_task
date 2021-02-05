import requests
import time
from fastapi import FastAPI, Request


HOST = '0.0.0.0'
PORT = 5000
PROXY_PORT = 8000
TEST_PROXY_URL = 'http://127.0.0.1:5000/demo'

test_app = FastAPI()


@test_app.post("/demo")
async def proxy_request(request: Request):
    post_data = await request.json()
    headers = request.headers
    for header in headers:
        print("{}: {}".format(header, headers.get(header)))
    print("Message: {}".format(post_data))
    return post_data


def test_proxy(test_proxy_url, post_data, STATUS_OK=200):
    res = requests.post(test_proxy_url, json=post_data)
    test_data = res.json()
    assert res.status_code == STATUS_OK
    assert test_data == post_data


if __name__ == "__main__":
    test_data = {"username": "tebra", "city": "SU"}
    time.sleep(5)
    test_proxy(TEST_PROXY_URL, test_data)
