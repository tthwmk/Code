from strategies.strategy import Strategy
import vectorbt as vbt
import numpy as np

class SMAStrategy(Strategy):
    def __init__(self, data):
        self.data = data
        self.windows=  np.arange(10, 100, 5)
        self.indicator = vbt.IndicatorFactory.from_pandas_ta("SMA")
        self.fast_sma, self.slow_sma = self.indicator.run_combs(self.data, self.windows, short_names=['fast', 'slow'])
    
    def get_entries(self):
        return self.fast_sma.sma_crossed_above(self.slow_sma)
    
    def get_exits(self):
        return self.fast_sma.sma_crossed_below(self.slow_sma)   


# class SMAStrategy(Strategy):
#     def __init__(self, data, indicator: str, windows=np.arange(10, 100, 5)):
#         self.data = data
#         self.windows = windows
#         self.indicator = vbt.IndicatorFactory.from_pandas_ta(indicator)
#         self.fast_sma, self.slow_sma = self.indicator.run_combs(
#             self.data, self.windows, short_names=["fast", "slow"]
#         )

#     def get_entries(self):
#         return self.fast_sma.sma_crossed_above(self.slow_sma)

#     def get_exits(self):
#         return self.fast_sma.sma_crossed_below(self.slow_sma)
