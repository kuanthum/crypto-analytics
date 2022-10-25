import pandas as pd
import numpy as np

class ichimoku():
    
    '''
    This is ichimoku cloud implemantation.
    For more information about how this work you can read Readme.md file.
    The complexity of coding ichimoku indicators is that there are some parts of it
    that must be displaced. But, in general, indicators aren't that dificult to understand
    given that they follow the logic of simple ones like EMA´s etc.
    I tried to make the code all verbose as posible on porpouse, for understanding and easy bugs tracking
    '''

    def __init__(self,df, lookback=9):
        '''
        For default Ichimoku is calculated taken 9 candles displacement as base.
        Is recomended to double this number if you are trading crypto
        '''

        self.df         = df
        self.close      = df['close']
        self.high       = df['high']
        self.low        = df['low']
        self.last_price = float(self.close.iloc[-1])
        self.lookback   = lookback
        self.l2         =(lookback*3)-1
        self.l3         =self.l2*2
        self.last_candle= len(df)

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
        indicator_name = ['tenkan','kijun','senkou_span_a','senkou_span_b']
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
            self.df[f'{indicator_name[index]}'] = values
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
        senkou_a = list(self.df['senkou_span_a'][:-26])
        senkou_b = list(self.df['senkou_span_b'][:-26])
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
        result = list(map(lambda x, y: 1 if x > y else(-1 if x < y else 0),self.df['tenkan'],self.df['kijun']))
        self.df['tk_cross'] = result
        return self.df

    #Evals if forecasted cloud is red or green 
    def kumo_ahead(self):
        result = list(map(lambda x, y: 1 if x > y else(-1 if x < y else 0),self.df['senkou_a_ahead'],self.df['senkou_b_ahead']))
        self.df['kumo_ahead'] = result
        return self.df

    def price_vs_kumo(self):
        #The complexity of this function is given by the fact that the price can be
        #abobe the cloud, below the cloud, in the middle.
        #but the cloud is form by two indicators, so you must eval those indicators position to

        self.df['price_vs_kumo'] = list(np.full(len(self.df), 0))
        for i in range(len(self.df)):
            if self.df['senkou_a_ahead'][i] > self.df['senkou_b_ahead'][i]:
                if self.df['close'][i] > self.df['senkou_a_ahead'][i]:
                    self.df['price_vs_kumo'][i] = 1
                elif self.df['close'][i] > self.df['senkou_b_ahead'][i]:
                    self.df['price_vs_kumo'][i] = 0
                else:
                    self.df['price_vs_kumo'][i] = -1
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

    #cross distance directo
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

    # return tail of tk cross beacause is not posible to eval distance to previous cross
    def tk_tail(self):
        c = 0
        tk = self.df['tk_cross'][c]
        change = tk
        while tk == change:
            tk = self.df['tk_cross'][c]
            c += 1
            if c > len(self.df):
                break
        return c-2

    # Appends cross distance to every row of the dataframe
    def cross_distance_list(self):
        tail = self.tk_tail()
        values = []
        c = 0
        #for i in self.df.index:
        for i in range(0,(len(self.df)-28-tail)):
            last_value = len(self.df)-28-c                      #take index 
            tk = self.df['tk_cross'][last_value]                #take tk value for index
            change = tk                                         
            counter = 0
            while tk == change:                                 #if tk value doesnt change, repeat
                tk = self.df['tk_cross'][last_value-counter]    #tk = tk value from previous register
                counter = counter + 1                   
                if counter > len(self.df):
                    break
            c += 1
            values.append(counter)

        fill_nan = list(np.full(tail, -1))
        fill_nan_2 = list(np.full(28, -1))
        values.reverse()
        values = fill_nan+values
        
        self.df['cross_distance'] = values+fill_nan_2
        self.df['cross_distance'] = self.df['cross_distance'].astype('Int64')
        return self.df

    #tk strenght directo
    def cross_strenght(self,distance):
        dist = -distance-28
        price_on_cross = self.df['close'].iloc[dist]
        tenkan = self.df['tenkan'].iloc[dist] #tenkan
        kijun = self.df['kijun'].iloc[dist]  #kijun
        if price_on_cross > tenkan and price_on_cross > kijun:
            return [1,-1] #strong long weak short
        elif price_on_cross < tenkan and price_on_cross < kijun:
            return [-1,1] #strong short weak long
        else: 
            return [0,0] #undefined
    
    # Identify where the tk cross was done
    def cross_signal(self):
        result = list(map(lambda x: 1 if x == 3 else (0 if x == -1 else None), self.df['cross_distance']))
        self.df['cross_signal'] = result
        self.df['cross_signal'] = self.df['cross_signal'].astype('Int64')
        return self.df
        
    #Append tk cross strenght for every value in df
    def cross_strenght_2(self):
        search = self.df['cross_signal'].where(self.df['cross_signal'] == 1)
        index = search.dropna()
        prices = []
        for i in index.index:
            price_on_cross = self.df['close'][i]
            tenkan = self.df['tenkan'][i]
            kijun = self.df['kijun'][i]
            if price_on_cross > tenkan and price_on_cross > kijun:
                prices.append([i,1,-1]) #Strong long weak short
            elif price_on_cross < tenkan and price_on_cross < kijun:
                prices.append([i,-1,1]) #Strong short weak long
            else:
                prices.append([i,0,0])  #Unefined

        self.df['strong'] = np.full(len(self.df), None)
        self.df['weak']   = np.full(len(self.df), None)
        for i in prices:
            self.df['strong'][i[0]] = i[1]
            self.df['weak'][i[0]] = i[2]

        return self.df
    
if __name__ == '__main__':
    ichimoku()