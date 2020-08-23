import os
import re
import requests
from edgar import Company, TXTML


def get_all_companies():
    """
    Used to get all company names and CIK from the EDGAR web-site
    """
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
    """
    Find all companies with given name from EDGAR website
    """
    result = []
    words = name.lower()
    for company, cik in get_all_companies()[0].items():
        if all(word in company.lower() for word in words.split(" ")):
            result.append((name, cik))
    return dict(result)


def get_companies_by_cik(cik):
    """
    Find the company name for a given CIK
    """
    name = get_all_companies()[1].get(cik, "None")
    return dict([(name, cik)])


def get_10K_doc_raw(name, cik):
    """
    Get the latest 10-K filing document for a given company
    using the edgar package
    """
    company = Company(name, cik)
    # tree = company.get_all_filings(filing_type="10-K")
    # docs = Company.get_documents(tree, no_of_documents=1)
    docs = company.get_10Ks(no_of_documents=1)
    return docs


def get_10K_doc_txt(cik, year):
    """
    Get the 10-K annual filing for a given company CIK for a given year
    from all filings already downloaded
    """
    txt_doc = ""
    src = r"\Users\diyan\Documents\SEC_DATA\\" + str(year) + r"\QTR1"
    search_str = "10-K_edgar_data_" + str(int(cik))

    src_dir = os.listdir(src)

    for src_file in src_dir:
        if os.path.isfile(src + os.sep + src_file):
            if search_str in src_file:
                with open(src + os.sep + src_file, "r") as f:
                    txt_doc = f.read()
    return txt_doc


def parse_10K_doc_raw(raw_doc):
    """
    Parse the raw 10-K document using re and TXTML libraries
    """
    return re.sub(r'[^\x00-\x7F]+', ' ', TXTML.parse_full_10K(raw_doc))


def parse_10K_doc_txt(txt_doc):
    """
    Parse the text 10-K document using the re library
    """
    return re.sub(r'[^\x00-\x7F]+', ' ', txt_doc.replace('\n', ''))


def pull_risk_section(text):
    """
    Extract the Risk Section (Item 1A.) from the annual 10-K document
    """
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
    raw_docs = get_10K_doc_raw(name, cik)
    print(len(raw_docs))
    i = 1
    for doc in raw_docs:
        txt_doc = parse_10K_doc_raw(doc)
        f = open(r".\Data\10_K.txt", "w")
        f.write(txt_doc)
        f.close()
        risk = pull_risk_section(txt_doc)
        print(risk)
