from api.services.utility_service import generate_random_prices, generate_random_amounts

def get_bulk_order_list(data, band_algorithm=None):
    price_difference_range_start = data.get('priceDifferenceRangeStart')
    price_difference_range_end = data.get('priceDifferenceRangeEnd')
    no_of_orders = data.get('noOfOrders')
    cash_amount = data.get('cashAmount')
    order_type = data.get('orderType')
    price_range_start = data.get('priceRangeStart')
    price_range_end = data.get('priceRangeEnd')
    if band_algorithm == 'HighVolumeLowPrice':
        orders_list = generate_high_volume_low_price_orders(no_of_orders, cash_amount, order_type, price_range_start, price_range_end, price_difference_range_start, price_difference_range_end)
    elif band_algorithm == 'GradualRestriction':
        orders_list = generate_gradual_restriction_orders(no_of_orders, cash_amount, order_type, price_range_start, price_range_end, price_difference_range_start, price_difference_range_end)
    else:
        orders_list = generate_equal_volume_distribution_orders(no_of_orders, cash_amount, order_type, price_range_start, price_range_end, price_difference_range_start, price_difference_range_end)
    return orders_list

def generate_equal_volume_distribution_orders(no_of_orders, cash_amount, order_type, price_range_start, price_range_end, price_difference_range_start, price_difference_range_end):
    prices, no_of_orders = generate_random_prices(no_of_orders, price_range_start, price_range_end, price_difference_range_start, price_difference_range_end)
    amounts = generate_random_amounts(cash_amount, no_of_orders)
    orders_list = []
    for index, price in enumerate(prices):
        order = {
            "side": order_type,
            "ordType": "LIMIT",
            "ordPrice": price,
            "ordQty": f"{round(amounts[index]/price)}"
        }
        orders_list.append(order)
    return orders_list

def generate_high_volume_low_price_orders(no_of_orders, cash_amount, order_type, price_range_start, price_range_end, price_difference_range_start, price_difference_range_end):
    prices, no_of_orders = generate_random_prices(no_of_orders, price_range_start, price_range_end, price_difference_range_start, price_difference_range_end)
    amounts = generate_random_amounts(cash_amount, no_of_orders)
    buy_order = order_type == 'BUY'
    amounts.sort(reverse=(not buy_order))
    orders_list = []
    for index, price in enumerate(prices):
        order = {
            "side": order_type,
            "ordType": "LIMIT",
            "ordPrice": price,
            "ordQty": f"{round(amounts[index]/price)}"
        }
        orders_list.append(order)
    return orders_list

def generate_gradual_restriction_orders(no_of_orders, cash_amount, order_type, price_range_start, price_range_end, price_difference_range_start, price_difference_range_end):
    prices, no_of_orders = generate_random_prices(no_of_orders - 1, price_range_start, price_range_end, price_difference_range_start, price_difference_range_end)
    amounts = generate_random_amounts(cash_amount * 0.8, no_of_orders - 1)
    amounts.sort()
    orders_list = []
    for index, price in enumerate(prices):
        order = {
            "side": order_type,
            "ordType": "LIMIT",
            "ordPrice": price,
            "ordQty": f"{round(amounts[index]/price)}"
        }
        orders_list.append(order)
    fail_safe_order = {
        "side": order_type,
        "ordType": "LIMIT",
        "ordPrice": price_range_end,
        "ordQty": f"{round(cash_amount*0.2/price_range_end)}"
    }
    orders_list.append(fail_safe_order)
    return orders_list