from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as mticker
import sys
import base64
import numpy as np
import io
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline.offline
import pandas_datareader.data as web
from datetime import datetime

def symbols():
    s = pd.read_csv("symbols.csv")
    s.columns = ["Symbol"]
    return list(s.Symbol)

def candlestick2(stock):
    ts = TimeSeries(key='QBGZM8IV1P2X2VJQ', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=stock, interval='60min', outputsize='compact')
    
    df = web.get_data_yahoo('GOOGL')

    trace = go.Candlestick(x=df.index,
                           open=df.Open,
                           high=df.High,
                           low=df.Low,
                           close=df.Close,
                           increasing=dict(line=dict(color= '#17BECF')),
                           decreasing=dict(line=dict(color= '#7F7F7F')))
    data = [trace]
    plotly.offline.plot(data, filename='file.html')
    return None1

def candlestick1(stock):
    ts = TimeSeries(key='QBGZM8IV1P2X2VJQ', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=stock, interval='60min', outputsize='compact')
    
    fig, ax1 = plt.subplots()
    ax1.plot(data, 'b')
    ax1.set_xlabel('Time(s)')
    ax1.set_ylabel(stock.upper(), color='b')
    
    plt.title(
        'Stock Value of ' + stock.upper() )
    for tick in ax1.get_xticklabels():
        tick.set_rotation(45)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    fig.tight_layout()
    canvas.print_png(output)
    response = base64.b64encode(output.getvalue()).decode('ascii')
    return response

def candlestick(stock):
    ts = TimeSeries(key='QBGZM8IV1P2X2VJQ', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
    data['close'].plot()
    
    fig, ax1 = plt.subplots()
    ax1.plot(data, 'b')
    ax1.set_xlabel('Time(s)')
    ax1.set_ylabel(stock.upper(), color='b')
    
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    plt.title(
        'Stock Value of ' + stock.upper() )
    for tick in ax1.get_xticklabels():
        tick.set_rotation(90)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    fig.tight_layout()
    canvas.print_png(output)
    response = base64.b64encode(output.getvalue()).decode('ascii')
    return response