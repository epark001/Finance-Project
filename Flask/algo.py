from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd

ts = TimeSeries(key='XP12DSLMVA2QP4MO', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='V',interval='15min', outputsize='full')
data['close'].plot()
print(data.describe())
plt.title('stock data stuff')
plt.show()