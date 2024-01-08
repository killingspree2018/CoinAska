import random
# import schedule
import time
from datetime import datetime
from pytz import timezone
import math
from api.services.third_party_service import ThirdPartyService
from api.services.order_service import generate_volume_bot_orders

third_party_service = ThirdPartyService()
frequency = 0.08
amount = 100

def get_lowest_selling_price(old_price):
    depth_data = third_party_service.get_depth_data().get('data')
    sell_orders = depth_data.get('a')
    sell_order_prices = [order[0] for order in sell_orders]
    lowest_selling_price = float(min(sell_order_prices))
    if old_price is None or old_price != lowest_selling_price:
        print(f'Lowest Selling order Price at {lowest_selling_price}')
        return lowest_selling_price, True
    return lowest_selling_price, False


def price_movement():
    t = 0
    old_price = None
    # plot_time = 0
    # xpoints = []
    # ypoints = []
    lowest_selling_price, price_changed = get_lowest_selling_price(old_price)
    old_price = lowest_selling_price
    while True:
        lower_cap = lowest_selling_price * 0.99
        spectrum = 0.01 * lowest_selling_price
        price_offset = lower_cap + (spectrum * random.randint(1, 9))/10
        amplitude = random.uniform(spectrum * 0.02, spectrum * 0.09)
        t = t % (3 / frequency)
        cycles = random.randint(1, 5)
        total_time = (cycles * 3 / frequency) + t
        while t < total_time:
            lowest_selling_price, price_changed = get_lowest_selling_price(old_price)
            if price_changed:
                old_price = lowest_selling_price
                price_changed = False
                break
            price = round(price_offset + amplitude * math.sin(frequency * t), 8)
            # orders = generate_volume_bot_orders(price, amount)
            # response = third_party_service.create_bulk_orders(orders)
            now = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
            print(f'Time = {now} : Price = {price}')
            # xpoints.append(plot_time)
            # ypoints.append(price)
            rand_time_jump = random.randint(1, 10)
            t += rand_time_jump
            time.sleep(5)
            # plot_time += rand_time_jump
        # print(f'-------------Part:-{x}---with-cylces-{cycles}------------')
    # plt.plot(xpoints, ypoints)
    # plt.show()

price_movement()
# schedule.every(30).seconds.do(price_movement)