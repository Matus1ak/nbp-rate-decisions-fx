import requests
from datetime import date,timedelta

CHUNK_SIZE = 365 #maximum number of days nbp api allows to fetch at once is 367

def fetch_rates(currency_code, start_date, end_date):
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/{start_date}/{end_date}/?format=json"
    response = requests.get(url)

    return response.json()

def split_to_chunks(start_date, end_date):
    chunks = []
    chunk_start = start_date

    while chunk_start <= end_date:

        chunk_end=min(chunk_start+timedelta(days=CHUNK_SIZE-1),end_date)
        chunks.append((chunk_start,chunk_end))
        chunk_start = chunk_end+timedelta(days=1)

    return chunks

        
