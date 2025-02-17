import requests

from email_sender import send_email

currencies = ["usd", "chf", "gbp", "eur", "jpy", "cny"]
message = "Daily Exchange Rates:\n\n"

for c in currencies:
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{c}/"

    request = requests.get(url)
    content = request.json()

    message += ((content["currency"].capitalize() +
          "\nDate: " + content["rates"][0]["effectiveDate"] +
          "\nAverage rate: " + str(content["rates"][0]["mid"])) +
          "\n\n")

send_email("Daily currencies", message)