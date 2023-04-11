from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import CandleData, User
from .basebot import get_candle_close
from . import db
from .rsibot import rsicalculation
import json, time, talib, numpy

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/get_new_data')
def get_new_data():
    data = get_candle_close()
    write_data(data)
    return jsonify(candledata = data)

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

@views.route('/read_last_data')
def read_last_data():
    data = CandleData.query.order_by(CandleData.id.desc())
    temp = data.first()
    if isinstance(temp, CandleData):
        return temp.timestamp
    else:
        return 1

@views.route('/write_data')
def write_data(data):
    temp = read_last_data()
    close, timestamp = data.split(' ')
    if temp != int(timestamp):
        new_data = CandleData(close=close, timestamp=timestamp)
        db.session.add(new_data)
        db.session.commit()

@views.route('/methodcalculation')
def methodcalculation():
    userpref = User.query.filter_by(email=current_user.email).first().method_preference
    if userpref == 0:
        rsicalculation(read_all_closes(-1))
    elif userpref == 1:
        print(2)
    elif userpref == 2:
        print(2)
    elif userpref == 3:
        print(2)
    elif userpref == 4:
        print(2)
    elif userpref == 5:
        print(2)
    elif userpref == 6:
        print(2)
    return("Data")

@views.route('/delete_all_data')
def delete_all_data():
    db.reflect()
    db.drop_all()
    return ("Hello")