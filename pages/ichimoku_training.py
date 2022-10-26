import streamlit as st
from datetime import datetime, timedelta
from bybit_conn import get_data
from ichimoku import ichimoku
from etl import df_etl, separate_dataframe
from visuals import candle_stick
from html_ import card

# --- Page config --- 
st.set_page_config(layout="wide")
st.sidebar.image(r'logo2.png')
st.title('ICHIMOKU CLOUD ANALYSIS')
st.subheader('ByBit USDT Perpetual')

# --- Instanciate connection ---
data = get_data()

# --- SYMBOL ---
symbol = st.sidebar.selectbox('Symbol', data.get_symbols(), index=data.get_symbols().index('BTCUSDT'))

# --- TIMEFRAME ---
intervals     = ('1 min','3 min','5 min','15 min','30 min','1 h','2 h','4 h','6 h','12 h','1 d','1 w','1 m')
intervals_api = [1,3,5,15,30,60,120,240,360,720,"D","M","W"]
interval      = st.sidebar.selectbox('Interval', intervals)
interval_api  = intervals_api[intervals.index(interval)]

# --- DATE RANGE CONFIG ---
def delta(interval_api):
    if type(interval_api) == int:
        return interval_api
    else:
        raise Exception('not implemented yet')

_to    = datetime.now()                                  # Fecha final
_from  = _to - timedelta(minutes=delta(interval_api)*60) # Fecha inicial
_delta = datetime.now()-timedelta(minutes=300)           # Default number of rows

from_date = st.sidebar.date_input(label='Start Date',value=_from)
to_date   = st.sidebar.date_input(label='End Date',value=_to)
from_time = st.sidebar.time_input(label='Start Time', value=_delta)
to_time   = st.sidebar.time_input(label='End Time', value=datetime.now())

# --- GET DATA --- 
def load_data():
    historical = data.get_historical_klines(
        _from_date = from_date.strftime("%Y-%m-%d"),
        _from_time = from_time.strftime("%H:%M:%S"),
        symbol = symbol,
        interval = interval_api
        )
    return historical

# --- TRANSFORM AND FEATURE CREATION ---
df = df_etl(load_data())
#   ichi = ichimoku(df_etl(historical))
#   df = ichi.run()

# --- Time travel ---
select = st.slider('Time travel', min_value=df.index.min(), max_value=df.index.max(), value=(df.index.min(), round(df.index.max()/2)))
df=df[select[0]:select[1]]

ichi = ichimoku(df)
df = ichi.run()
dfs = separate_dataframe(df)

# --- METRICS ---
tk = df['tk_cross'][len(df)-28]
kh = df['kumo_ahead'][len(df)-2]
pk = df['price_vs_kumo'][len(df)-28]
pc = df['price_vs_chikou'][len(df)-28]
cross_distance = ichi.cross_distance()
cross_strenght = ichi.cross_strenght(cross_distance)

# --- HTML ---
def light(x):
    color = (0,0,0)
    if x > 0:
        color = (94,156,118)
    elif x < 0:
        color = (247,143,143)
    elif x == 0:
        color = (237,180,88)
    return color

# --- VISUALIZATION ---
col1, col2, col3 = st.columns([8.6,0.7,0.7])
with col1:
    fig = candle_stick(df,dfs)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header('Metrics')
    
    st.text('TK CROSS')
    card1 = card(tk,light(tk))  
    st.markdown(card1, unsafe_allow_html=True)
    
    st.text('KUMO')
    card2 = card(kh,light(kh))
    st.markdown(card2, unsafe_allow_html=True)

    st.text('$ VS KUMO')
    card3 = card(pk,light(pk))
    st.markdown(card3, unsafe_allow_html=True)

    st.text('$ VS CHIKOU')
    card4 = card(pc,light(pc))
    st.markdown(card4, unsafe_allow_html=True)

with col3:
    st.header('.')

    st.text('CROSS DIST.')
    card5 = card(cross_distance,(163,186,195))
    st.markdown(card5, unsafe_allow_html=True)

    st.text('CROSS STRONG')
    card5 = card(cross_strenght[0],light(cross_strenght[0]))
    st.markdown(card5, unsafe_allow_html=True)

    st.text('CROSS WEAK')
    card5 = card(cross_strenght[1],light(cross_strenght[1]))
    st.markdown(card5, unsafe_allow_html=True)


# --- Dataframe ---
check = st.checkbox("Display data", value=False)
if check:
    st.dataframe(df, use_container_width=True)

# --- Downlad data ---
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='ichimoku.csv',
    mime='text/csv',
)


