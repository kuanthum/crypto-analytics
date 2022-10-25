import pandas as pd
import json
from pybit import usdt_perpetual
from datetime import datetime, timedelta


class get_data():

    def __init__(self):

        '''
        All this code is for interact with bybit.
        Default endpoint is configurated to obtain data and trade in test-net,
        if you want the real thing you can change de credentials.json file.
        '''

        #API and Secret keys
        credentials_read = open('credentials.json')
        credentials      = json.load(credentials_read)
        self.endpoint = credentials['endpoint']
        self.api_key = credentials['api_key'],
        self.api_secret = credentials['api_secret']
        #Connection
        self.session = usdt_perpetual.HTTP(
                    endpoint=self.endpoint,
                    api_key=self.api_key,
                    api_secret=self.api_secret,
                    request_timeout= 100
                    )

    #get symbols list    
    def get_symbols(self) -> list:
        response = self.session.query_symbol()
        df = pd.DataFrame(response['result'])
        symbols = list(df['name'])
        return symbols
    
    #time convertion
    def from_time_format(self, minutes):
        now = datetime.now()
        from_time =  now - timedelta(minutes)
        from_time_unix = round(datetime.timestamp(from_time))
        return from_time_unix

    #query market data
    def query_kline(self, from_time, symbol='BTCUSDT', interval=1, limit=1000):
        response = self.session.query_kline(
            symbol=symbol,
            interval=interval,
            limit=limit,
            from_time=self.from_time_format(from_time),
        )
        df = pd.DataFrame(response['result'])
        return df
    
        #query market data
    def query_kline_raw(self, from_time, symbol='BTCUSDT', interval=1, limit=1000):
        response = self.session.query_kline(
            symbol=symbol,
            interval=interval,
            limit=limit,
            from_time=self.from_time_format(from_time),
        )
        result = response['result']
        return result
    
    #orders

if __name__ == '__main__':
    get_data()