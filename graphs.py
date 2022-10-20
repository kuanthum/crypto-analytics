import plotly.graph_objects as go
import numpy as np

def candle_stick(df, dfs):

    fig = go.Figure()

    fig = go.Figure(
            data=[go.Candlestick(
                    x=df['date'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'])
                ],
            )

    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['close'].where(df['cross_signal'] == 1),
            mode='markers',
            marker_size=20,
            marker_color= np.select(
                [df["tk_cross"] > 0, df["tk_cross"] < 0], ["green", "red"], "rgba(0,0,0,0)"
            ),
            name='coso'
        )
    )

    cs = fig.data[0]

    # Set line and fill colors
    cs.increasing.fillcolor = '#4267b2'
    cs.increasing.line.color = '#4267b2'
    cs.decreasing.fillcolor = '#FF4136'
    cs.decreasing.line.color = '#FF4136'

    fig.update_traces(name='Price', showlegend = True)
    
    fig.update_layout(
        title='',
        margin=dict(l=10, r=30, t=30, b=10),
        plot_bgcolor="#e9ebee",
        paper_bgcolor="#e9ebee",
        autosize=True,
        height=600
        )

    fig.add_trace(
        go.Scatter(
            mode ='lines',
            x=df['date'],
            y=df["chikou"],
            line={'color':'#151515', 'width':0.5, 'dash':'dash'},
            name='Chikou',
            ))
    
    fig.add_trace(
        go.Scatter(
            mode = 'lines',
            x=df['date'],
            y=df["tenkan"],
            line={'color':'#5e9c76', 'width':2},
            name='Tenkan-sen'
            #1874CD
        ))

    fig.add_trace(
        go.Scatter(
            mode = 'lines',
            x=df['date'],
            y=df["kijun"],
            line={'color':'#c74343', 'width':2},
            name='Kijun-sen'
        ))

    fig.add_trace(
        go.Scatter(
            mode = 'lines',
            x=df['date'],
            y=df["senkou_a_ahead"],
            line={'color':'#5e9c76', 'width':1},
            name='Senkou Span A',
        ))

    fig.add_trace(
        go.Scatter(
            mode ='lines',
            x=df['date'],
            y=df["senkou_b_ahead"],
            line={'color':'red', 'width':1},
            name='Senkou Span B'
            ))

    #Reads senkou relation to plot green or red cloud
    def fillcol(label):
        if label == 1:
            return 'rgba(186,224,189,0.4)'
        elif label == 0:
            return 'rgba(247,143,143,0.4)'
    
    #Reads previusly splited dataframe for ploting cloud changes
    for df in dfs:
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y = df['senkou_a_ahead'],
                line = dict(color='rgba(0,0,0,0)'),
                showlegend=False
                ))

        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['senkou_b_ahead'],
                line = dict(color='rgba(0,0,0,0)'),
                showlegend=False,
                fill='tonexty',
                fillcolor=fillcol(df['colors'].iloc[0])
                ))
    
    # fig.add_trace(
    #         go.Candlestick(
    #             x=df['date'],
    #             open=df['open'],
    #             high=df['high'],
    #             low=df['low'],
    #             close=df['close']
    #         ))

    fig.update_xaxes(title_text="Date",
                    showline=True,
                    linewidth=3,
                    linecolor='#4267b2',
                    mirror=True,
                    showgrid=True, gridwidth=0.1, gridcolor='White'
                    )
    fig.update_yaxes(title_text="Price",
                    showline=True,
                    linewidth=3,
                    linecolor='#4267b2',
                    mirror=True,
                    showgrid=True, gridwidth=0.1, gridcolor='White'
                    )

    return fig
