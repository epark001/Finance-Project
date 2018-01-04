from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required, AnyOf
from flask_navigation import Navigation
from algo import *       


app = Flask(__name__)
nav = Navigation(app)
app.config['SECRET_KEY'] = 'reallyreallyreallyreallysecretkey'


manager   = Manager(app)
bootstrap = Bootstrap(app)
moment    = Moment(app)
#choices for length in form
choices   = [('', ''),('1day', '1 day'), ('1week', '1 week'), ('4week', '4 weeks'), ('3month', '3 months'), ('1year', '1 year'), ('5year', '5 years')]

class TickerForm(FlaskForm):
    #Validators check if the two tickers are in our list of tickers traded on nasdaq, amex, and nyse
    #Also require for every field to be filled out
    stock   = StringField(u'Stock:',    validators=[Required(), AnyOf(symbols(), message=u'Stock is not a valid symbol!')])
    submit    = SubmitField(u'Submit')

#Home page  
@app.route('/', methods=['GET', 'POST'])
def index():
    graph = None
    stock = None
    form = TickerForm()
    if form.validate_on_submit():
        stock  = form.stock.data
        graph = candlestick(stock)
        return render_template('index.html', form=form, stock=stock, graph = graph)
    return render_template('index.html', form=form, graph = graph)

#Team page 
@app.route('/team', methods=['GET', 'POST'])
def team():
    return render_template('team.html')

#Algorithm page
@app.route('/algorithm', methods=['GET', 'POST'])
def algorithm():
    return render_template('algorithm.html')

#News page
@app.route('/news', methods=['GET', 'POST'])
def news():
    return render_template('news.html', ticker1 = 'GOOGL', ticker2 = 'MSFT')

#Run app
if __name__ == '__main__':
    app.run()
