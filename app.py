from flask import Flask, Blueprint
from flask import request
from api.services.order_service import get_bulk_order_list
from api.services.third_party_service import ThirdPartyService

app = Flask(__name__)
blueprint = Blueprint('api', __name__)
app.register_blueprint(blueprint)


@app.route('/')
def index():
    return 'Hello, this is Coin Aska Market Making Bot Flask server!'

# {
#     "priceDifferenceRangeStart": 2,
#     "priceDifferenceRangeEnd": 3,
#     "noOfOrders": 10,
#     "cashAmount": 5000,
#     "orderType": "BUY",
#     "priceRangeStart": 100,
#     "priceRangeEnd": 105
# }
@app.route('/api/bulk-orders', methods=['POST'])
def place_bulk_orders():
    if request.method == 'POST':
        # Your logic to fetch and return data
        data = request.json
        bulk_order_list = get_bulk_order_list(data)
        third_party_service = ThirdPartyService()
        response = third_party_service.create_bulk_orders(bulk_order_list)
        print(response)
        return response
        # return bulk_order_payload
        
@app.route('/api/get-orders', methods=['GET'])
def get_all_orders():
    if request.method == 'GET':
        # Your logic to fetch and return data
        third_party_service = ThirdPartyService()
        order_list = third_party_service.get_current_orders()
        print(order_list)
        return order_list

if __name__ == '__main__':
    app.run(debug=True)