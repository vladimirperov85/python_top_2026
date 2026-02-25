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
        response.raise_for_status()
        html = response.text
        return html
    except Exception as e:
        print("При выполнение запроса произошла ошибка", e)
        return None


def parse_html(html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    weather_data:{day : {}}
    tables = soup.find_all('table')[2]
    rows = tables.find_all('tr')
    for row in rows:
        cells = row.find_all("td")
        weather_day =  cells[0].text

        weather_temp = cells[1].text
        weather_feeling = cells[2].text
        weather_probability = cells[3].text
        weather_pressure = cells[4].text
        weather_fact = cells[1].find('div')['title']
        weather_wind_direction = cells[5].find_all('span')[0]['title'].strip()
        weather_wind_speed_ms = cells[5].find_all('span')[1].text
        weather_humidity = cells[6].text

        pass


def write_weather_data(weather_data: dict) -> None:
    with open('weather_data.json', 'w', encoding='utf-8') as f:
        json.dump(weather_data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    html = get_html(url=BASE_URL)
    weather_data = parse_html(html=html)
    write_weather_data(weather_data=weather_data)
