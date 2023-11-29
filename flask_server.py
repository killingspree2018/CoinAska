from flask import Flask, request
import random
app = Flask(__name__)

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
        price_difference_range_start = data.get('priceDifferenceRangeStart')
        price_difference_range_end = data.get('priceDifferenceRangeEnd')
        no_of_orders = data.get('noOfOrders')
        cash_amount = data.get('cashAmount')
        order_type = data.get('orderType')
        price_range_start = data.get('priceRangeStart')
        price_range_end = data.get('priceRangeEnd')
        prices, no_of_orders = generate_random_prices(no_of_orders, price_range_start, price_range_end, price_difference_range_start, price_difference_range_end)
        amounts = generate_random_amounts(cash_amount, no_of_orders)
        # {
        #     "symbol": "LUFFYUSDT",
        #     "orders": [
        #         {
        #             "side": "BUY",
        #             "ordType": "LIMIT",
        #             "ordPrice": 9.2e-10,
        #             "ordQty": "1"
        #         },
        #         {
        #             "side": "BUY",
        #             "ordType": "LIMIT",
        #             "ordPrice": 9.2e-10,
        #             "ordQty": "1"
        #         }
        #     ],
        #     "timestamp": 1642574848089
        # }
        orders_list = []
        for index, price in enumerate(prices):
            order = {
                "side": order_type,
                "ordType": "LIMIT",
                "ordPrice": price,
                "ordQty": f"{round(amounts[index]/price, int(8))}"
            }
            orders_list.append(order)
        bulk_order_payload = {
            "symbol": "askausdt",
            "orders": orders_list
        }
        print(bulk_order_payload)
        return bulk_order_payload


def generate_random_prices(no_of_orders, price_range_start, price_range_end, price_difference_range_start, price_difference_range_end):

    # Calculate the maximum number of orders that can be generated
    max_possible_orders = min(int((price_range_end - price_range_start) / price_difference_range_start) + 1, int((price_range_end - price_range_start) / price_difference_range_end) + 1)

    # Check if it's possible to generate 'n' orders with the given conditions
    if max_possible_orders < no_of_orders:
        print(f"Cannot generate {no_of_orders} orders with the given conditions.")
        print(f"Maximum number of orders that can be generated: {max_possible_orders}")
        no_of_orders = max_possible_orders  # Set no_of_orders to the maximum possible orders

    # Generate orders
    prices = [price_range_start]
    for _ in range(1, no_of_orders):
        diff = round(random.uniform(price_difference_range_start, price_difference_range_end), int(8))
        price = prices[-1] + diff
        prices.append(price)
    print(prices)
    return prices, no_of_orders

def generate_random_amounts(cash_amount, no_of_orders):
    sum_of_random_numbers = 0
    random_numbers = []
    random_amounts = []
    for _ in range(0, no_of_orders):
        random_no = round(random.uniform(5, 10), int(8))
        random_numbers.append(random_no)
        sum_of_random_numbers += random_no
    scaling_factor = cash_amount/sum_of_random_numbers
    for random_number in random_numbers:
        random_amounts.append(random_number*scaling_factor)
    print(random_amounts)
    return random_amounts


if __name__ == '__main__':
    app.run(debug=True)