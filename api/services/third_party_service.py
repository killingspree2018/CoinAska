import hashlib
import hmac
import json
import math
import time
import requests
from settings import http_api_key, http_secret_key
api_key = http_api_key
secret_key = http_secret_key
expires = int(time.time() * 1000)
expires_key = str(math.floor(expires / 30000))
expires_key = expires_key.encode("utf-8")
key = hmac.new(secret_key, expires_key, hashlib.sha256).hexdigest()
key = key.encode("utf-8")

class ThirdPartyService:
    def __init__(self):
        self.ticker_name = 'askausdt'
        self.ticker_id = 739

    def make_api_request(self, url, data, stringType=None):
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
        print(f'Making api call to {url} with payload {payload} with headers {headers}')
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(response.text)

    def get_ticker_information(self):
        url = "https://api.coinstore.com/api/v2/public/config/spot/symbols"
        data = {
            "symbolCodes":[self.ticker_name],
            "symbolIds":[self.ticker_id]
        }
        try:
            ticker_data = self.make_api_request(url, data)
            print(ticker_data)
        except Exception as err:
            print(err)

    def get_user_information(self):
        url = "https://api.coinstore.com/api/spot/accountList"
        data = {
            "symbolCodes":[self.ticker_name],
            "symbolIds":[self.ticker_id]
        }
        try:
            users = self.make_api_request(url, data)
            print(users)
        except Exception as err:
            print(err)
    
    def get_current_orders(self, version=None):
        url = "https://api.coinstore.com/api/" + (f"{version}/trade/order/active" if version is not None else 'trade/order/active')
        # data = {
        #     "symbolCodes":[self.ticker_name],
        #     "symbolIds":[self.ticker_id]
        # }
        try:
            current_orders = self.make_api_request(url, 'symbol=askausdt', True)
            print(current_orders)
        except Exception as err:
            print(err)

    def cancel_orders(self, order_id, all_orders=None):
        url = f"https://api.coinstore.com/api/trade/order/{'cancelAll' if all_orders else 'cancel'}"
        data = {
            "symbol": self.ticker_name,
        }
        if not all_orders:
            data["ordId"] = order_id
        try:
            current_orders = self.make_api_request(url, data)
            print(current_orders)
        except Exception as err:
            print(err)

    # /trade/order/placeBatch
    def create_bulk_orders(self, orders_list):
        order_data = {
            "symbol": self.ticker_name,
            "orders": orders_list
        }
        url = "https://api.coinstore.com/api/trade/order/placeBatch"
        response = self.make_api_request(url, order_data)
        return response


    
    

