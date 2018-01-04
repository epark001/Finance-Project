from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
import base64
import numpy as np
import io
import pandas as pd


def symbols():
    s = pd.read_csv("symbols.csv")
    s.columns = ["Symbol"]
    return list(s.Symbol)

def candlestick(stock):
    ts = TimeSeries(key='QBGZM8IV1P2X2VJQ', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=stock, interval='60min', outputsize='compact')
    
    fig, ax1 = plt.subplots()
    ax1.plot(data, 'b')
    ax1.set_xlabel('Time(s)')
    ax1.set_ylabel(stock.upper(), color='b')

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