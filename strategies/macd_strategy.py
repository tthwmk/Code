from strategies.strategy import Strategy
import vectorbt as vbt
import numpy as np

class MACDStrategy(Strategy):
    def __init__(self, data):
        self.data = data
        
    def init(self):
        fast_windows, slow_windows, signal_windows = vbt.utils.params.create_param_combs(
            (product, (combinations, np.arange(2, 51, 1), 2), np.arange(2, 21, 1)))
        
        self.indicator = vbt.MACD.run(
            self.data,
            fast_window=fast_windows,
            slow_window=slow_windows,
            signal_window=signal_windows
        )
    
    def get_entries(self):
        self.init()
        return self.indicator.macd_above(0) & self.indicator.macd_above(self.indicator.signal)
    
    def get_exits(self):
        return self.indicator.macd_below(0) | self.indicator.macd_below(self.indicator.signal)   