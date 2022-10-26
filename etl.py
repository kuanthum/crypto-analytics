import pandas as pd
from datetime import datetime

'''
This module contains functions for cleaning and transform data
'''
#Convert unixtime to date and drop unnecesary columns
def df_etl(df):
    date = [datetime.fromtimestamp(i) for i in df['start_at']]
    df['date'] = date
    df.drop(columns=['id','interval','period','open_time','start_at', 'symbol'], inplace = True)
    return df

#Encodes de color for ichimoku cloud
def cloud_color_encoding(df):
    colors = []
    for row in range(0,len(df)):
        if df['senkou_a_ahead'][row] > df['senkou_b_ahead'][row]:
            color = 1
        else:
            color = 0
        colors.append(color)
    return colors

#Splits dataframe so ichimoku cloud can be ploted
def separate_dataframe(df):
    dfs = []
    df['group'] = df['colors'].ne(df['colors'].shift()).cumsum()
    df = df.groupby('group')
    for name, data in df:
        dfs.append(data)
    return dfs
