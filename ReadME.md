🚗 Tesla Revenue Analysis
Detecting Quarterly Declines with ETL + SQL Automation

Automated financial alert system for Tesla’s quarterly revenue using Python, PostgreSQL, and SQL.

📈 Case Study Overview
I designed this project to uncover and report significant revenue drops in Tesla’s financials using an automated ETL + SQL pipeline. The system:

Scrapes and cleans Tesla’s revenue data

Stores it in PostgreSQL

Detects >15% revenue drops via SQL logic

Logs alerts into a business-ready table for analysis

This simulates real-time financial monitoring used by businesses and investors.

🎯 Business Problem
Tesla’s quarterly revenue reports significantly influence investor sentiment, media coverage, and strategic decisions.

This project addresses:

📉 How to detect sharp revenue drops programmatically

🧠 How to automate business insights

🧾 How to store and monitor quarterly financial data with integrity

💼 Objective
✅ Build a full-stack data pipeline that:

Scrapes Tesla’s quarterly revenue data

Cleans & formats the data using Python (Pandas)

Loads data into a PostgreSQL database

Calculates quarter-over-quarter growth

Logs ≥15% revenue declines into a custom alert table

🧰 Tech Stack
Tool	Purpose
Python	Scripting, automation
Pandas	Data cleaning & transformation
SQLAlchemy	PostgreSQL connection layer
psycopg2	PostgreSQL database adapter
PostgreSQL	Data warehousing & analysis
SQL	Revenue growth logic & alerting
dotenv	Secure environment variable storage

📂 Folder Structure
tesla-revenue-analysis/
│
├── data/
│   └── raw/
│       └── tesla_quarterly_revenue.csv
│
├── scripts/
│   ├── fetch_tesla_revenue.py       # Scrapes Tesla revenue
│   ├── clean_and_plot_revenue.py    # Cleans data and plots revenue
│   └── etl_pipeline.py              # ETL + DB load + Alert logic
│
├── .env                             # DB credentials (excluded from GitHub)
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Ignored files and folders
└── README.md                        # This file

🚀 Workflow Breakdown
1️⃣ Data Acquisition (Web Scraping)
Tesla’s revenue data is collected via pandas.read_html() or manual export

Stored as CSV for reproducibility

2️⃣ Data Cleaning (Pandas)
df['Quarter'] = pd.to_datetime(df['Quarter'])
df['Revenue'] = pd.to_numeric(df['Revenue'].str.replace(',', ''), errors='coerce')
df.rename(columns={'Quarter': 'qtr', 'Revenue': 'rev'}, inplace=True)

3️⃣ Database Load (PostgreSQL via SQLAlchemy)
engine = create_engine(f'postgresql://{user}:{pwd}@localhost:5432/{db}')
df.to_sql('quarterly_revenue', engine, if_exists='replace', index=False)

4️⃣ SQL Function: Calculate Revenue Growth
CREATE OR REPLACE FUNCTION get_quarterly_growth()
RETURNS TABLE (
    qtr DATE,
    rev NUMERIC,
    prev_rev NUMERIC,
    revenue_growth_percent NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        qtr,
        rev,
        LAG(rev) OVER (ORDER BY qtr) AS prev_rev,
        ROUND(((rev - LAG(rev) OVER (ORDER BY qtr)) / LAG(rev) OVER (ORDER BY qtr)) * 100, 2) AS revenue_growth_percent
    FROM quarterly_revenue;
END;
$$ LANGUAGE plpgsql;

5️⃣ SQL Alert Table: Detect Large Drops
CREATE TABLE IF NOT EXISTS revenue_drop_alerts (
    quarter DATE PRIMARY KEY,
    revenue NUMERIC,
    revenue_growth_percent NUMERIC
);

INSERT INTO revenue_drop_alerts (quarter, revenue, revenue_growth_percent)
SELECT
    qtr,
    rev,
    revenue_growth_percent
FROM get_quarterly_growth()
WHERE revenue_growth_percent < -15
  AND qtr NOT IN (SELECT quarter FROM revenue_drop_alerts);

📊 Business Insight
In Q1 2025, Tesla's revenue dropped by 24.79%, falling from $25.7B → $19.3B.

This alert could signal:

⚠️ Seasonal demand shifts

📉 EV market headwinds

⚙️ Supply chain or production issues

By surfacing this drop automatically, stakeholders can take action faster.

🔍 Key Achievements
✅ Designed a full ETL + monitoring pipeline
✅ Leveraged SQL window functions for growth analysis
✅ Logged business-critical KPIs automatically
✅ Secured credentials with .env
✅ Demonstrated scalable and reusable code design

🔮 Future Improvements
📈 Integrate Tesla’s stock price for correlation analysis

📊 Build dashboards in Tableau or Power BI

📬 Send email or SMS alerts for real-time notifications

✅ Add unit tests and CI/CD for production-grade deployment

