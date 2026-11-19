import pandas as pd
import sqlalchemy

# 1. PULL DATA: Membaca dataset dari file Excel
file_path = "ecommerce_data_analyst_portfolio_idr.xlsx"
df = pd.read_excel(file_path, sheet_name="Product_Data")

# 2. DATA CLEANING & FEATURE ENGINEERING: Menambah kolom Total Revenue & Profit
df["Total_Revenue_IDR"] = df["Final_Price_IDR"] * df["Units_Sold"]
df["Total_Profit_IDR"] = (df["Final_Price_IDR"] - df["Cost_Price_IDR"]) * df["Units_Sold"]

# 3. EXPLORATORY ANALYSIS: Ringkasan performa per Kategori
category_report = df.groupby("Category").agg(
    Total_SKU=("SKU", "count"),
    Total_Units_Sold=("Units_Sold", "sum"),
    Total_Revenue_IDR=("Total_Revenue_IDR", "sum"),
    Total_Profit_IDR=("Total_Profit_IDR", "sum"),
    Avg_Rating=("Rating", "mean")
).reset_index()

# Urutkan berdasarkan keuntungan terbesar
category_report = category_report.sort_values(by="Total_Profit_IDR", ascending=False)
print("=== RINGKASAN PERFORMA KATEGORI ===")
print(category_report)

# 4. PUSH DATA: Simpan hasil olahan ke database SQLite lokal
engine = sqlalchemy.create_engine("sqlite:///ecommerce_store.db")
df.to_sql("products_cleaned", con=engine, if_exists="replace", index=False)
category_report.to_sql("category_summary", con=engine, if_exists="replace", index=False)

print("\nData berhasil di-push ke database 'ecommerce_store.db'!")