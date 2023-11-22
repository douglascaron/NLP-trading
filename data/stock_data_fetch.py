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
        data.to_csv(file_name, index=False)
        print(f"Data saved to {file_name}")
    except Exception as e:
        print(f"Error saving data to {file_name}: {e}")

if __name__ == "__main__":
    nasdaq_data_file = "nasdaq_data.csv"
    
    try:
        nasdaq_data = pd.read_csv(nasdaq_data_file)
    except FileNotFoundError:
        print(f"Error: {nasdaq_data_file} not found.")
        exit(1)

    symbol = input("Enter stock symbol: ").upper()  # Convert input to uppercase for case-insensitive comparison
    if symbol not in nasdaq_data['Symbol'].values:
        print(f"Error: {symbol} not found in {nasdaq_data_file}. Please enter a valid symbol.")
        exit(1)

    start_date = datetime.now() - timedelta(days=60)
    end_date = datetime.now()
    interval = "5m"
    file_name = f"{symbol}_{interval}.csv"
    
    try:
        stock_data = get_stock_data(symbol, start_date, end_date, interval)
        if stock_data is not None:
            print("\nStock Data:")
            print(stock_data)

            save_to_csv(stock_data, file_name)
    except ValueError as ve:
        print(f"Error: {ve}")
