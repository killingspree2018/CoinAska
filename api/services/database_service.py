from settings import cursor, cnx
from datetime import datetime, timedelta

class DatabaseService:
    def __init__(self):
        self.bot_configurables = {}
        self.buy_price_bands = []
        self.sell_price_bands = []
        self.base_price = None
        self.get_bot_configurables()
        self.get_price_bands()
        self.get_moving_average()
        
    def get_bot_configurables(self):
        cursor.execute('Select * From BotConfigurables')
        parameters = cursor.fetchall()
        self.bot_configurabless = dict((parameter_name, parameter_value) for parameter_name, parameter_value in parameters)
        # print(self.bot_configurabless)

    def get_moving_average(self):
        moving_average_period = self.bot_configurabless.get('MovingAveragePeriod')
        custom_base_price = self.bot_configurabless.get('CustomBasePrice')
        if custom_base_price is None:
            no_of_values = int(moving_average_period * 12 * 24)
            query = f'Select * From CoinPriceTracker ORDER BY CurrentTime DESC LIMIT {no_of_values}'
            cursor.execute(query)
            rows = cursor.fetchall()
            prices = [row[0] for row in rows]
            # Calculate the average if enough data points are available
            if len(prices) >= moving_average_period * 24 * 12:  # Assuming 12 periods per hour (5 min intervals)
                self.base_price = round(sum(prices) / len(prices), int(8))
                print(f"Current {moving_average_period}-day moving average: {self.base_price}")
        else:
           self.base_price = custom_base_price

    def get_price_bands(self):
        cursor.execute('Select * From PriceBands Order By BandName')
        price_bands = cursor.fetchall()
        for id, type, band_name, start_percentage, end_percentage, custom_end_price, price_difference_start, band_algorith, price_difference_end, account_balance_percent, custom_account_balance, no_of_orders in price_bands:
            if type == 'Buy':
                self.buy_price_bands.append({'BandName': band_name, 'StartPercentage': start_percentage, 'EndPercentage': end_percentage, 'CustomEndPrice': custom_end_price, 'PriceDifferenceRangeStart': price_difference_start, 'PriceDifferenceRangeEnd': price_difference_end, 'BandAlgorith': band_algorith, 'AccountBalancePercentage': account_balance_percent, 'CustomAccountBalance': custom_account_balance, 'NoOfOrders': no_of_orders})
            else:
                self.sell_price_bands.append({'BandName': band_name, 'StartPercentage': start_percentage, 'EndPercentage': end_percentage, 'PriceDifferenceRangeStart': price_difference_start, 'PriceDifferenceRangeEnd': price_difference_end, 'BandAlgorith': band_algorith, 'AccountBalancePercentage': account_balance_percent, 'CustomAccountBalance': custom_account_balance, 'NoOfOrders': no_of_orders})
        # print(self.buy_price_bands)
        # print(self.sell_price_bands)
        
    def initialize_price_data():
        # Fetch the latest timestamp in the table
        cursor.execute("SELECT MAX(CurrentTime) FROM CoinPriceTracker")
        latest_time = cursor.fetchone()[0]
        # If there is no data in the table, set a start date
        if latest_time is None:
            latest_time = datetime.now() - timedelta(days=30)
        current_time = latest_time
        while current_time <= datetime.now():
            price = 0.00800000
            cursor.execute("INSERT INTO CoinPriceTracker (Price, CurrentTime) VALUES (%s, %s)", (price, current_time))
            current_time += timedelta(minutes=5)
        cnx.commit()

    def delete_price_data():
        cursor.execute("Delete FROM CoinPriceTracker")
        cnx.commit()

