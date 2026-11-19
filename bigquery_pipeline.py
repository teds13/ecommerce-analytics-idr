import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# 1. Konfigurasi Project, Dataset, dan File Kredensial JSON
PROJECT_ID = "ecommerce-analytics-id"
DATASET_ID = "ecommerce_idr"
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "bq-credentials.json")
EXCEL_PATH = os.path.join(os.path.dirname(__file__), "ecommerce_data_analyst_portfolio_idr.xlsx")

# 2. Autentikasi Service Account & Inisialisasi BigQuery Client
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
client = bigquery.Client(project=PROJECT_ID, credentials=credentials)

# 3. Pull Data & Feature Engineering (IDR)
df = pd.read_excel(EXCEL_PATH, sheet_name="Product_Data")
df["Total_Revenue_IDR"] = df["Final_Price_IDR"] * df["Units_Sold"]
df["Total_Profit_IDR"] = (df["Final_Price_IDR"] - df["Cost_Price_IDR"]) * df["Units_Sold"]

# Ringkasan per Kategori
category_report = df.groupby("Category", as_index=False).agg(
    Total_SKU=("SKU", "count"),
    Total_Units_Sold=("Units_Sold", "sum"),
    Total_Revenue_IDR=("Total_Revenue_IDR", "sum"),
    Total_Profit_IDR=("Total_Profit_IDR", "sum"),
    Avg_Rating=("Rating", "mean")
).sort_values(by="Total_Profit_IDR", ascending=False)

# 4. Push Data ke Tabel BigQuery (WRITE_TRUNCATE = timpa isi lama dengan data terbaru)
job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

products_table_id = f"{PROJECT_ID}.{DATASET_ID}.products_cleaned"
summary_table_id = f"{PROJECT_ID}.{DATASET_ID}.category_summary"

client.load_table_from_dataframe(df, products_table_id, job_config=job_config).result()
client.load_table_from_dataframe(category_report, summary_table_id, job_config=job_config).result()

print("Sukses! Data berhasil di-push ke BigQuery:")
print(f"- {products_table_id}")
print(f"- {summary_table_id}")