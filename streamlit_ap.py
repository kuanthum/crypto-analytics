
import streamlit as st
from main import df
from etl import df_etl, cloud_color_encoding, separate_dataframe
from graphs import candle_stick
from ichimoku import ichimoku

from html_ import card, card_2

st.set_page_config(layout="wide")
st.sidebar.image(r'logo2.png')
st.title('ICHIMOKU CLOUD ANALYSIS')


data = df()


# --- Config ---
col1,col3, col4 = st.columns(3)
with col1:
    st.subheader('ByBit USDT Perpetual')

symbol = st.sidebar.selectbox('Symbol', data.get_symbols(), index=data.get_symbols().index('BTCUSDT'))  

intervals = ['1 min','3 min','5 min','15 min','30 min','1 h','2 h','4 h','6 h','12 h','1 d','1 w', '1 m']
interval = st.sidebar.selectbox('Interval', intervals)

#Intervals and from_time
min_range, h_range = range(0,5), range(5,10)
if intervals.index(interval) in min_range:
    t_delta = 'minutes'
elif intervals.index(interval) in h_range :
    t_delta = 'hours'
elif intervals.index(interval) == 10:
    t_delta = 'days'
elif intervals.index(interval) == 11:
    t_delta = 'weeks'
elif intervals.index(interval) == 12:
    t_delta = 'months'

from_time = st.sidebar.slider(f'Number of records in {t_delta}', min_value=1, value=100, max_value=1000)


# --- DATA ---
def load_data():
    data.symbol = symbol
    intervals_api = [1,3,5,15,30,60,120,240,360,720,"D","M","W"]
    data.interval = intervals_api[intervals.index(interval)]
    data.from_time = 226
    market = data.query_kline()
    data.limit = 226
    return market
df = df_etl(load_data())

with col3:
    st.metric(label = "From",
              value = f"{df['date'].min()}")
with col4:
    st.metric(label ="To",
              value = f"{df['date'].max()}") 
#Limit
#limit = st.sidebar.number_input('limit', min_value=50, value=1000, step=50)

#eliminar registros futuros
select = st.slider('Time travel', min_value=df.index.min(), max_value=df.index.max(),value=(df.index.min(),round(df.index.max()/2)))

df=df[select[0]:select[1]]
ichi = ichimoku(df)
ichi.iterator()
ichi.add_forecast()

# --- VISUALS ----

graph = ichi.move_indicators()

ichi.tk_cross()
ichi.kumo_ahead()
ichi.price_vs_kumo()
ichi.price_vs_chikou()

# --- ICHIMOKU METRICS ---
tk = ichi.df['tk_cross'][len(ichi.df)-28]
kh = ichi.df['kumo_ahead'][len(ichi.df)-2]
pk = ichi.df['price_vs_kumo'][len(ichi.df)-28]
pc = ichi.df['price_vs_chikou'][len(ichi.df)-28]
cross_distance = ichi.cross_distance()
cross_strenght = ichi.cross_strenght(cross_distance)
ichi.cross_distance_list()
ichi.cross_signal()
df = ichi.cross_strenght_2()


graph['colors'] = cloud_color_encoding(graph)
dfs = separate_dataframe(graph)
fig = candle_stick(graph,dfs)

col1, col2, col3 = st.columns([8,1,1])
with col1:
    st.plotly_chart(fig, use_container_width=True)

def light(x):
    color = (0,0,0)
    if x > 0:
        color = (94,156,118)
    elif x < 0:
        color = (247,143,143)
    elif x == 0:
        color = (237,180,88)
    return color

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




