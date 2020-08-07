import itertools
import requests
from bs4 import BeautifulSoup


def get_sp500_companies():
    data = {}
    sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    r = requests.get(sp500_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find("table", {"id": "constituents"})
    table_body = table.find('tbody')

    rows = table_body.findAll('tr')
    for row in rows:
        cells = row.findAll('td')
        if len(cells) >= 8:
            co_sym = cells[0].text.strip()
            co_cik = cells[7].text.strip()
            data[co_sym] = co_cik
    return data


if __name__ == '__main__':
    for sym, cik in itertools.islice(get_sp500_companies().items(), 5):
        print(sym, cik)
