import itertools
import wiki as w
import sec as s
from textblob import TextBlob


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    for sym, cik in itertools.islice(w.get_sp500_companies().items(), 5):
        raw_docs = s.get_documents(sym, cik, type='10-K', num=5)
        rsk_docs = [s.pull_risk_section(s.parse_10K_document(doc)) for doc in raw_docs]
        rsk_sentiment = [TextBlob(rsk).sentiment.polarity for rsk in rsk_docs]
        print(sym, cik, rsk_sentiment)
