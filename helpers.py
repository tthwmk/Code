import numpy as np
import pandas as pd
from typing import List, Optional, Union
from pathlib import Path
import time
import yfinance as yf


def permute_data(data: pd.Series, seed: Optional[int] = 1730) -> pd.Series:
    """
    shuffled a given data, N.B faster than the np.shuffle and
    allows for using random state for replicability
    """
    rng = np.random.default_rng(seed)
    permuted_data = rng.permutation(data.values)  # faster than choice
    return pd.Series(data=permuted_data, index=data.index)


def random_like(
    data: pd.Series,
    seed: Optional[int] = 1730,
    p: List[float] = [
        0.5,
    ],
    binomial: Optional[bool] = True,
) -> pd.Series:
    """
    generates entries of the same size as the main entries according to given probabilities.
    two options are given, Binomial or choice. Binomial is faster

    """
    rng = np.random.default_rng(seed)
    if binomial:
        random_data = rng.binomial(n=1, p=0.5, size=data.size).astype("bool")
    else:
        random_data = rng.choice([True, False], size=data.size, p=p)
    return pd.Series(data=random_data, index=data.index)


DATA_PATH = Path("./data").resolve()

if not DATA_PATH.exists():
    DATA_PATH.mkdir()


def download_data(
    ticker: str,
    period: Optional[str] = "max",
    interval: Optional[str] = "1d",
    auto_adjust: Optional[bool] = True,
    retries: Optional[int] = 3,
    path: Union[str, Path] = DATA_PATH,
):
    """
    downloads data from yahoo and converts it to parquet for speed and space
    to be run using a threadpool executor since it is IO bound.

    i.e from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor as executor:
        executor.map(download_data, [Tickers])

    TODO:
        stop it from save parquet files of empty tickers

    """
    for _ in range(retries):
        try:
            temp = yf.Ticker(ticker)
            temp_history = temp.history(
                period=period, interval=interval, auto_adjust=auto_adjust
            )
            temp_history.to_parquet(
                path=f"{path/ticker}.parquet", engine="pyarrow", index=True
            )
            print(f"{ticker} was successfully downloaded")
            time.sleep(2)
        except:
            pass


def delete_empty_parquet(path):
    for p in path.iterdir():
        if (len(pd.read_parquet(p))) == 0:
            print(f"deleting {p}")
            p.unlink()


def get_file_name(path: Path, output: list = []):
    for file in path.iterdir():
        output.append(file.stem)
    return output
