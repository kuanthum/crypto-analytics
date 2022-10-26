import streamlit as st
from datetime import datetime, timedelta
from bybit_conn_2 import get_data


#Page config
st.set_page_config(layout="wide")
st.sidebar.image(r'logo2.png')
st.title('ICHIMOKU CLOUD ANALYSIS')

#Instanciate connection
data = get_data()

#SYMBOL
symbol = st.sidebar.selectbox('Symbol', data.get_symbols(), index=data.get_symbols().index('BTCUSDT'))

#TIMEFRAME
intervals = ('1 min','3 min','5 min','15 min','30 min','1 h','2 h','4 h','6 h','12 h','1 d','1 w','1 m')
intervals_api = [1,3,5,15,30,60,120,240,360,720,"D","M","W"]
interval = st.sidebar.selectbox('Interval', intervals)
interval_api = intervals_api[intervals.index(interval)]

#DATE RANGE CONFIG
def delta(interval_api):
    if type(interval_api) == int:
        return interval_api
    else:
        raise Exception('not implemented yet')

_to   = datetime.now()
_from = _to - timedelta(minutes=interval_api*60)
_delta = datetime.now()-timedelta(minutes=30)

from_date = st.sidebar.date_input(label='Start Date',value=_from)
to_date   = st.sidebar.date_input(label='End Date',value=_to)
from_time = st.sidebar.time_input(label='Start Time', value=_delta)
to_time   = st.sidebar.time_input(label='End Time', value=datetime.now())
#GET DATA
historical = data.get_historical_klines(
    _from_date = from_date.strftime("%Y-%m-%d"),
    _from_time = from_time.strftime("%H:%M:%S"),
    symbol = symbol,
    interval = interval_api
    )

#VISUALIZATION
st.dataframe(historical)    

