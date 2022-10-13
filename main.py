import pandas as pd
import json
from pybit import usdt_perpetual
from datetime import datetime, timedelta


class df():

    def __init__(self,symbol:str = 'BTCUSDT',interval:int = 1,limit:int = 1000,from_time:int = 30):

        '''
        All this code is for interact with bybit.
        Default endpoint is configurated to obtain data and trade in test-net,
        if you want the real thing you can change de credentials.json file.
        '''

        #API and Secret keys
        credentials_read = open('credentials.json')
        credentials      = json.load(credentials_read)

        self.symbol = symbol
        self.interval = interval
        self.limit = limit
        self.from_time = from_time
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
    def from_time_format(self):
        now = datetime.now()
        from_time =  now - timedelta(minutes=self.from_time)
        from_time_unix = round(datetime.timestamp(from_time))
        return from_time_unix

    #query market data
    def query_kline(self):
        response = self.session.query_kline(
            symbol=self.symbol,
            interval=self.interval,
            limit=self.limit,
            from_time=self.from_time_format(),
        )
        df = pd.DataFrame(response['result'])
        return df
    
    #orders

if __name__ == '__main__':
    df()