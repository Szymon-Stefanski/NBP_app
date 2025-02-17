import requests

from email_sender import send_email

urls = [""]

url = "https://api.nbp.pl/api/exchangerates/rates/a/chf/"

request = requests.get(url)
content = request.json()
print(content)

message = (content["currency"].capitalize() +
      "\nDate: " + content["rates"][0]["effectiveDate"] +
      "\nAverage rate: " + str(content["rates"][0]["mid"]))

send_email("Daily currencies", message)