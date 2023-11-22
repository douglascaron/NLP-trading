import backtrader as bt
import pandas as pd
import yfinance as yf
import os
import matplotlib

class SmaCross(bt.Strategy):
    params = dict(
        pfast=10,
        pslow=20
    )

    def __init__(self):
        sma1 = bt.indicators.SimpleMovingAverage(period=self.params.pfast)
        sma2 = bt.indicators.SimpleMovingAverage(period=self.params.pslow)
        self.crossover = bt.indicators.CrossOver(sma1, sma2)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.close()

def run_strategy(stock):
    cerebro = bt.Cerebro()
    try:
        df = yf.download(stock, period="60d", interval="15m")
    except Exception as e:
        print(f"Error downloading data for {stock}: {e}")
        return
    
    feed = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(feed)
    cerebro.addstrategy(SmaCross)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=75)
    cerebro.broker.set_cash(10000.0)
    
    try:
        cerebro.run()
        # cerebro.plot()
        starting_portfolio_value = cerebro.broker.getvalue()
        ending_portfolio_value = cerebro.broker.getvalue()
        
        # Save results to CSV
        result_data = {'Symbol': [stock], 'End_Cash': [ending_portfolio_value]}
        result_df = pd.DataFrame(result_data)
        result_df.to_csv('backtest_log.csv', mode='a', header=not os.path.exists('backtest_log.csv'), index=False)
        
        print(f"Starting Portfolio Value for {stock}: {starting_portfolio_value}")
        print(f"Ending Portfolio Value for {stock}: {ending_portfolio_value}")
    except Exception as e:
        print(f"Error running strategy for {stock}: {e}")

if __name__ == '__main__':
    df_symbols = pd.read_csv('30_data.csv')    
    for symbol in df_symbols['Symbol']:
        print(f"\nRunning strategy for {symbol}")
        run_strategy(symbol)