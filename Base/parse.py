import requests
from bs4 import BeautifulSoup
import lxml
from openpyxl import Workbook
from time import sleep

# Парсинг новостей с сайта https://ria.ru/

BASE_URL = 'https://ria.ru/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

def parse_ria_news():
    all_news = []

    try:
        print('Parsing...')
        print(f'url: {BASE_URL}')
        print('-'*30)

        response = requests.get(BASE_URL, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f'Error {response.status_code}')
            return all_news

        soup = BeautifulSoup(response.text, 'lxml')
        news_block = soup.find_all('div', class_='cell-list__item m-no-image')
        print('news_block')
        print(f'NEWS: {len(news_block)}')
        
        for i, block in enumerate(news_block):
            try:
                # Ищем ссылку с заголовком
                title_link = block.find('a', class_='cell-list__item-title')
                if not title_link:
                    print(f'Не найден заголовок {i}')
                    continue
                
                # Получаем текст заголовка
                title = title_link.text.strip()
                print(title)
                
                # СОХРАНЯЕМ в список!
                all_news.append({
                    'title': title,
                    # сюда можно добавить ссылку, дату и т.д.
                })
                
            except Exception as e:
                print(f'Ошибка при парсинге новости {i}: {e}')
                
    except Exception as e:
        print(f'Ошибка при загрузке страницы: {e}')
    
    return all_news

if __name__ == '__main__':
    new_data = parse_ria_news()
    print(f'Всего собрано новостей: {len(new_data)}')
    print(new_data)



       
          
    
     