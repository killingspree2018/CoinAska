from api.services.database_service import DatabaseService
from api.services.order_service import get_bulk_order_list
from api.services.third_party_service import ThirdPartyService

class MarketMakingBotService:
    def __init__(self, current_price):
        self.database_obj = DatabaseService()
        self.current_price = current_price
        
    def start_processing(self):
        # get buy band in which current price of the stock lies
        self.place_orders(self.database_obj.buy_price_bands, 'BUY')
        self.place_orders(self.database_obj.sell_price_bands, 'SELL')

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
        # third_party_service = ThirdPartyService()
        # response = third_party_service.create_bulk_orders(combined_order_list)
        return combined_order_list
