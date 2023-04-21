from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import CandleData, User, Transactions, BacktestTransactions
from .bots.basebot import reset_backtesting_data, get_wallet_balance as get_user_wallet
from . import db
from .bots.rsibot import rsicalculation
from .bots.smabot import smacalculation
from .bots.emabot import emacalculation
from .bots.wmabot import wmacalculation
from .bots.macdbot import macdcalculation
from .bots.obvbot import obvcalculation
from .bots.bbbot import bollingerbandcalculation

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/read_all_data/<dataamount>')
def read_all_data(dataamount):
    closes = []
    if dataamount == -1:
        data = CandleData.query.order_by(CandleData.id.desc())
    else:
        data = CandleData.query.order_by(CandleData.id.desc()).limit(dataamount)
    for d in data:
        closes.append(str(d.close) + " " + str(d.timestamp))
    closes.reverse()
    return jsonify(candlecloses = closes)

@views.route('/read_all_closes/<dataamount>')
def read_all_closes(dataamount):
    closes = []
    if dataamount == -1:
        data = CandleData.query.order_by(CandleData.id.desc())
    else:
        data = CandleData.query.order_by(CandleData.id.desc()).limit(dataamount)
    for d in data:
        closes.append(float(d.close))
    closes.reverse()
    return (closes)

@views.route('/get_wallet_balance')
def get_wallet_balance():
    return jsonify(get_user_wallet())


@views.route('/read_all_transactions/')
def read_all_transactions():
    transactions = []
    data = Transactions.query.order_by(Transactions.id.desc())
    for d in data:
        transactions.append(str(d.information))
    transactions.reverse()
    return jsonify(transactions = transactions)

@views.route('/read_all_backtest_transactions/')
def read_all_backtest_transactions():
    transactions = []
    data = BacktestTransactions.query.order_by(BacktestTransactions.id.desc())
    for d in data:
        transactions.append(str(d.information))
    transactions.reverse()
    return jsonify(transactions = transactions)

@views.route('/read_last_data')
def read_last_data():
    data = CandleData.query.order_by(CandleData.id.desc())
    temp = data.first()
    if isinstance(temp, CandleData):
        return temp.timestamp
    else:
        return 1

@views.route('/methodcalculation')
def methodcalculation(data=[], backtesting=0):
    userpref = User.query.filter_by(email=current_user.email).first().method_preference
    if data != []:
        closes = data
    else:
        closes = read_all_closes(-1)
    if userpref == 0:
        rsicalculation(closes, backtesting)
    elif userpref == 1:
        smacalculation(closes, backtesting)
    elif userpref == 2:
        emacalculation(closes, backtesting)
    elif userpref == 3:
        wmacalculation(closes, backtesting)
    elif userpref == 4:
        macdcalculation(closes, backtesting)
    elif userpref == 5:
        obvcalculation(closes, backtesting)
    elif userpref == 6:
        bollingerbandcalculation(closes, backtesting)
    return("Method Calculation")

@views.route('/backtesting', methods=['GET', 'POST'])
@login_required
def backtesting(): 
    reset_backtesting_data()
    if request.method == 'POST':  
        closes = []

        file = request.files['file-input']

        while line := file.readline():
            text = line.decode('utf-8')
            close, timestamp = text.strip().split(' ')
            closes.append(float(close))

            methodcalculation(closes, 1)

        print(closes)
                
    return render_template("backtesting.html", user=current_user)

@views.route('/delete_all_data')
def delete_all_data():
    db.reflect()
    db.drop_all()
    return ("Database Cleared!")