import random

def generate_random_prices(no_of_orders, price_range_start, price_range_end, price_difference_range_start, price_difference_range_end):

    # Calculate the maximum number of orders that can be generated
    max_possible_orders = min(int(abs(price_range_end - price_range_start) / price_difference_range_start) + 1, int(abs(price_range_end - price_range_start) / price_difference_range_end) + 1)
    # Check if it's possible to generate 'n' orders with the given conditions
    if max_possible_orders < no_of_orders:
        print(f"Cannot generate {no_of_orders} orders with the given conditions.")
        print(f"Maximum number of orders that can be generated: {max_possible_orders}")
        no_of_orders = max_possible_orders  # Set no_of_orders to the maximum possible orders
    # Generate orders
    prices = []
    for _ in range(0, no_of_orders):
        diff = random.uniform(price_difference_range_start, price_difference_range_end)
        price_seed = prices[-1] if len(prices) else min(price_range_start, price_range_end)
        price = round(price_seed + diff, int(8))
        prices.append(price)
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
    return random_amounts
