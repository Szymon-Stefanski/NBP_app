import mysql.connector
import requests
from email_sender import send_email

connection = mysql.connector.connect(user='root', password='changeme', host='localhost', database='nbp')
my_cursor = connection.cursor()

my_cursor.execute("DROP TABLE IF EXISTS currencies")

my_cursor.execute("""
    CREATE TABLE IF NOT EXISTS currencies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        date VARCHAR(50),
        rate DECIMAL(10,4)
    )
""")

world_currencies = ["usd", "chf", "gbp", "eur", "jpy", "cny"]
message = "Daily Exchange Rates:\n\n"

for c in world_currencies:
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{c}/"

    request = requests.get(url)
    content = request.json()

    message += ((content["currency"].capitalize()  +
          "\nDate: " + content["rates"][0]["effectiveDate"] +
          "\nAverage rate: " + str(content["rates"][0]["mid"])) +
          "\n\n")

    sql = "INSERT INTO currencies (name, date, rate) VALUES (%s, %s, %s)"
    val = (content["currency"].capitalize(),
           content["rates"][0]["effectiveDate"],
           content["rates"][0]["mid"])
    my_cursor.execute(sql, val)

connection.commit()
send_email("Daily currencies", message)

my_cursor.close()
connection.close()
