import pandas as pd
import json
import time
from pybit import usdt_perpetual
from datetime import datetime, timedelta
from functools import reduce

class get_data():

    def __init__(self):

        '''
        All this code is for interact with bybit.
        Default endpoint is configurated to obtain data and trade in test-net,
        if you want the real thing you can change de credentials.json file.
        '''

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
    def format_date_unix(self, date, time):
        date = str(date)
        time = str(time)
        formated_date = datetime.strptime(date+' '+time,"%Y-%m-%d %H:%M:%S")
        unix_timestamp = round(datetime.timestamp(formated_date))
        return unix_timestamp

    #query market data
    def query_kline_raw(self, from_time, symbol='BTCUSDT', interval=1, limit=200):
        response = self.session.query_kline(
            symbol=symbol,
            interval=interval,
            limit=limit,
            from_time=from_time,
        )
        result = response['result']
        return result

    #    
    def get_historical_klines(self,
                            _from_date,
                            _from_time,
                            _to_date=None,
                            _to_time=None,
                            symbol='BTCUSDT',
                            interval=1
                            ):

        """ Dado que solo podemos traer 200 registros como máximo, esta funcion nos permitirá aumentar esa cantidad
            iterando varias request.

            Args:
                _from (str): date+time 
                _to   (str): date+time
            
            Returns:
                df: dataframe
        """
        
        from_time = self.format_date_unix(_from_date,_from_time)

        # Si no se indica fecha se tomara desde _from hasta ahora.
        if _to_date == None: 
            to_time = round(datetime.timestamp(datetime.now())) #unixtime now
        else:
            to_time = self.format_date_unix(_to_date,_to_time) #unixtime indicated
        
        output_data = []
        idx = 0

        while True:
            temp_dict = self.query_kline_raw(symbol=symbol, from_time=from_time, interval=interval)
            temp_data = [list(i.values()) for i in temp_dict]
            output_data.append(temp_data)
            #print(temp_data[len(temp_data)-1][4])
            print(len(temp_data))
            last_reg = temp_data[len(temp_data)-1]
            print(last_reg)
            last_date = last_reg[4]
            print(last_date)
            #last_date = temp_data[len(temp_data)-1][4]
            from_time = last_date + interval*60
            print(from_time)
            idx += 1

            # check if we received less than the required limit and exit the loop
            # otherwise temp_data len will be 0
            if len(temp_data) < 200:
            #    # exit the while loop
                break

            if last_date == to_time:
                break

            # sleep after every 3rd call to be kind to the API
            if idx % 3 == 0:
                print('being kind to the api')
                time.sleep(0.2)
                print(idx)
                print(last_date, to_time)

            # convert to data frame
        
        #unpack nested list [[[][][]]] to [[][][]] otherwise cant convert to dataframe
        output_data = reduce(lambda x, y: x+y, output_data)
        print(output_data)

        df = pd.DataFrame(output_data, columns=['id','symbol','interval','period','open_time','start_at', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
        df['date'] = [datetime.fromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S')[:-3] for i in df['open_time']]
        return df

    #orders 

if __name__ == '__main__':
    get_data()