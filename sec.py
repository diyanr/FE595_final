import re
import requests
from edgar import Company, TXTML
from textblob import TextBlob


def get_all_companies():
    sec_url = 'https://www.sec.gov/Archives/edgar/cik-lookup-data.txt'
    fwd = []
    rev = []
    page = requests.get(sec_url)
    content = page.content.decode("latin1")
    lines = content.split("\n")[:-1]
    for line in lines:
        if line == "":
            continue
        m = re.match('(.*)\:([0-9]+)\:$', line)
        name, cik = m.group(1, 2)
        fwd.append((name, cik))
        rev.append((cik, name))
    return dict(fwd), dict(rev)


def get_companies_by_name(name):
    result = []
    words = name.lower()
    for company, cik in get_all_companies()[0].items():
        if all(word in company.lower() for word in words.split(" ")):
            result.append((name, cik))
    return dict(result)


def get_companies_by_cik(cik):
    name = get_all_companies()[1].get(cik, "None")
    return dict([(name, cik)])


def get_10K_documents(name, cik, num=1):
    company = Company(name, cik)
    # tree = company.get_all_filings(filing_type="10-K")
    # docs = Company.get_documents(tree, no_of_documents=num)
    docs = company.get_10Ks(no_of_documents=num)
    return docs


def parse_10K_document(doc):
    return re.sub(r'[^\x00-\x7F]+', ' ', TXTML.parse_full_10K(doc))


def pull_risk_section(text):
    result = " "
    matches = list(re.finditer(re.compile('Item [0-9][A-Z]*\.', re.IGNORECASE), text))

    end_idx = [i for i in range(len(matches)) if matches[i][0].lower() == 'Item 2.'.lower()]
    if len(end_idx) == 0:
        return result
    else:
        end = max(end_idx)

    start_idx = [i for i in range(len(matches)) if matches[i][0].lower() == 'Item 1A.'.lower() and i < end]
    if len(start_idx) == 0:
        return result
    else:
        start = max(start_idx)

    start = matches[start].span()[1]
    end = matches[end].span()[0]
    return text[start:end]


if __name__ == '__main__':
    sym = 'MRK'
    name = 'Merck & Co.'
    cik = '0000310158'
    raw_docs = get_10K_documents(name, cik, num=1)
    print(len(raw_docs))
    i = 1
    for doc in raw_docs:
        txt_doc = parse_10K_document(doc)
        f = open("10_K.txt", "w")
        f.write(txt_doc)
        f.close()
        risk = pull_risk_section(txt_doc)
        print(risk)
        # print(TextBlob(risk).sentiment.polarity)
