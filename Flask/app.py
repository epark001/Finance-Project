from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

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
    stock  = None
    form = TickerForm()
    if form.validate_on_submit():
        stock  = form.stock.data
        ticker2  = form.ticker2.data
        interval = form.interval.data
        length   = form.length.data
    return render_template('index.html', form=form, stock=stock, ticker2=ticker2, interval=interval, length=length)

if __name__ == '__main__':
    app.run()
