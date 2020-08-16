import secfiles as sf
import random as rnd
import wiki as w
import sec as s
from textblob import TextBlob
import pandas as pd
import yahoofin as y


def get_10K_txt_file(co_cik, year):
    txt_doc = sf.get_10K_files(co_cik, year)
    rsk_doc = s.pull_risk_section(sf.parse_10K_document(txt_doc))
    rsk_sentiment = TextBlob(rsk_doc).sentiment.polarity
    return rsk_sentiment


# def get_10K_risk_sentiments(co_name, co_cik, no_of_docs=5):
#     raw_docs = s.get_10K_documents(co_name, co_cik, num=no_of_docs)
#     rsk_docs = [s.pull_risk_section(s.parse_10K_document(doc)) for doc in raw_docs]
#     rsk_sentiment = [TextBlob(rsk).sentiment.polarity for rsk in rsk_docs]
#     return rsk_sentiment

def get_10K_risk_sentiments(companies, years, no_of_companies=5, shuffle=True):
    year_lst = []
    name_lst = []
    sym_lst = []
    cik_lst = []
    sentiment_lst = []

    # co_list = pd.read_csv(r".\Data\sp500.csv")
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


def get_quarterly_returns(year, comapnies=5, shuffle=True):
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


if __name__ == '__main__':
    years = [*range(2018, 2008, -1)]
    companies = 500

    # get_10K_risk_sentiments(years, companies).to_csv(r"./Data/sentiments.csv", index=False)

    # get_quarterly_returns(years, companies).to_csv(r"./Data/returns.csv", index=False)

    sentiments = pd.read_csv(r".\Data\sentiments.csv")
    get_returns_for_sentiment(sentiments).to_csv(r".\Data\results.csv")

    # docs = len(years)
    #
    # co_list = list(w.get_sp500_companies().items())
    # co_list = pd.read_csv(r".\Data\sp500.csv")
    # co_index = [*range(len(co_list))]
    #
    # rnd.shuffle(co_index)
    # # for idx in co_index[:companies]:
    # #     name, sym, cik = co_list.loc[idx,:]
    # #     print(name, sym, cik)
    #
    # with open("./Data/sent.txt", "w+") as file:
    #     for idx in co_index[:companies]:
    #         name, sym, cik = co_list.loc[idx, :]
    #         for year in years:
    #             sentiment = get_10K_txt_file(cik, year)
    #             file.write(f'"{sym}" , "{name}", "{cik}", {year}, {sentiment}\n')
    # sentiment = get_10K_risk_sentiments(name, cik, no_of_docs=docs)
    # for i in range(len(sentiment)):
    #     file.write(f'"{sym}" , "{name}", "{cik}", {years[i]}, "{sentiment[i]}"\n')
