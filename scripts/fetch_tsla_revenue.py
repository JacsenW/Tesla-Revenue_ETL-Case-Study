import yfinance as yf
import pandas as pd
import os

def fetch_tsla_revenue():
    tsla = yf.Ticker("TSLA")
    quarterly_income = tsla.quarterly_financials.T
    
    if 'Total Revenue' in quarterly_income.columns:
        revenue = quarterly_income['Total Revenue']
    elif 'Revenue' in quarterly_income.columns:
        revenue = quarterly_income['Revenue']
    else:
        revenue = quarterly_income.loc['Total Revenue'] if 'Total Revenue' in quarterly_income.index else None

    if revenue is None:
        print("Revenue data not found in financials")
        return

    df_revenue = revenue.reset_index()
    df_revenue.columns = ['Quarter', 'Revenue']
    df_revenue['Quarter'] = pd.to_datetime(df_revenue['Quarter'])
    df_revenue.sort_values('Quarter', inplace=True)

    # Make sure directory exists
    os.makedirs('data/raw', exist_ok=True)

    df_revenue.to_csv('data/raw/tsla_quarterly_revenue.csv', index=False)
    print(df_revenue)

if __name__ == "__main__":
    fetch_tsla_revenue()
# This script fetches Tesla's quarterly revenue data and saves it to a CSV file.
# It uses the yfinance library to retrieve financial data and pandas for data manipulation.