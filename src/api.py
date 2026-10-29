import requests
from datetime import date,timedelta

CHUNK_SIZE = 365 #maximum number of days nbp api allows to fetch at once is 367 days

def fetch_rates(currency_code, start_date, end_date):
    
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/{start_date}/{end_date}/?format=json"
    response = requests.get(url, timeout=10)

    status = response.status_code
    info_mes = f"{currency_code} {start_date} {end_date}"


    match status:
        case 200:
            rates_data = response.json()
            print(f"{info_mes}: fetched {len(rates_data['rates'])} days")
            return rates_data
        case 404:
            print(f"{info_mes}: {response.text}")
            return None
        case 400:
            print(f"{info_mes}: {response.text}")
            response.raise_for_status()
        case _:
            print(f"{info_mes} {status} : {response.text}")
            response.raise_for_status()

    



def split_to_chunks(start_date, end_date):
    chunks = []
    chunk_start = start_date

    while chunk_start <= end_date:

        chunk_end=min(chunk_start+timedelta(days=CHUNK_SIZE-1),end_date)
        chunks.append((chunk_start,chunk_end))
        chunk_start = chunk_end+timedelta(days=1)

    return chunks





        
