import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_visualizations(filepath):
    print("Loading data for visualizations...")
    df = pd.read_csv(filepath)
    
    # Quick cleaning
    df = df.drop_duplicates(subset=['Transaction_ID'])
    df['Selling_Price'] = df['Selling_Price'].astype(str).str.replace('$', '', regex=False).astype(float)
    df['Cost_Price'] = pd.to_numeric(df['Cost_Price'], errors='coerce')
    df['Cost_Price'].fillna(df['Cost_Price'].mean(), inplace=True)
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    
    # Financial metrics
    df['Net_Revenue'] = (df['Selling_Price'] * df['Quantity']) * (1 - df['Discount'])
    df['Profit'] = df['Net_Revenue'] - (df['Cost_Price'] * df['Quantity'])
    
    # Create directory for charts
    os.makedirs("visualizations", exist_ok=True)
    
    sns.set_theme(style="whitegrid")
    
    # 1. Regional Profit Heatmap (Bar chart as proxy)
    plt.figure(figsize=(10, 6))
    region_profit = df.groupby('Region')['Profit'].sum().reset_index()
    sns.barplot(data=region_profit, x='Region', y='Profit', hue='Region', palette='viridis', legend=False)
    plt.title('Total Profit by Region', fontsize=16)
    plt.ylabel('Total Profit ($)')
    plt.xlabel('Region')
    plt.tight_layout()
    plt.savefig('visualizations/regional_profit.png')
    print("Saved regional_profit.png")
    
    # 2. Seasonal Trend Line
    plt.figure(figsize=(12, 6))
    df_monthly = df.set_index('Order_Date').resample('ME')['Net_Revenue'].sum().reset_index()
    sns.lineplot(data=df_monthly, x='Order_Date', y='Net_Revenue', marker='o', color='b')
    plt.title('Monthly Sales Trend (Seasonality & Forecast proxy)', fontsize=16)
    plt.ylabel('Net Revenue ($)')
    plt.xlabel('Date')
    plt.tight_layout()
    plt.savefig('visualizations/seasonal_trend.png')
    print("Saved seasonal_trend.png")
    
    # 3. Product Category Profit Margins (Segmentation)
    plt.figure(figsize=(10, 6))
    category_summary = df.groupby('Product_Category').agg({'Net_Revenue': 'sum', 'Profit': 'sum'}).reset_index()
    category_summary['Margin'] = (category_summary['Profit'] / category_summary['Net_Revenue']) * 100
    sns.barplot(data=category_summary, x='Product_Category', y='Margin', hue='Product_Category', palette='magma', legend=False)
    plt.title('Profit Margin by Product Category', fontsize=16)
    plt.ylabel('Profit Margin (%)')
    plt.xlabel('Category')
    plt.tight_layout()
    plt.savefig('visualizations/category_margins.png')
    print("Saved category_margins.png")

if __name__ == "__main__":
    try:
        create_visualizations("raw_ecommerce_transactions.csv")
        print("All visualizations generated successfully in the 'visualizations' folder.")
    except ImportError:
        print("Please install pandas, matplotlib, and seaborn (pip install pandas matplotlib seaborn) to run this script.")
    except Exception as e:
        print(f"Error generating visuals: {e}")
