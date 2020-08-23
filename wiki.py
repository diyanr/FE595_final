import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_sp500_companies():
    sym = []
    name = []
    cik = []
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
            sym.append(cells[0].text.strip())
            name.append(cells[1].text.strip())
            cik.append(cells[7].text.strip())

    return pd.DataFrame({"Name": name,
                         "Symbol": sym,
                         "CIK": cik})


if __name__ == '__main__':
    # Get list of companies that are components of the S&P 500 Index
    get_sp500_companies().to_csv(r"./Data/sp500.csv", index=False)
