import requests
from bs4 import BeautifulSoup
import chardet


def get_b3_stock_codes():
    url = 'https://www.fundamentus.com.br/detalhes.php'
    headers = {
        'User-Agent': (
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
           'AppleWebKit/537.36 (KHTML, like Gecko)'
           'Chrome/58.0.3029.110 Safari/537.3')
    }

    response = requests.get(url, headers=headers)

    # Detectar a codificação correta
    detected_encoding = chardet.detect(response.content)['encoding']
    response.encoding = detected_encoding if detected_encoding else 'utf-8'

    if response.status_code != 200:
        raise Exception(
            ('Error retrieving table. '
              f'Status code: {response.status_code}')
            )

    soup = BeautifulSoup(response.text, 'lxml')  # Usar lxml como parser

    table = soup.find('table', {'id': 'test1', 'class': 'resultado'})

    if table is None:
        raise Exception('Stickers table not found.')

    stock_codes = [
        {
            'sticker': cells[0].text.strip(),
            'company_name': cells[1].text.strip(),
            'company_full_name': cells[2].text.strip()
        }
        for row in table.find_all('tr')[1:]
        if (cells := row.find_all('td')) and len(cells) >= 3
        and cells[0].text.strip() and cells[1].text.strip()
        and cells[2].text.strip()
    ]

    return stock_codes
