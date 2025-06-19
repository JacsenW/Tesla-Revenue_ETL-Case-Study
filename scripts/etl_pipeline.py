import os 
import pandas as pd
import psycopg2
from sqlalchemy import create_engine 
from dotenv import load_dotenv
from pathlib import Path

# 📂 Load .env from root directory
from dotenv import load_dotenv
load_dotenv()  # Automatically looks in current and parent dirs


# 🔐 Get DB credentials from .env
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

# ✅ Confirm env vars loaded
print(f"🔐 DB_USER: {DB_USER}")
print(f"🔐 DB_NAME: {DB_NAME}")
print(f"🔐 DB_PASSWORD loaded: {'Yes' if DB_PASSWORD else 'No'}")

# 📄 CSV path
CSV_PATH = Path(__file__).resolve().parent.parent / 'data' / 'raw' / 'tsla_quarterly_revenue.csv'

# 📊 Step 1 - Clean CSV
def fetch_and_clean_data():
    print("📥 Reading CSV file...")
    df = pd.read_csv(CSV_PATH)
    df['Quarter'] = pd.to_datetime(df['Quarter'])
    df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
    df.rename(columns={'Quarter': 'qtr', 'Revenue': 'rev'}, inplace=True)
    print("✅ Data cleaned.")
    return df

# 🛢️ Step 2 - Load into Postgres
def load_data_to_postgres(df):
    print("🚀 Loading cleaned data to PostgreSQL...")
    try:
        db_url = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        engine = create_engine(db_url)
        df.to_sql('quarterly_revenue', engine, if_exists='replace', index=False)
        print("✅ Data loaded successfully.")
    except Exception as e:
        print("❌ Failed to load data:", e)

# 🚨 Step 3 - Log alerts
def log_revenue_drops(threshold=15):
    print(f"🔍 Checking for revenue drops greater than {threshold}%...")
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        insert_sql = f"""
        INSERT INTO revenue_drop_alerts (quarter, revenue, revenue_growth_percent)
        SELECT
            qtr::DATE,
            rev::NUMERIC,
            revenue_growth_percent::NUMERIC
        FROM get_quarterly_growth()
        WHERE revenue_growth_percent < -{threshold}
        AND qtr NOT IN (SELECT quarter FROM revenue_drop_alerts);
        """
        cur.execute(insert_sql)
        conn.commit()
        cur.close()
        conn.close()
        print("🚨 Revenue drop alerts logged successfully.")
    except Exception as e:
        print("❌ Failed to log alerts:", e)

# 🔁 Full ETL
def main_etl():
    print("🔁 Starting ETL process...")
    df = fetch_and_clean_data()
    load_data_to_postgres(df)
    log_revenue_drops()
    print("✅ ETL process completed successfully.")

# ▶️ Run
if __name__ == "__main__":
    main_etl()
