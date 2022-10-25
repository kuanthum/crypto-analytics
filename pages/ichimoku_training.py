import streamlit as st
from bybit_conn_2 import get_data

#Page config
st.set_page_config(layout="wide")
st.sidebar.image(r'logo2.png')
st.title('ICHIMOKU CLOUD ANALYSIS')

#Instanciate connection
data = get_data()

#Get symbols tradable
symbol = st.sidebar.selectbox('Symbol', data.get_symbols(), index=data.get_symbols().index('BTCUSDT'))

#Select interval
intervals = ('1 min','3 min','5 min','15 min','30 min','1 h','2 h','4 h','6 h','12 h','1 d','1 w', '1 m')
interval = st.sidebar.selectbox('Interval', intervals)


#Get market data
# @st.cache
# def load_data():
#     df = data.query_kline(from_time=100)
#     return df

df = data.query_kline(from_time=300)
st.dataframe(df)

raw = data.query_kline_raw(from_time=300)
st.text(len(raw))
