import time
from datetime import date,timedelta
import requests

REQUESTS_NUMBER = 3 # how many times code tries to fetch rates from api
CHUNK_SIZE = 365 #maximum number of days nbp api allows to fetch at once is 367 days

def fetch_rates(currency_code, start_date, end_date):
    
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/{start_date}/{end_date}/?format=json"
    
    info_mes = f"{currency_code} {start_date} {end_date}"

    for i in range(1,REQUESTS_NUMBER+1):
        try: 
            response = requests.get(url, timeout=10)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:

            print(f"{info_mes}: {type(e).__name__} ; attempt {i} out of {REQUESTS_NUMBER}")

            if i == REQUESTS_NUMBER: 
                raise
            else: 
                time.sleep(2**(i-1))
                continue
        
        status = response.status_code

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
            case status if 500 <= status < 600:
                print(f"{info_mes} {status}: {response.text} ; attempt {i} out of {REQUESTS_NUMBER}")

                if i == REQUESTS_NUMBER: 
                    response.raise_for_status()
                else: 
                    time.sleep(2**(i-1))               

            case _:
                print(f"{info_mes} {status}: {response.text}")
                response.raise_for_status()

    

def split_to_chunks(start_date, end_date):
    chunks = []
    chunk_start = start_date

    while chunk_start <= end_date:

        chunk_end=min(chunk_start+timedelta(days=CHUNK_SIZE-1),end_date)
        chunks.append((chunk_start,chunk_end))
        chunk_start = chunk_end+timedelta(days=1)

    return chunks