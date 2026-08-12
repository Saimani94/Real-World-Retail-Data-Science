from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "retail_sales.csv"
REPORT_DIR = ROOT / "reports" / "plots"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    numeric_cols = ["quantity", "unit_price", "discount"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    df["revenue"] = df["quantity"] * df["unit_price"] * (1 - df["discount"])
    return df


def summarize(df: pd.DataFrame) -> None:
    print("\n=== DATASET OVERVIEW ===")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")
    print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"Missing values: {int(df.isna().sum().sum())}")
    print(f"Duplicate rows: {int(df.duplicated().sum())}")
    print(f"Total revenue: ₹{df['revenue'].sum():,.2f}")
    print(f"Units sold: {df['quantity'].sum():,.0f}")


def save_plots(df: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid")

    monthly = (
        df.assign(month=df["date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["revenue"]
        .sum()
    )
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=monthly, x="month", y="revenue", marker="o")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue (₹)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "monthly_revenue.png", dpi=160)
    plt.close()

    category = (
        df.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )
    plt.figure(figsize=(8, 5))
    sns.barplot(data=category, x="revenue", y="category")
    plt.title("Revenue by Category")
    plt.xlabel("Revenue (₹)")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "revenue_by_category.png", dpi=160)
    plt.close()

    region = (
        df.groupby("region", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )
    plt.figure(figsize=(8, 5))
    sns.barplot(data=region, x="region", y="revenue")
    plt.title("Revenue by Region")
    plt.xlabel("Region")
    plt.ylabel("Revenue (₹)")
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "revenue_by_region.png", dpi=160)
    plt.close()

    product = (
        df.groupby("product", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(8)
    )
    plt.figure(figsize=(9, 5))
    sns.barplot(data=product, x="revenue", y="product")
    plt.title("Top Products by Revenue")
    plt.xlabel("Revenue (₹)")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "top_products.png", dpi=160)
    plt.close()

    plt.figure(figsize=(7, 5))
    sns.scatterplot(data=df, x="discount", y="revenue", size="quantity", alpha=0.7, legend=False)
    plt.title("Discount vs Revenue")
    plt.xlabel("Discount")
    plt.ylabel("Revenue (₹)")
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "discount_vs_revenue.png", dpi=160)
    plt.close()


def create_report_tables(df: pd.DataFrame) -> None:
    monthly = (
        df.assign(month=df["date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)
        .agg(revenue=("revenue", "sum"), units=("quantity", "sum"))
    )
    category = df.groupby("category", as_index=False).agg(
        revenue=("revenue", "sum"), units=("quantity", "sum"), orders=("transaction_id", "nunique")
    )
    region = df.groupby("region", as_index=False).agg(
        revenue=("revenue", "sum"), units=("quantity", "sum"), orders=("transaction_id", "nunique")
    )
    customer = df.groupby("customer_id", as_index=False).agg(
        total_spend=("revenue", "sum"), units=("quantity", "sum"), orders=("transaction_id", "nunique")
    ).sort_values("total_spend", ascending=False)

    monthly.to_csv(ROOT / "reports" / "monthly_summary.csv", index=False)
    category.to_csv(ROOT / "reports" / "category_summary.csv", index=False)
    region.to_csv(ROOT / "reports" / "region_summary.csv", index=False)
    customer.to_csv(ROOT / "reports" / "customer_summary.csv", index=False)


def main() -> None:
    df = load_data()
    summarize(df)
    create_report_tables(df)
    save_plots(df)
    print("\nAnalysis complete. Tables saved to reports/ and charts saved to reports/plots/.")


if __name__ == "__main__":
    main()
