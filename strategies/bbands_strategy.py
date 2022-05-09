from strategies.strategy import Strategy
import vectorbt as vbt
import numpy as np

class BBANDStrategy(Strategy):
    def __init__(self, data):
        self.data = data
        
    def init(self):
        lengths, stds, mas = vbt.utils.params.create_param_combs((product, np.arange(10, 55, 5),  (product, [2, 3],["sma", "ema"]) ) ) 
        self.indicator = vbt.IndicatorFactory.from_pandas_ta("BBANDS").run(
            self.data,
            length=lengths,
            std=stds,
            mamode = mas
        )
        
    
    def get_entries(self):
        self.init()
        return self.indicator.close_below(bbands.bbl)
        
       
    
    def get_exits(self):
        return self.indicator.close_above(bbands.bbu)
          