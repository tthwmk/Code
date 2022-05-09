from utils import download_data
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

tickers = pd.read_csv("tickers.csv").values.flatten()

sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
sp500_symbols = pd.read_html(sp500_url, header=0)[0].Symbol.to_list()

to_download = list(set(tickers) - set(sp500_symbols))
to_download = to_download[len(to_download) // 2 :]

##since this is io-bound (network io) we use threadpool
with ThreadPoolExecutor() as executor:
    executor.map(download_data, to_download)
