from api.services.database_service import DatabaseService
from api.services.order_service import get_bulk_order_list
from api.services.third_party_service import ThirdPartyService

class MarketMakingBotService:
    def __init__(self, current_price):
        self.database_obj = DatabaseService()
        self.current_price = current_price
        
    def start_processing(self):
        # get buy band in which current price of the stock lies
        buy_bands = self.get_price_band('BUY')
        self.place_orders(buy_bands, 'BUY')
        sell_bands = self.get_price_band('SELL')
        self.place_orders(sell_bands, 'SELL')

    def get_price_band(self, order_type):
        base_price = self.database_obj.base_price
        eligible_bands = []
        buy_order = order_type == 'BUY'
        price_band_list = self.database_obj.buy_price_bands if buy_order else self.database_obj.sell_price_bands
        for band in price_band_list:
            # start_percent = band.get('StartPercentage')
            end_percent = band.get('EndPercentage')
            custom_end_price = band.get('CustomEndPrice')
            # start_value = (1 + start_percent / 100) * base_price
            end_value = (1 + end_percent / 100) * base_price if not custom_end_price else custom_end_price
            if (buy_order and self.current_price > end_value) or (not buy_order and self.current_price < end_value):
                eligible_bands.append(band)
        return eligible_bands

    def place_orders(self, bands, order_type):
        buy_order = order_type == 'BUY'
        base_price = self.database_obj.base_price
        combined_order_list = []
        for band in bands:
            start_percent = band.get('StartPercentage')
            end_percent = band.get('EndPercentage')
            custom_end_price = band.get('CustomEndPrice')
            start_value = (1 + start_percent / 100) * base_price
            end_value = (1 + end_percent / 100) * base_price if not custom_end_price else custom_end_price
            cash_amount = band.get('CustomAccountBalance')
            no_of_orders = band.get('NoOfOrders')
            band_algorithm = band.get('BandAlgorithm')
            band_name = band.get('BandName')
            if (buy_order and self.current_price > start_value) or (not buy_order and self.current_price < start_value):
                cash_amount_adjusted = cash_amount * abs(self.current_price - end_value)/abs(start_value - end_value)
                no_of_orders_adjusted = no_of_orders * abs(self.current_price - end_value)/abs(start_value - end_value)
                data = {
                    'priceDifferenceRangeStart': band.get('PriceDifferenceRangeStart'),
                    'priceDifferenceRangeEnd': band.get('PriceDifferenceRangeEnd'),
                    'noOfOrders': no_of_orders_adjusted,
                    'cashAmount': cash_amount_adjusted,
                    'orderType': order_type,
                    'priceRangeStart': self.current_price,
                    'priceRangeEnd': end_value
                }
            else:
                data = {
                    'priceDifferenceRangeStart': band.get('PriceDifferenceRangeStart'),
                    'priceDifferenceRangeEnd': band.get('PriceDifferenceRangeEnd'),
                    'noOfOrders': no_of_orders,
                    'cashAmount': cash_amount,
                    'orderType': order_type,
                    'priceRangeStart': start_value,
                    'priceRangeEnd': end_value
                }
            orders_list = get_bulk_order_list(data, band_algorithm)
            combined_order_list += orders_list
            print(f'This is the order list for {no_of_orders} {order_type} orders being placed for band {band_name} : {orders_list}')
        # third_party_service = ThirdPartyService()
        # response = third_party_service.create_bulk_orders(combined_order_list)
        return combined_order_list
