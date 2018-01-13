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
choices   = [('1day', '1 day'), ('1week', '5 Days'), ('4week', '10 Days'), ('3month', '5 months'), ('1year', '2 years'), ('4year', '4 years')]

class TickerForm(FlaskForm):
    #Validators check if the two tickers are in our list of tickers traded on nasdaq, amex, and nyse
    #Also require for every field to be filled out
    stock   = StringField(u'Stock:',    validators=[Required(), AnyOf(symbols(), message=u'Stock is not a valid symbol!')])
    length    = SelectField(u'Time Length:', validators=[Required()], choices=choices)
    submit    = SubmitField(u'Submit')

#Home page  
@app.route('/', methods=['GET', 'POST'])
def index():
    graph = None
    length = None
    stock = None
    form = TickerForm()
    if form.validate_on_submit():
        stock  = form.stock.data
        length = form.length.data
        graph = stockchart(stock, length)
        return render_template('index.html', form=form, stock=stock, length=length, graph=graph)
    return render_template('index.html', form=form, graph=graph)

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
