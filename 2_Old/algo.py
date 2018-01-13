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

def stockchart(symbol1, length):
    if length == '1day':
        return stockchart_1day(symbol1)

    if length == '1week':
        return stockchart_1week(symbol1)

    if length == '4week':
        return stockchart_4week(symbol1)

    if length == '3month':
        return stockchart_3month(symbol1)

    if length == '1year':
        return stockchart_1year(symbol1)

    if length == '4year':
        return stockchart_5year(symbol1)
    else:
        return stockchart_1day(symbol1)

def candlestick2(stock):
    ts = TimeSeries(key='QBGZM8IV1P2X2VJQ', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=stock, interval='60min', outputsize='compact')
    
    import pandas_datareader as pdr
    df = web.get_data_yahoo('AAPL')


    trace = go.Candlestick(x=df.index,
                           open=df.Open,
                           high=df.High,
                           low=df.Low,
                           close=df.Close)
    data = [trace]
    layout = go.Layout(title='Candlestick Plot Testing', width=800, height=640)
    fig = go.Figure(data=data, layout=layout)

    py.image.save_as(fig, filename='candle_testing.png')
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

def graph(stock, data, title):
    
    data.drop(['volume'], axis=1, inplace=True)
    data.drop(['open'], axis=1, inplace=True)
    data.drop(['high'], axis=1, inplace=True)
    data.drop(['low'], axis=1, inplace=True)
    
    fig, ax1 = plt.subplots()
    ax1.plot(data, 'b')
    ax1.set_xlabel('Time(s)')
    ax1.set_ylabel(stock.upper(), color='b')

        

    
    if title == '24 Hours':
        n = 3
        for index, label in enumerate(ax1.xaxis.get_ticklabels()):
            if index % n != 0:
                label.set_visible(False)
        plt.title(
            'Stock Value of ' + stock.upper() + ' for 1 Day')
    if title == '1 Week':
        n = 3
        for index, label in enumerate(ax1.xaxis.get_ticklabels()):
            if index % n != 0:
                label.set_visible(False)
        plt.title(
            'Stock Value of ' + stock.upper() + ' for 5 Days')
    if title == '4 Weeks':
        n = 2
        for index, label in enumerate(ax1.xaxis.get_ticklabels()):
            if index % n != 0:
                label.set_visible(False)
        plt.title(
            'Stock Value of ' + stock.upper() + ' for 10 Days')
    if title == '3 Months':
        n = 3
        for index, label in enumerate(ax1.xaxis.get_ticklabels()):
            if index % n != 0:
                label.set_visible(False)
        plt.title(
            'Stock Value of ' + stock.upper() + ' for 5 Months')
    if title == '1 Year':
        n = 26
        for index, label in enumerate(ax1.xaxis.get_ticklabels()):
            if index % n != 0:
                label.set_visible(False)
        plt.title(
            'Stock Value of ' + stock.upper() + ' for 2 Years')
    if title == '4 Years':
        n = 3
        for index, label in enumerate(ax1.xaxis.get_ticklabels()):
            if index % n != 0:
                label.set_visible(False)
        plt.title(
            'Stock Value of ' + stock.upper() + ' for ' + title)
    for tick in ax1.get_xticklabels():
        tick.set_rotation(90)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    fig.tight_layout()
    canvas.print_png(output)
    response = base64.b64encode(output.getvalue()).decode('ascii')
    return response
















def stockchart_1day(symbol):
    title = '1 Day'
    ts = TimeSeries(key='QBGZM8IV1P2X2VJQ', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol, interval='5min', outputsize='compact')
    return graph(symbol, data, '24 Hours')



def stockchart_1week(symbol):
    title = '1 Week'
    ts = TimeSeries(key='QBGZM8IV1P2X2VJQ', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol, interval='30min', outputsize='compact')
    return graph(symbol, data, title)



def stockchart_4week(symbol):

    title = '4 Weeks'
    ts = TimeSeries(key='QBGZM8IV1P2X2VJQ', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol, interval='60min', outputsize='compact')

    return graph(symbol, data, title)



def stockchart_3month(symbol1):
    
    title = '3 Months'
    ts = TimeSeries(key='QBGZM8IV1P2X2VJQ', output_format='pandas')
    data1, meta_data = ts.get_daily(symbol=symbol1, outputsize='compact')

    return graph(symbol1, data1, title)


def stockchart_1year(symbol1):
    title = '1 Year'
    ts = TimeSeries(key='QBGZM8IV1P2X2VJQ', output_format='pandas')
    data1, meta_data = ts.get_daily(symbol=symbol1, outputsize='full')

    return graph(symbol1, data1, title)


def stockchart_5year(symbol1):
    title = '4 Years'
    ts = TimeSeries(key='QBGZM8IV1P2X2VJQ', output_format='pandas')
    data1, meta_data = ts.get_monthly(symbol=symbol1)

    return graph(symbol1, data1, title)