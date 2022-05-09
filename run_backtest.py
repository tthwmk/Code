from strategies.strategy import Strategy
from strategies.sma_strategy import SMAStrategy
from concurrent.futures import ProcessPoolExecutor
from utils.backtest import Backtest
from pathlib import Path
import pandas as pd


DATA_PATH = Path("./data").resolve()

tickers = [file.stem for file in DATA_PATH.iterdir()]


def run_backtest(ticker: str):
    print(f"backtesting on {ticker} \n")
    data = pd.read_parquet(f"{DATA_PATH/ticker}.parquet").get("Close")
    strategy = SMAStrategy(data)
    backtest = Backtest(ticker, strategy)
    result = backtest.run()
    return pd.DataFrame.from_dict(result, orient="index")

to_process = tickers[:100]

##more computation bound than IO bound
with ProcessPoolExecutor() as executor:
    result = executor.map(run_backtest, to_process)

output = pd.concat(list(result))

output.to_csv("SMA.csv")
