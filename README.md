# Daily Exchange Rates

## Description
This script fetches daily exchange rates from the National Bank of Poland (NBP) API for selected currencies and sends them via email.

## Requirements
- Python 3
- `requests` (library for fetching data from the API)
- `email_sender` module for sending emails

## Installation
1. Clone the repository or download the script file.
2. Install the required libraries:
   ```sh
   pip install requests
   ```

## Functionality
- Fetches exchange rates for USD, CHF, GBP, EUR, JPY, and CNY.
- Formats a message containing the currency name, date, and average exchange rate.
- Sends an email with the exchange rate information.

## Data Source
NBP API: [https://api.nbp.pl/](https://api.nbp.pl/)
