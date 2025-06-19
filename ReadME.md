# 🚗 Tesla Revenue Analysis: Detecting Quarterly Declines with ETL + SQL Automation

## 📈 Case Study: Monitoring Tesla's Financial Performance with Data Engineering & SQL Analysis

 I designed this project to uncover and report **significant revenue drops** in Tesla’s quarterly financial data. By building a full **ETL pipeline** with **Python**, storing and analyzing the data in **PostgreSQL**, and creating a custom **SQL alerting system**, this case study replicates the type of real-time financial monitoring used by modern businesses and investors.

---

## 🎯 Business Problem

Tesla’s revenue figures are a major catalyst for market movements, investor confidence, and strategic decisions. But in a fast-paced world, how can businesses and analysts:

- Monitor revenue performance across quarters?
- Detect steep drops that may require executive attention?
- Automate financial insights to be delivered proactively?

---

## 💼 Objective

Create an automated analytics pipeline that:
- 📥 Collects Tesla’s public quarterly revenue data
- 🧼 Cleans, formats, and stores the data in a database
- 📊 Calculates quarter-over-quarter growth rates
- 🚨 Logs large revenue drops (≥15%) into an alert system using SQL
- 🧠 Surfaces business insights for timely decision-making

---

## 🧱 Tools and Technologies

| Tool         | Purpose                                 |
|--------------|------------------------------------------|
| Python       | Scripting, ETL process                  |
| Pandas       | Data cleaning & transformation          |
| SQLAlchemy   | Database connection layer               |
| psycopg2     | PostgreSQL adapter                      |
| PostgreSQL   | Data warehouse                          |
| SQL          | Revenue growth logic, alert logging     |
| dotenv       | Secure environment variable access      |

---

## 📦 Folder Structure

├── data/
│ └── raw/
│ └── tesla_quarterly_revenue.csv
├── scripts/
│ ├── web_scraper.py # Web scraping logic (if used)
│ ├── etl_pipeline.py # ETL flow, DB load, alert trigger
│ └── revenue_analysis.sql # SQL for revenue growth & alerts
├── .env # DB credentials (excluded in GitHub)
├── requirements.txt # Python dependencies
├── .gitignore
├── README.md # This file

pgsql
Copy
Edit

---

## 🚀 Step-by-Step Workflow

### 1️⃣ Data Acquisition & Web Scraping

The pipeline starts by gathering Tesla's quarterly revenue data from public sources using `pandas.read_html()` and/or manual exports. The result is saved to CSV for reproducibility and loading into the pipeline.

### 2️⃣ Data Cleaning with Python

The raw dataset included:
- Empty or missing revenue values
- Revenue figures with commas
- Inconsistent date formats

Using **Pandas**, I performed:
- Date parsing on the `Quarter` column → converted to `datetime`
- Numeric conversion of `Revenue` → removed commas, cast to `float`
- Renaming → `Quarter` → `qtr`, `Revenue` → `rev`

```python
df['Quarter'] = pd.to_datetime(df['Quarter'])
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
df.rename(columns={'Quarter': 'qtr', 'Revenue': 'rev'}, inplace=True)
3️⃣ Database Load with SQLAlchemy
Using SQLAlchemy, I connected to a local PostgreSQL database and pushed the cleaned data into a table called quarterly_revenue. This created a structured, queryable source of truth.

python
Copy
Edit
engine = create_engine(f'postgresql://{user}:{pwd}@localhost:5432/{db}')
df.to_sql('quarterly_revenue', engine, if_exists='replace', index=False)
4️⃣ Custom SQL Logic to Detect Revenue Drops
Once loaded, I used SQL window functions to calculate quarter-over-quarter revenue growth. Here's the heart of the SQL logic:

sql
Copy
Edit
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
This function calculates:

The revenue from the previous quarter

The percentage change in revenue

Flags quarters where revenue declined sharply

5️⃣ SQL-Powered Alert Table for Business Monitoring
I created a table revenue_drop_alerts to log drops over 15%, preventing duplicate entries for the same quarter:

sql
Copy
Edit
CREATE TABLE IF NOT EXISTS revenue_drop_alerts (
    quarter DATE PRIMARY KEY,
    revenue NUMERIC,
    revenue_growth_percent NUMERIC
);
Then, the following SQL block logs qualifying drops:

sql
Copy
Edit
INSERT INTO revenue_drop_alerts (quarter, revenue, revenue_growth_percent)
SELECT
    qtr,
    rev,
    revenue_growth_percent
FROM get_quarterly_growth()
WHERE revenue_growth_percent < -15
  AND qtr NOT IN (SELECT quarter FROM revenue_drop_alerts);
📊 Business Impact & Key Insight
In Q1 2025, Tesla experienced a 24.79% revenue decline, dropping from $25.7B to $19.3B. This was the largest drop in the dataset and triggered an alert in our PostgreSQL system.

This insight could signal:

Seasonal weakness (similar dip in Q1 2024)

External market headwinds

EV demand shifts or production bottlenecks

By surfacing this programmatically, stakeholders can act fast — whether that’s investors reassessing positions or analysts digging into product line-level metrics.

🔬 Technical Highlights
✅ Built a full ETL pipeline using Python and PostgreSQL

✅ Automated financial KPI monitoring with SQL functions

✅ Demonstrated data warehousing principles by staging and modeling data

✅ Practiced window functions and logic gates in PostgreSQL

✅ Secured credentials using .env variables

✅ Created modular, reusable code for enterprise-scale insights

📈 Future Enhancements
Add Tesla stock price time series to study correlation with revenue changes

Generate real-time dashboards in Tableau or Power BI

Send email/SMS alerts on drop detection using APIs

Add unit tests and CI/CD deployment to improve production-readiness

🧑‍💼 About the Analyst
Hi, I’m Jacsen White — a data analyst focused on using SQL, Python, and storytelling to deliver real insights from complex data.

This project reflects how I think about business problems:

🤖 Automate where possible

🧠 Focus on why, not just what

📣 Communicate insights to people, not just machines

yaml
Copy
Edit

---

### ✅ What to Do Next

Here’s how to get this project live on GitHub:

1. Save that case study as `README.md` in your project folder.
2. Create a `.gitignore` file and exclude:
.env
pycache/
*.pyc
venv/

sql
Copy
Edit
3. Push the full project folder to a new GitHub repo (name it something like `tesla-revenue-analysis`).
4. In your GitHub project settings, add a banner and fill in the “About” section using:
