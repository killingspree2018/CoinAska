from database_connection import cursor
from http_request import make_api_request

ticker_name = 'askausdt'
ticker_id = 739
bot_configurables = {}
buy_price_bands = []
sell_price_bands = []
current_price = None

def get_bot_configurables():
    cursor.execute('Select * From BotConfigurables')
    parameters = cursor.fetchall()
    bot_configurables = dict((parameter_name, parameter_value) for parameter_name, parameter_value in parameters)
    print(bot_configurables)


def get_price_bands():
    cursor.execute('Select * From PriceBands')
    price_bands = cursor.fetchall()
    # band_parameters = ('StartPercentage', 'EndPercentage', 'CustomEndPrice', 'PriceDifference', 'BandAlgorithm')
    for id, type, band_name, start_percentage, end_percentage, custom_end_price, price_difference, band_algorith in price_bands:
        if type == 'Buy':
            buy_price_bands.append({'StartPercentage': start_percentage, 'EndPercentage': end_percentage, 'CustomEndPrice': custom_end_price, 'PriceDifference': price_difference, 'BandAlgorith': band_algorith})
        else:
            sell_price_bands.append({'StartPercentage': start_percentage, 'EndPercentage': end_percentage, 'PriceDifference': price_difference, 'BandAlgorith': band_algorith})
    print(buy_price_bands)
    print(sell_price_bands)
    
    
def get_ticker_information():
    url = "https://api.coinstore.com/api/v2/public/config/spot/symbols"
    data = {
        "symbolCodes":[ticker_name],
        "symbolIds":[ticker_id]
    }
    try:
        ticker_data = make_api_request(url, data)
        print(ticker_data)
    except Exception as err:
        print(err)
        
def get_user_information():
    url = "https://api.coinstore.com/api/spot/accountList"
    data = {
        "symbolCodes":[ticker_name],
        "symbolIds":[ticker_id]
    }
    try:
        users = make_api_request(url, data)
        print(users)
    except Exception as err:
        print(err)
        
        
def get_current_orders(version=None):
    url = "https://api.coinstore.com/api/" + (f"{version}/trade/order/active" if version is not None else 'trade/order/active')
    # data = {
    #     "symbolCodes":[ticker_name],
    #     "symbolIds":[ticker_id]
    # }
    try:
        current_orders = make_api_request(url, 'symbol=btcusdt', True)
        print(current_orders)
    except Exception as err:
        print(err)
        

def cancel_orders(order_id, all_orders=None):
    url = f"https://api.coinstore.com/api/trade/order/{'cancelAll' if all_orders else 'cancel'}"
    data = {
        "symbol": ticker_name,
    }
    if not all_orders:
        data["ordId"] = order_id
    try:
        current_orders = make_api_request(url, data)
        print(current_orders)
    except Exception as err:
        print(err)
      
def create_orders(order_data):
    url = f"https://api.coinstore.com/api/trade/order/{'place' if len(order_data) == 1 else 'placeBatch'}"
    
    data = {
        # "clOrdId": "8vdpfHC0LmhojVIffOlkBc9bV9992",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "ordType": "LIMIT",
        "ordPrice": "30000",
        "ordQty": "1",
        # "ordAmt": "",
        # "timeInForce": ""
    }
    
    {
    "symbol": "LUFFYUSDT",
    "orders": [
        {
            "side": "BUY",
            "ordType": "LIMIT",
            "ordPrice": 9.2e-10,
            "ordQty": "1"
        },
        {
            "side": "BUY",
            "ordType": "LIMIT",
            "ordPrice": 9.2e-10,
            "ordQty": "1"
        }
    ],
    "timestamp": 1642574848089
}
    response = make_api_request("POST", url, headers=headers, data=payload)
    print(response.text)
    
    
# get_bot_configurables()
# get_price_bands()
# get_ticker_information()
# get_user_information()
get_current_orders()
get_current_orders('V2')

    
    

