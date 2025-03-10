from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nbp.db'
db = SQLAlchemy(app)

class Currencies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.String(50))
    rate = db.Column(db.Float)

    def __repr__(self):
        return '<Currencies %r>' % self.name

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        currency_content = request.form['content']
        url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency_content}/"
        getter = requests.get(url)
        content = getter.json()

        new_currency = Currencies(name=currency_content.upper(),
                                  date=content["rates"][0]["effectiveDate"],
                                  rate=content["rates"][0]["mid"])

        try:
            db.session.add(new_currency)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            db.session.rollback()
            return f"Error: {e}"
    else:
        currencies = Currencies.query.order_by(Currencies.date).all()
        return render_template("main.html", currencies=currencies)

@app.route("/about")
def about():
    return render_template("about.html")

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
