import pandas as pd
import numpy as np

class ichimoku():
    
    '''
    This is ichimoku cloud implemantation.
    For more information about how this work you can read Readme.md file.
    '''

    def __init__(self,df, lookback=9):
        self.df         = df
        self.close      = df['close']
        self.high       = df['high']
        self.low        = df['low']
        self.last_price = float(self.close.iloc[-1])

        self.lookback = lookback
        self.l2=(lookback*3)-1
        self.l3=self.l2*2
        self.last_candle = len(df)

    #Convertion line
    def tenkan_sen(self, counter=0):
        thigh = float(self.high[(-self.lookback)-counter:(self.last_candle)-counter].max())
        tlow  = float(self.low[(-self.lookback)-counter:(self.last_candle)-counter].min())
        tenkan_sen = (thigh+tlow)/2
        return tenkan_sen

    #Base line
    def kijun_sen(self,counter=0):
        khigh = float(self.high[(-self.l2)-counter:(self.last_candle)-counter].max())
        klow  = float(self.low[(-self.l2)-counter:(self.last_candle)-counter].min())
        kijun_sen = (khigh+klow)/2
        return kijun_sen

    #Kumo Cloud
    def senkou_span_a(self,counter=0):
        senkou_span_a = ((self.tenkan_sen(counter))+(self.kijun_sen(counter)))/2
        return senkou_span_a

    def senkou_span_b(self,counter=0):
        senkou_span_b_high = float(self.high[-self.l3-counter:self.last_candle-counter].max())
        senkou_span_b_low  = float(self.low[-self.l3-counter:self.last_candle-counter].min())
        senkou_span_b = (senkou_span_b_high+senkou_span_b_low)/2
        return senkou_span_b

    #Chikou is just close price displaced so it will be present in move_indicators function

    #Generates the columns with indicators values
    def iterator(self):
        indicators = [self.tenkan_sen,self.kijun_sen,self.senkou_span_a,self.senkou_span_b]
        index = 0
        for indicator in indicators:
            c = 0
            values = []
            for e in range(0,len(self.df)):
                values.append(indicator(c))
                c +=1
            for i in range(len(self.df)-len(values)):
                values.append(None)
            values.reverse()
            self.df[f'indicator{index}'] = values
            index += 1
        return self.df

    #Generate new dates for ichimoku forecast (kumo cloud ahead)
    def add_forecast(self):
        date = []
        for i in range(0,self.l2+1):
            delta = self.df['date'][len(self.df)-1] - self.df['date'][len(self.df)-2] #Restar dos fechas para infereir intervalo
            new_date = self.df['date'][len(self.df)-1]+delta*i #Sumar de manera iterativa el intervalo de tiempo
            date.append(new_date)
        
        df_copy = pd.DataFrame().reindex(columns=self.df.columns)
        df_copy['date'] = pd.Series(date)
        self.df = pd.concat([self.df,df_copy],axis=0, ignore_index=True)
        return self.df    

    #This is a litle bit harcoded, it moves senoku spans fordward in time
    def move_indicators(self):
        chikou   = list(self.df['close'][26:])
        senkou_a = list(self.df['indicator2'][:-26])
        senkou_b = list(self.df['indicator3'][:-26])
        fill_nan = list(np.full(26, None))
        senkou_a_displaced = fill_nan+senkou_a
        senkou_b_displaced = fill_nan+senkou_b
        chikou_displaced   = chikou+fill_nan
        #We are holding indicators2 and 3 columns beacuse it will be usefull for analizing price vs cloud
        #Both are evaluated, kumo vs price and color of kumo ahead
        self.df['senkou_a_ahead'] = senkou_a_displaced
        self.df['senkou_b_ahead'] = senkou_b_displaced
        self.df['chikou'] = chikou_displaced
        return self.df

    ''' ANALITICS '''
    #Creates a new column with tk_cross value
    #1 for uptrend -1 for downtrend 0 if there are equals
    def tk_cross(self):
        result = list(map(lambda x, y: 1 if x > y else(-1 if x < y else 0),self.df['indicator0'],self.df['indicator1']))
        self.df['tk_cross'] = result
        return self.df

    #Evals if forecasted cloud is red or green 
    def kumo_ahead(self):
        result = list(map(lambda x, y: 1 if x > y else(-1 if x < y else 0),self.df['senkou_a_ahead'],self.df['senkou_b_ahead']))
        self.df['kumo_ahead'] = result
        return self.df

    def price_vs_kumo(self):
        self.df['price_vs_kumo'] = list(np.full(len(self.df), 0))
        for i in range(len(self.df)):
            if self.df['senkou_a_ahead'][i] > self.df['senkou_b_ahead'][i]:
                if self.df['close'][i] > self.df['senkou_a_ahead'][i]:
                    self.df['price_vs_kumo'][i] = 1
                elif self.df['close'][i] > self.df['senkou_b_ahead'][i]:
                    self.df['price_vs_kumo'][i] = -1
                else:
                    self.df['price_vs_kumo'][i] = 0
            elif self.df['close'][i] < self.df['senkou_a_ahead'][i]:
                self.df['price_vs_kumo'][i] = -1
            elif self.df['close'][i] > self.df['senkou_b_ahead'][i]:
                self.df['price_vs_kumo'][i] = 1
            else:
                self.df['price_vs_kumo'][i] = 0

    def price_vs_chikou(self):
        result = list(map(lambda x, y: 1 if x > y else (-1 if x < y else (0 if x == y else None)),self.df['chikou'],self.df['close']))
        fill_nan = list(np.full(26, None))   
        self.df['price_vs_chikou'] = fill_nan+result[:-26]
        self.df['price_vs_chikou'] = self.df['price_vs_chikou'].astype('Int64')
        return self.df

    def cross_distance(self):
        last_value = len(self.df)-28
        tk = self.df['tk_cross'][last_value]
        change = tk
        counter = 0
        while tk == change:
            tk = self.df['tk_cross'][last_value-counter]
            counter = counter + 1
            if counter > len(self.df):
                break
        return counter

    def cross_strenght(self,distance):
        dist = -distance-28
        print(dist)
        price_on_cross = self.df['close'].iloc[dist]
        tenkan = self.df['indicator0'].iloc[dist] #tenkan
        kijun = self.df['indicator1'].iloc[dist]  #kijun
        if price_on_cross > tenkan and price_on_cross > kijun:
            return -1
        elif price_on_cross < tenkan and price_on_cross < kijun:
            return 1
        else:
            return 0

if __name__ == '__main__':
    ichimoku()