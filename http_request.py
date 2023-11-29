import hashlib
import hmac
import json
import math
import time
import requests
from settings import http_api_key, http_api_secret
api_key = http_api_key
secret_key = http_api_secret
expires = int(time.time() * 1000)
expires_key = str(math.floor(expires / 30000))
expires_key = expires_key.encode("utf-8")
key = hmac.new(secret_key, expires_key, hashlib.sha256).hexdigest()
key = key.encode("utf-8")


def make_api_request(url, data, stringType=None):
    if stringType:    
        payload = data
    else:   
        payload = json.dumps(data)
    payload = payload.encode("utf-8")
    signature = hmac.new(key, payload, hashlib.sha256).hexdigest()
    headers = {
    'X-CS-APIKEY': api_key,
    'X-CS-SIGN': signature,
    'X-CS-EXPIRES': str(expires),
    'exch-language': 'en_US',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    # 'Host': 'https://api.coinstore.com',
    'Connection': 'keep-alive'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return json.loads(response.text).get('data')
    else:
        print(response.text)
        