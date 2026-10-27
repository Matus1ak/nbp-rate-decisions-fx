import requests

def fetch_rates(currency_code, start_date, end_date):
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/{start_date}/{end_date}/?format=json"
    response = requests.get(url)

    return response.json()