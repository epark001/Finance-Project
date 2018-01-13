from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
app = Flask(__name__) 
app.config.from_object(__name__) 
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.kernel_ridge import KernelRidge
from sklearn import linear_model
from datetime import datetime
TOTAL = 30

def get_data(symbol):
	ts = TimeSeries(key="1WWS9XXK956Y1EIJ", output_format='pandas')
	data, meta_data = ts.get_daily(symbol=symbol, outputsize="full")
	dates = []
	prices = []
	for i in data['close']:
		dates.append(i)
	for i in data['close'].keys():
		prices.append(i)
	return pd.DataFrame(dates, prices, columns=["prices"])

def predict(symbol, days):
	global TOTAL
	TOTAL = 30
	close_data_df = get_data(symbol)

	dates = list(close_data_df.axes[0])
	date_indexes = list(range(len(dates)))

	actual_price = close_data_df.prices
	if len(date_indexes) > TOTAL:
		date_indexes = list(range(TOTAL))
		actual_price = actual_price[-1 * TOTAL:]
	TOTAL = len(actual_price)

	date_indexes = np.reshape(date_indexes,(len(date_indexes), 1))

	svr_rbf = SVR(kernel= 'rbf', C=1e3, gamma=0.1, epsilon=0.001)
	kr = GridSearchCV(KernelRidge(kernel='rbf', gamma=0.1),
                  param_grid={"alpha": [1e0, 1e-1, 1e-2, 1e-3],
                              "gamma": np.logspace(-2, 2, 5)})

	linear_mod = linear_model.LinearRegression()
	
	svr_rbf.fit(date_indexes, actual_price) 
	kr.fit(date_indexes, actual_price)

	svr_rbf_predict = svr_rbf.predict(date_indexes)
	kr_predict = kr.predict(date_indexes)
	
	svr_rbf_predict_values = []
	kr_predict_values = []
	avg_predict_values = []

	for i in range(len(date_indexes)):
		svr_rbf_predict_values.append(svr_rbf_predict[i])
		kr_predict_values.append(kr_predict[i])
		avg_predict_values.append((svr_rbf_predict[i] + kr_predict[i]) / 2)
	
	date_indexes = list(range(TOTAL))
	for i in range(days):
		date_indexes.append(TOTAL + i)
		svr_rbf_predict_values.append(svr_rbf.predict(TOTAL + i)[0])
		kr_predict_values.append(kr.predict(TOTAL + i)[0])
		avg_predict_values.append((svr_rbf.predict(TOTAL + i)[0] + kr.predict(TOTAL + i)[0]) / 2)
	return date_indexes, actual_price, svr_rbf_predict_values, kr_predict_values, avg_predict_values

@app.route('/')
def home():
	return render_template('main.html')

symbols = []

with open('companylist.csv', 'r') as csvfile:
	for line in csvfile:
		temp = line.split('"')
		symbols.append(temp[1])

@app.route('/', methods=['POST'])
def home_post():
	global client_name
	client_name = request.form['name'].upper()

	if client_name in symbols:
		return make_response(redirect(url_for('main') + "?stock=" + client_name))
	else:
		return make_response(redirect(url_for('home')))

@app.route('/predict', methods=['GET'])
def main():
	stock = request.args.get('stock')
	date = datetime.now()
	date_str = "{}/{}/{}".format(date.month, date.day, date.year)

	date_indexes, actual_price, svr_rbf_predict_values, kr_predict_values, avg_predict_values = predict(stock, 3)
	chart_actual_price = {}
	for i in range(len(actual_price)):
		chart_actual_price[i] = actual_price[i]

	chart_svr_rbf_predict_values = {}
	chart_kr_predict_values = {}
	chart_avg_predict_values = {}
	for i in range(len(date_indexes)):
		date_indexes[i] -= 0
		chart_svr_rbf_predict_values[date_indexes[i]] = svr_rbf_predict_values[i]
		chart_kr_predict_values[date_indexes[i]] = kr_predict_values[i]
		chart_avg_predict_values[date_indexes[i]] = avg_predict_values[i]
	return render_template('index.html',  dates=date_indexes, actual_price=chart_actual_price, 
		svr_rbf_predicted_values=chart_svr_rbf_predict_values, kr_predicted_values=chart_kr_predict_values, 
		avg_predicted_values=chart_avg_predict_values, stock_name=stock,
		date_time=date_str, total=TOTAL)

if __name__ == "__main__":
	app.run(debug=True, threaded=True)