import requests
from bs4 import BeautifulSoup
import json


BASE_URL = 'https://world-weather.ru/pogoda/russia/saint_petersburg/'


def get_html(url: str) -> str:
    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 YaBrowser/25.12.0.0 Safari/537.36'
    }
    try:

        response = requests.get(url, headers=headers)
        response.raise_for_status
        html  = response.text
        return html
    except Exception as e:
        print("При выполнение запроса произошла ошибка", e)
        return None



def parse_html(html: str) -> dict:
    soup = BeautifulSoup(html,'html.parser')
    weather_data = {}
    tables  = soup.find_all('table')[2]
    rows = tables.find_all('tr')
    for row in rows:
        pass

html = get_html(url =BASE_URL)
weather_data = parse_html(html = html)



    
   