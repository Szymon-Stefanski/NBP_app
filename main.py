from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import plotly.express as px
import pandas as pd
import requests

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nbp.db'
db = SQLAlchemy(app)


class Currencies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.String(50), nullable=False)
    rate = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Currencies %r>' % self.name


class Gold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    rate = db.Column(db.Float, nullable=False)


@app.route("/")
def about():
    return render_template("main.html")


@app.route("/currencies/", methods=['GET'])
def display_currencies():
    url = "https://api.nbp.pl/api/exchangerates/tables/a/"
    get = requests.get(url)
    content = get.json()

    currencies_nbp = []

    for rate in content[0]["rates"]:
        currencies_nbp.append({
            "name": rate["currency"],
            "code": rate["code"],
            "date": content[0]["effectiveDate"],
            "rate": rate["mid"]
        })

    for x in currencies_nbp:
        new_currency = Currencies(name=x["name"],
                                  code=x["code"],
                                  date=x["date"],
                                  rate=x["rate"])
        try:
            db.session.add(new_currency)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            currencies = Currencies.query.order_by(Currencies.date).all()
            return render_template("currencies.html", currencies=currencies)

    currencies = Currencies.query.order_by(Currencies.date).all()
    return render_template("currencies.html", currencies=currencies)


@app.route("/gold/", methods=['GET'])
def display_gold():
    url = "https://api.nbp.pl/api/cenyzlota/"
    get = requests.get(url)
    content = get.json()

    data = content[0]['data']
    cena = content[0]['cena']

    existing_gold = Gold.query.filter_by(date=data).first()

    if existing_gold is None:
        new_gold = Gold(date=data, rate=cena)
        try:
            db.session.add(new_gold)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            gold = Gold.query.order_by(Gold.date).all()
            return render_template("gold.html", gold=gold)
    else:
        pass

    gold = Gold.query.order_by(Gold.date).all()
    return render_template("gold.html", gold=gold)


@app.route("/calculator/", methods=['GET', 'POST'])
def calculator():
    currencies = Currencies.query.all()

    result = None

    if request.method == 'POST':
        code = request.form["code"]
        amount = float(request.form['amount'])

        for currency in currencies:
            if currency.code == code:
                rate = currency.rate
                result = round((amount * rate),2)
                break

    return render_template("calculator.html", currencies=currencies, result=result)


@app.route("/charts/", methods=['GET', 'POST'])
def charts():
    currencies = Currencies.query.all()

    today = datetime.today()
    thirty_days_ago = today - timedelta(days=30)
    formatted_date = thirty_days_ago.strftime('%Y-%m-%d')

    data = {
        "date": [],
        "value": []
    }

    graph_html = None

    if request.method == 'POST':
        code = request.form["code"]

        url = (f"https://api.nbp.pl/api/exchangerates/rates/a/{code}/{formatted_date}/"
               f"{today.strftime('%Y-%m-%d')}/")
        get = requests.get(url)
        content = get.json()

        if "rates" in content and content["rates"]:
            for rate in content["rates"]:
                data["date"].append(rate["effectiveDate"])
                data["value"].append(rate["mid"])

            df = pd.DataFrame(data)

            fig = px.line(df, x="date", y="value", title=f"Course {code}/PLN")
            graph_html = fig.to_html(full_html=False)
        else:
            print("API problem.")

    return render_template("charts.html", graph_html=graph_html, currencies=currencies)


if __name__ == "__main__":
    app.run(debug=True)
