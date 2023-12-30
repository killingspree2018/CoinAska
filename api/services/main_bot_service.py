from api.services.database_service import DatabaseService
from api.services.order_service import get_bulk_order_list
import random
import time
import math
from api.services.third_party_service import ThirdPartyService

class MarketMakingBotService:

    def __init__(self, current_price):
        self.database_obj = DatabaseService()
        self.current_price = current_price
        self.third_party_service = ThirdPartyService()
    
    def price_movement(lowest_selling_price):
        frequency = 0.08
        t = 0
        # plot_time = 0
        # xpoints = []
        # ypoints = []
        while True:
            upper_cap = lowest_selling_price
            lower_cap = upper_cap * 0.99
            spectrum = 0.01 * upper_cap
            price_offset = lower_cap + (spectrum * random.randint(1, 9))/10
            amplitude = random.uniform(spectrum * 0.02, spectrum * 0.09)
            t = t % (3 / frequency)
            cycles = random.randint(1, 5)
            total_time = (cycles * 3 / frequency) + t
            while t < total_time:
                price = price_offset + amplitude * math.sin(frequency * t)
                # print(f't = {t} : price = {price}')
                # xpoints.append(plot_time)
                # ypoints.append(price)
                rand_time_jump = random.randint(1, 10)
                t += rand_time_jump
                # plot_time += rand_time_jump
            # print(f'-------------Part:-{x}---with-cylces-{cycles}------------')
        # plt.plot(xpoints, ypoints)
        # plt.show()

    def start_processing(self):
        # get buy band in which current price of the stock lies
        buy_orders = self.place_orders(self.database_obj.buy_price_bands, 'BUY')
        sell_orders = self.place_orders(self.database_obj.sell_price_bands, 'SELL')
        # while True:
        #     self.toggle_post_only_orders(buy_orders, 'BUY')
        #     self.toggle_post_only_orders(sell_orders, 'SELL')
        #     time.sleep(0.5)

    def toggle_post_only_orders(self, orders, order_type):
        post_only_orders = []
        for order in orders:
            random_no = round(random.uniform(20, 40), int(8))
            order["ordQty"] = order.get("ordQty") * (random_no / 100)
            order["ordType"] = "POST_ONLY"
            post_only_orders.append(order)
        response = self.third_party_service.create_bulk_orders(post_only_orders)
        time.sleep(0.5)
        orders_data = response.get("data")
        order_ids = [order.get("ordId") for order in orders_data]
        self.third_party_service.cancel_orders_in_bulk(order_ids)
        print(f'This is the fake order list for {order_type} orders: {post_only_orders}')
        print("""
              ----------------------------------------------------------------------------------------------------    
              """)
            
    def place_orders(self, bands, order_type):
        buy_order = order_type == 'BUY'
        base_price = self.database_obj.base_price
        combined_order_list = []
        last_band = bands[-1]
        if not buy_order:
            last_band_end_percent = last_band.get('EndPercentage')
            last_band_end_value = round((1 + last_band_end_percent / 100) * base_price, 8)
            sell_buffer_end_value = round((1 + 25 / 100) * self.current_price, 8)
            data_buffer = {
                'priceDifferenceRangeStart': last_band.get('PriceDifferenceRangeStart'),
                'priceDifferenceRangeEnd': last_band.get('PriceDifferenceRangeEnd'),
                'noOfOrders': 0,
                'cashAmount': 0,
                'orderType': order_type,
                'priceRangeStart': last_band_end_value,
                'priceRangeEnd': sell_buffer_end_value
            }
        for band in bands:
            start_percent = -band.get('StartPercentage') if buy_order else band.get('StartPercentage')
            custom_end_price = band.get('CustomEndPrice')
            end_percent = -band.get('EndPercentage') if buy_order and not custom_end_price else band.get('EndPercentage')
            start_value = (1 + start_percent / 100) * base_price
            end_value = (1 + end_percent / 100) * base_price if not custom_end_price else custom_end_price
            cash_amount = band.get('CustomAccountBalance')
            no_of_orders = band.get('NoOfOrders')
            band_algorithm = band.get('BandAlgorithm')
            band_name = band.get('BandName')
            data = None
            if (buy_order and self.current_price < start_value and self.current_price > end_value) or (not buy_order and self.current_price > start_value and self.current_price < end_value):
                cash_amount_adjusted = round(cash_amount * abs(self.current_price - end_value) / abs(start_value - end_value), 8)
                no_of_orders_adjusted = round(no_of_orders * abs(self.current_price - end_value) / abs(start_value - end_value))
                data = {
                    'priceDifferenceRangeStart': band.get('PriceDifferenceRangeStart'),
                    'priceDifferenceRangeEnd': band.get('PriceDifferenceRangeEnd'),
                    'noOfOrders': no_of_orders_adjusted,
                    'cashAmount': cash_amount_adjusted,
                    'orderType': order_type,
                    'priceRangeStart': self.current_price,
                    'priceRangeEnd': end_value
                }
                if not buy_order:
                    data_buffer['noOfOrders'] += no_of_orders - no_of_orders_adjusted
                    data_buffer['cashAmount'] += cash_amount - cash_amount_adjusted
            elif (buy_order and self.current_price > end_value) or (not buy_order and self.current_price < end_value):
                if start_value == base_price and (buy_order and self.current_price > base_price) or (not buy_order and self.current_price < base_price):
                    start_value = self.current_price
                data = {
                    'priceDifferenceRangeStart': band.get('PriceDifferenceRangeStart'),
                    'priceDifferenceRangeEnd': band.get('PriceDifferenceRangeEnd'),
                    'noOfOrders': no_of_orders,
                    'cashAmount': cash_amount,
                    'orderType': order_type,
                    'priceRangeStart': start_value,
                    'priceRangeEnd': end_value
                }
            elif not buy_order:
                data_buffer['noOfOrders'] += no_of_orders
                data_buffer['cashAmount'] += cash_amount
            if data:
                order_list = get_bulk_order_list(data, band_algorithm)
                combined_order_list += order_list
                print(f'This is the original order list for {no_of_orders} {order_type} orders being placed for band {band_name} : {order_list}')
                print("""
                      ----------------------------------------------------------------------------------------------------    
                      """)
        if not buy_order:
            combined_order_list += get_bulk_order_list(data_buffer, band_algorithm)
        print(f'This is the order list with buffer for {order_type} orders : {combined_order_list}')
        print("""
              ----------------------------------------------------------------------------------------------------    
              """)
        # response = self.third_party_service.create_bulk_orders(combined_order_list)
        if buy_order:
            self.buy_orders_placed = combined_order_list 
        else:
            self.sell_orders_placed = combined_order_list
        return combined_order_list
