from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
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


@app.route("/charts/")
def charts():
    data = {
        "date": ["2025-02-01", "2025-02-17", "2025-03-03"],
        "value": [4.20, 4.25, 4.18]
    }
    df = pd.DataFrame(data)

    fig = px.line(df, x="date", y="value", title="Kurs EUR/PLN")
    graph_html = fig.to_html(full_html=False)

    return render_template("charts.html", graph_html=graph_html)


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


# CURRENCIES - EXCHANGE RATES:
@app.route("/api/exchangerates/rates/a/<currency>/")
def value(currency):
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Invalid request"}, response.status_code

    return response.json()


@app.route("/api/exchangerates/rates/a/<currency>/<date>")
def value_date(currency, date):
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/{date}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Invalid request"}, response.status_code

    return response.json()


@app.route("/api/exchangerates/rates/a/<currency>/<startDate>/<endDate>")
def value_from_to(currency, startDate, endDate):
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/{startDate}/{endDate}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Invalid request"}, response.status_code

    return response.json()


@app.route("/api/exchangerates/rates/a/<currency>/last/{topCount}")
def value_top(currency, topCount):
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/{topCount}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Invalid request"}, response.status_code

    return response.json()


# GOLD PRICES:
@app.route("/api/cenyzlota")
def gold():
    url = f"https://api.nbp.pl/api/cenyzlota/"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Invalid request"}, response.status_code

    return response.json()


@app.route("/api/cenyzlota/last/<topCount>")
def gold_top(topCount):
    url = f"https://api.nbp.pl/api/cenyzlota/last/{topCount}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Invalid request"}, response.status_code

    return response.json()


@app.route("/api/cenyzlota/<date>")
def gold_date(date):
    url = f"https://api.nbp.pl/api/cenyzlota/{date}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Invalid request"}, response.status_code

    return response.json()


@app.route("/api/cenyzlota/<startDate>/<endDate>")
def gold_from_to(startDate, endDate):
    url = f"https://api.nbp.pl/api/cenyzlota/{startDate}/{endDate}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Invalid request"}, response.status_code

    return response.json()


if __name__ == "__main__":
    app.run(debug=True)
