# NBP Exchange Rates App

## Description
This Flask-based application fetches real-time exchange rates and gold prices from the National Bank of Poland (NBP) API. 
It allows users to view currency exchange rates (USD, EUR, GBP, JPY, CHF, CNY) and the latest gold prices. The app 
features a user-friendly interface to display charts for selected currencies over the past 30 days, and supports 
conversion calculations between different currencies and Polish Zloty (PLN).

## Features
- Fetches exchange rates for major currencies (USD, EUR, GBP, JPY, CHF, CNY etc.) from the NBP API.
- Displays historical currency exchange rate charts for the last 30 days.
- Provides the latest gold prices from the NBP API.
- Allows users to convert currencies to PLN with a simple input form.
- Generates interactive charts using Plotly to visualize currency rates.

## Requirements
- Python 3
- `Flask` (web framework)
- `Flask-SQLAlchemy` (for database integration)
- `Plotly` (for generating interactive charts)
- `requests` (for fetching data from the NBP API)
- `pandas` (for handling and processing data)

## Installation

1. Clone the repository or download the script files.

2. Install the required Python libraries:
   ```sh
   pip install flask
   pip install flask_sqlalchemy
   pip install plotly
   pip install pandas
   pip install requests


## Data Source
NBP API: [https://api.nbp.pl/](https://api.nbp.pl/)
