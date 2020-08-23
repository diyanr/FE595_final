import random as rnd
import wiki as w
import sec as s
from textblob import TextBlob
import pandas as pd
import yahoofin as y


def get_10K_txt_file(co_cik, year):
    """
    Get the sentiment of the Risk Section (Item 1A.) from text 10-K filings
    from previously downloaded filings for a given company CIK and year
    """
    txt_doc = s.get_10K_doc_txt(co_cik, year)
    rsk_doc = s.pull_risk_section(s.parse_10K_doc_txt(txt_doc))
    rsk_sentiment = TextBlob(rsk_doc).sentiment.polarity
    return rsk_sentiment


def get_10K_risk_sentiments(companies, years, no_of_companies=5, shuffle=True):
    """
    Return a pandas dataframe containing the risk sentiments
    for a number of companies from a given list of companies (randomly shuffled)
    for a given list of years
    """
    year_lst = []
    name_lst = []
    sym_lst = []
    cik_lst = []
    sentiment_lst = []

    co_index = [*range(len(companies))]

    if shuffle:
        rnd.shuffle(co_index)

    for idx in co_index[:no_of_companies]:
        name, sym, cik = companies.loc[idx, :]
        for year in years:
            sentiment_lst.append(get_10K_txt_file(cik, year))
            year_lst.append(year)
            name_lst.append(name)
            sym_lst.append(sym)
            cik_lst.append(cik)

    return pd.DataFrame({"Name": name_lst,
                         "Symbol": sym_lst,
                         "CIK": cik_lst,
                         "Year": year_lst,
                         "Sentiment": sentiment_lst})


def get_quarterly_returns(years, companies=5, shuffle=True):
    """
    Returns a pandas dataframe containing the quarterly returns
    for a number of companies in the S&P 500 index (randomly shuffled)
    for a given list of years
    """
    year_lst = []
    name_lst = []
    sym_lst = []
    cik_lst = []
    q1_lst = []
    q2_lst = []
    q3_lst = []
    q4_lst = []

    co_list = pd.read_csv(r".\Data\sp500.csv")
    co_index = [*range(len(co_list))]

    if shuffle:
        rnd.shuffle(co_index)

    for idx in co_index[:companies]:
        name, sym, cik = co_list.loc[idx, :]
        for year in years:
            q1, q2, q3, q4 = y.get_returns(sym, year)
            q1_lst.append(q1)
            q2_lst.append(q2)
            q3_lst.append(q3)
            q4_lst.append(q4)
            year_lst.append(year)
            name_lst.append(name)
            sym_lst.append(sym)
            cik_lst.append(cik)
    return pd.DataFrame({"Name": name_lst,
                         "Symbol": sym_lst,
                         "CIK": cik_lst,
                         "Year": year_lst,
                         "Q1": q1_lst, "Q2": q2_lst, "Q3": q3_lst, "Q4": q4_lst})


def get_returns_for_sentiment(sentiments):
    """
    Returns a pandas dataframe containing the quarterly returns
    of list of companies provided in the list of sentiments provided.
    This list of sentiments will be for a number of companies for a number of years.
    """
    year_lst = []
    name_lst = []
    sym_lst = []
    cik_lst = []
    senti_lst = []
    q1_lst = []
    q2_lst = []
    q3_lst = []
    q4_lst = []

    for index, row in sentiments.iterrows():
        name, sym, cik, year, senti = row["Name"], row["Symbol"], row["CIK"], row["Year"], row["Sentiment"]
        q1, q2, q3, q4 = y.get_returns(sym, year)
        q1_lst.append(q1)
        q2_lst.append(q2)
        q3_lst.append(q3)
        q4_lst.append(q4)
        year_lst.append(year)
        name_lst.append(name)
        sym_lst.append(sym)
        cik_lst.append(cik)
        senti_lst.append(senti)

    return pd.DataFrame({"Name": name_lst,
                         "Symbol": sym_lst,
                         "CIK": cik_lst,
                         "Year": year_lst,
                         "Sentiment": senti_lst,
                         "Q1": q1_lst, "Q2": q2_lst, "Q3": q3_lst, "Q4": q4_lst})


def get_returns_for_spy(years):
    """
    Returns the quarterly returns for the SPY ETF
    which will be used as the benchmark for the S&P 500 Index
    """
    sym = 'SPY'
    name = 'SPDR S&P 500 ETF Trust'

    year_lst = []
    name_lst = []
    sym_lst = []
    cik_lst = []
    q1_lst = []
    q2_lst = []
    q3_lst = []
    q4_lst = []

    for year in years:
        q1, q2, q3, q4 = y.get_returns(sym, year)
        q1_lst.append(q1)
        q2_lst.append(q2)
        q3_lst.append(q3)
        q4_lst.append(q4)
        year_lst.append(year)
        name_lst.append(name)
        sym_lst.append(sym)

    return pd.DataFrame({"Name": name_lst,
                         "Symbol": sym_lst,
                         "Year": year_lst,
                         "Q1": q1_lst, "Q2": q2_lst, "Q3": q3_lst, "Q4": q4_lst})


if __name__ == '__main__':
    years = [*range(2018, 2008, -1)]
    companies = 500

    # get_10K_risk_sentiments(years, companies).to_csv(r"./Data/sentiments.csv", index=False)

    # get_quarterly_returns(years, companies).to_csv(r"./Data/returns.csv", index=False)

    # sentiments = pd.read_csv(r".\Data\sentiments.csv")
    # get_returns_for_sentiment(sentiments).to_csv(r".\Data\results.csv", index=False)

    get_returns_for_spy(years).to_csv(r".\Data\spy.csv", index=False)
