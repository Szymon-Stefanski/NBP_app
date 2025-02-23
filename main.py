from flask import Flask, render_template
import requests

app = Flask(__name__, static_folder='static')

@app.route("/")
def home():
    return render_template("main.html")

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
