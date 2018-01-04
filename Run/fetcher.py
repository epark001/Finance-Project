from alpha_vantage.timeseries import TimeSeries
from key import KEY
import pandas as pd

def fetch_symbol(symbol):
	ts = TimeSeries(key=KEY, output_format='pandas')
	data, meta_data = ts.get_daily(symbol=symbol, outputsize="full")
	dates = []
	prices = []
	for i in data['close']:
		dates.append(i)
	for i in data['close'].keys():
		prices.append(i)
	return pd.DataFrame(dates, prices, columns=["prices"])
