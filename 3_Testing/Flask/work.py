from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import sys

def stockchart(symbol):
    ts = TimeSeries(key='QBGZM8IV1P2X2VJQ', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol,interval='1min', outputsize='full')
    data2, meta_data = ts.get_intraday(symbol='aapl',interval='1min', outputsize='full')
    print(data)
    print(data2)
    fig, ax1 = plt.subplots()
    ax1.plot(data)
    plt.title('Stock chart')
    plt.show()

stockchart('abc')
