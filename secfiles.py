import re
import os
import errno
from shutil import copy2
import wiki as w
import random as rnd
from edgar import TXTML


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_10K_files(cik, year):
    doc = ""
    src = r"\Users\diyan\Documents\Stevens\FE595\SEC_DATA\\" + str(year) + r"\QTR1"
    search_str = "10-K_edgar_data_" + str(int(cik))

    src_dir = os.listdir(src)

    for src_file in src_dir:
        if os.path.isfile(src + os.sep + src_file):
            if search_str in src_file:
                with open(src + os.sep + src_file, "r") as f:
                    doc = f.read()
    return doc


def parse_10K_document(doc):
    # text = ""
    # html, properties = TXTML.get_HTML_from_document(doc)
    # if properties.get('type') and '10-K' in properties['type']:
    #     text = text + html.text_content()
    return re.sub(r'[^\x00-\x7F]+', ' ', doc.replace('\n', ''))


def copy_10K_files(cik, year):
    src = r"\Users\diyan\Documents\Stevens\FE595\SEC_DATA\\" + str(year) + r"\QTR1"
    dst = r"\Users\diyan\Documents\Stevens\FE595\FE595_final\Data\sec\\" + str(year)
    search_str = "10-K_edgar_data_" + str(int(cik))

    src_dir = os.listdir(src)

    for src_file in src_dir:
        if os.path.isfile(src + os.sep + src_file):
            if search_str in src_file:
                copy2(src + os.sep + src_file, dst)


if __name__ == '__main__':
    years = [2018, 2017]
    companies = 5
    docs = len(years)

    co_list = list(w.get_sp500_companies().items())
    co_index = [*range(len(co_list))]

    rnd.shuffle(co_index)
    for idx in co_index[:companies]:
        sym, (name, cik) = co_list[idx]
        for year in years:
            copy_10K_files(cik, year)