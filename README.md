# Daily Exchange Rates

## Description
This script fetches daily exchange rates from the National Bank of Poland (NBP) API for selected currencies, stores them in a MySQL database, and sends them via email.

## Requirements
- Python 3
- `requests` (library for fetching data from the API)
- `mysql-connector-python` (library for connecting to MySQL)
- `email_sender` module for sending emails
-  A running MySQL server

## Installation
1. Clone the repository or download the script file.
2. Install the required libraries:
   ```sh
   pip install requests
   ```
   
   ```sh
   pip install requests mysql-connector-python
   ```

## Functionality
- Fetches exchange rates for USD, CHF, GBP, EUR, JPY, and CNY.
- Stores the exchange rate data in a MySQL database.
- Formats a message containing the currency name, date, and average exchange rate.
- Sends an email with the exchange rate information.

## Data Source
NBP API: [https://api.nbp.pl/](https://api.nbp.pl/)
