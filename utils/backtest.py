import vectorbt as vbt
from strategies.strategy import Strategy
from helpers import permute_data, random_like
import numpy as np


class Backtest:
    def __init__(
        self,
        ticker: str,
        strategy: Strategy,
        fees: float = 0.001,
        size: float = np.inf,
        freq: str = "1D",
    ):
        self.ticker = ticker
        self.strategy = strategy
        self.fees = fees
        self.size = size
        self.freq = freq

    def __repr__(self):
        return f"<Bactest {str(self.strategy)}>"

    def _get_portfolio(self, entries, exits):
        return vbt.Portfolio.from_signals(
            close=self.strategy.data,
            entries=entries,
            exits=exits,
            fees=self.fees,
            size=self.size,
            freq=self.freq,
        )

    def run(self, **kwargs):
        entries = self.strategy.get_entries()
        exits = self.strategy.get_exits()

        random_entries = entries.apply(random_like)
        permuted_entries = entries.apply(permute_data)

        portfolio = self._get_portfolio(entries, exits, **kwargs)
        random_porfolio = self._get_portfolio(random_entries, exits, **kwargs)
        permuted_portfolio = self._get_portfolio(permuted_entries, exits, **kwargs)

        output = {
            self.ticker: dict(
                mean_expectancy=portfolio.trades.expectancy().mean(),
                max_expectancy=portfolio.trades.expectancy().max(),
                mean_random_expectancy=random_porfolio.trades.expectancy().mean(),
                mean_permuted_expectancy=permuted_portfolio.trades.expectancy().mean(),
            )
        }
        return output


# class Backtest:
#     def __init__(self,
#                  strategy:Strategy,
#                  commision:float,
#                  cash:float):

#         self.strategy = strategy
#         self.commision=commision
#         self.cash = cash


#     def __repr__(self):
#         return f"<Bactest {str(self.strategy)}>"

#     def run(self, **kwargs):
#         entries, exits = self.strategy.signals()
#         portfolio = vbt.Portfolio.from_signals(price=self.strategy.data,
#                                    entries=entries, exits=exits,
#                                    commision = self.commision,
#                                    cash = self.cash, **kwargs)
#         return portfolio.trades.expectancy()

# class AltBacktest:
#     def __init__(self,
#                  ticker:str,
#                  strategy:Strategy,
#                  commision:float,
#                  cash:float):
#         self.ticker=ticker
#         self.strategy = strategy
#         self.commision=commision
#         self.cash = cash


#     def __repr__(self):
#         return f"<Bactest {str(self.strategy)}>"

#     def _get_portfolio(entries, exits, **kwargs):
#         pf = vbt.Portfolio.from_signals(price=self.strategy.data,
#                                         entries=entries, exits=exits,
#                                         commision = self.commision,
#                                         cash = self.cash, **kwargs)

#     def run(self, **kwargs):
#         entries = self.strategy.get_entries()
#         exits = self.strategy.get_exits()

#         random_entries = entries.apply(random_like)
#         permuted_entries = entries.apply(permute_data)

#         portfolio = self._get_portfolio(entries, exits, **kwargs)
#         random_porfolio = self._get_portfolio(random_entries, exits, **kwargs)
#         permuted_portfolio = self._get_portfolio(permuted_entries, exits, **kwargs)

#         output = dict(
#             ticker = self.ticker,
#             mean_expectancy = portfolio.trades.expectancy().mean(),
#             max_expectancy = portfolio.trades.expectancy().max(),
#             mean_random_expectancy= random_porfolio.trades.expectancy().mean(),
#             mean_permuted_expectancy = permuted_portfolio.trades.expectancy().mean()
#         )
#         return output
