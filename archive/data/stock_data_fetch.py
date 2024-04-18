import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_stock_data(symbol, start_date, end_date, interval):
    try:
        data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
        if data.empty:
            print(f"No data available for {symbol} in the specified date range.")
            return None
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def save_to_csv(data, file_name):
    try:
        data.to_csv(file_name, index=True)
        print(f"Data saved to {file_name}")
    except Exception as e:
        print(f"Error saving data to {file_name}: {e}")

if __name__ == "__main__":
    top_30_data = "30_data.csv"
    
    try:
        top30 = pd.read_csv(top_30_data)
    except FileNotFoundError:
        print(f"Error: {top_30_data} not found.")
        exit(1)

    symbol = input("Enter stock symbol: ").upper()  # Convert input to uppercase for case-insensitive comparison
    if symbol not in top30['Symbol'].values:
        print(f"Error: {symbol} not found in {top_30_data}. Please enter a valid symbol.")
        exit(1)

    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()
    interval = input("Interval: ")
    file_name = f"stock_data_{symbol}_{interval}.csv"
    
    try:
        stock_data = get_stock_data(symbol, start_date, end_date, interval)
        if stock_data is not None:
            print("\nStock Data:")
            print(stock_data)

            save_to_csv(stock_data, file_name)
    except ValueError as ve:
        print(f"Error: {ve}")
