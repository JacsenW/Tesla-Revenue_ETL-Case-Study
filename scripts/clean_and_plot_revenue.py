import pandas as pd
import matplotlib.pyplot as plt

def clean_and_plot():
    #load the data
    df_revenue = pd.read_csv('data/raw/tsla_quarterly_revenue.csv')

    #Show rows with missing revenue values
    print("Rows with missing revenue values:")
    print(df_revenue[df_revenue['Revenue'].isna()])

    #Drop rows where Revenue is NaN
    df_cleaned = df_revenue.dropna(subset=['Revenue']).copy()

    #Reset index for cleaned DataFrame
    df_cleaned.reset_index(drop=True, inplace=True)

    #Convert 'Quarter' to datetime
    df_cleaned['Quarter'] = pd.to_datetime(df_cleaned['Quarter'])

    #Plot revenue over time (in billions)
    plt.figure(figsize=(10, 6))
    plt.plot(df_cleaned['Quarter'], df_cleaned['Revenue'] / 1e9, marker='o',)
    plt.title('Tesla Quarterly Revenue (Billion USD)')
    plt.xlabel('Quarter')
    plt.ylabel('Revenue (Billion USD)')
    plt.grid(True)
    plt.show()

    if __name__ == "__main__":
        clean_and_plot()