from api.services.third_party_service import ThirdPartyService
import json, math, random
import matplotlib.pyplot as plt
# import numpy as np

third_party_service = ThirdPartyService()
# data = {
#     "symbol": "askausdt",
#     "side": "BUY",
#     "ordType": "LIMIT",
#     "ordPrice": "0.00953000",
#     "ordQty": "5"
# }
# payload = json.dumps(data)
# response = third_party_service.create_headers(payload)
# print(response)

# ticker_info = third_party_service.get_ticker_information()
# print(ticker_info)

account_info = third_party_service.get_user_information()
print(account_info)

# orders_info = third_party_service.get_current_orders()
# print(orders_info)


# # Print the values in pairs
# for point in endpoints:
#     print(f"({point[0]:.2f}, {point[1]:.2f})")