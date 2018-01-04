from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'reallyreallyreallyreallysecretkey'

manager   = Manager(app)
bootstrap = Bootstrap(app)
moment    = Moment(app)

class TickerForm(FlaskForm):
    stock   = StringField('Stock Symbol:',     validators=[Required()])
    submit    = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    stock = None
    graph = None
    form = TickerForm()
    if form.validate_on_submit():
        stock  = form.stock.data
    graphing()
    return render_template('index.html', form=form, graph=graph)

def graphing():
    ts = TimeSeries(key='XP12DSLMVA2QP4MO', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol='V',interval='15min', outputsize='full')
    data['close'].plot()
    print(data.describe())
    plt.title('stock data stuff')
    plt.show()

if __name__ == '__main__':
    app.run()
