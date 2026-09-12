import pandas as pd

def analyze_data(filepath):
    print("--- Loading and Cleaning Data ---")
    # Load data
    df = pd.read_csv(filepath)
    print(f"Initial raw records: {len(df)}")
    
    # 1. Clean Duplicates
    df = df.drop_duplicates(subset=['Transaction_ID'])
    print(f"Records after removing duplicate Transaction IDs: {len(df)}")
    
    # 2. Handle missing/dirty data
    # Remove '$' from Selling_Price and convert to float
    df['Selling_Price'] = df['Selling_Price'].astype(str).str.replace('$', '', regex=False).astype(float)
    
    # Fill missing Cost_Price with the average cost price (simple imputation)
    df['Cost_Price'] = pd.to_numeric(df['Cost_Price'], errors='coerce')
    df['Cost_Price'].fillna(df['Cost_Price'].mean(), inplace=True)
    
    # Fill missing segments
    df['Customer_Segment'].fillna('Unknown', inplace=True)
    
    print("Data cleaning complete.\n")
    
    print("--- Financial Modeling ---")
    # 3. Calculate Financial Metrics
    df['Gross_Revenue'] = df['Selling_Price'] * df['Quantity']
    df['Net_Revenue'] = df['Gross_Revenue'] * (1 - df['Discount'])
    df['Total_Cost'] = df['Cost_Price'] * df['Quantity']
    df['Profit'] = df['Net_Revenue'] - df['Total_Cost']
    df['Profit_Margin_%'] = (df['Profit'] / df['Net_Revenue']) * 100
    
    print(f"Total Revenue Generated: ${df['Net_Revenue'].sum():,.2f}")
    print(f"Total Profit Generated: ${df['Profit'].sum():,.2f}")
    print(f"Overall Profit Margin: {(df['Profit'].sum() / df['Net_Revenue'].sum() * 100):.2f}%\n")
    
    print("--- Segmentation Insights ---")
    # 4. Underperforming Product Categories
    category_profit = df.groupby('Product_Category')['Profit_Margin_%'].mean().sort_values()
    print("Average Profit Margin by Category:")
    print(category_profit.apply(lambda x: f"{x:.2f}%"))
    print()
    
    # 5. High-Value Customer Segments
    segment_revenue = df.groupby('Customer_Segment')['Net_Revenue'].sum().sort_values(ascending=False)
    print("Total Revenue by Customer Segment:")
    print(segment_revenue.apply(lambda x: f"${x:,.2f}"))
    print()
    
    # 6. Regional Performance
    region_profit = df.groupby('Region')['Profit'].sum().sort_values(ascending=False)
    print("Total Profit by Region (Heatmap Target):")
    print(region_profit.apply(lambda x: f"${x:,.2f}"))
    print()

if __name__ == "__main__":
    try:
        analyze_data("raw_ecommerce_transactions.csv")
    except ImportError:
        print("Pandas is not installed. Run 'pip install pandas' to execute this preview script.")
    except Exception as e:
        print(f"An error occurred: {e}")
