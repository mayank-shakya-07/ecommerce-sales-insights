import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# E-Commerce Sales Performance & Insights\n",
                "## Exploratory Data Analysis (EDA) & Data Cleaning\n",
                "This notebook replicates the Power Query and DAX analysis using Python and Pandas. It serves to showcase the ability to handle the same data engineering and financial modeling tasks programmatically."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "import warnings\n",
                "\n",
                "warnings.filterwarnings('ignore')\n",
                "sns.set_theme(style=\"whitegrid\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 1. Data Loading & Cleaning (Power Query Equivalent)\n",
                "First, we load the raw transactions, remove duplicates, and normalize the data types (e.g., converting `$25.00` strings to numeric floats)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Load raw data\n",
                "df = pd.read_csv('raw_ecommerce_transactions.csv')\n",
                "print(f\"Initial records: {len(df)}\")\n",
                "\n",
                "# Remove duplicates based on Transaction_ID\n",
                "df = df.drop_duplicates(subset=['Transaction_ID'])\n",
                "print(f\"Records after deduplication: {len(df)}\")\n",
                "\n",
                "# Clean Selling_Price (Remove '$' and convert to float)\n",
                "df['Selling_Price'] = df['Selling_Price'].astype(str).str.replace('$', '', regex=False).astype(float)\n",
                "\n",
                "# Impute missing Cost_Price with the mean\n",
                "df['Cost_Price'] = pd.to_numeric(df['Cost_Price'], errors='coerce')\n",
                "df['Cost_Price'].fillna(df['Cost_Price'].mean(), inplace=True)\n",
                "\n",
                "# Handle missing Customer Segments\n",
                "df['Customer_Segment'].fillna('Unknown', inplace=True)\n",
                "\n",
                "# Convert Order_Date to datetime\n",
                "df['Order_Date'] = pd.to_datetime(df['Order_Date'])\n",
                "\n",
                "df.head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 2. Financial Modeling (DAX / Calculated Columns Equivalent)\n",
                "Here we calculate Gross Revenue, Net Revenue (post-discount), Total Cost, and Profit."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "df['Gross_Revenue'] = df['Selling_Price'] * df['Quantity']\n",
                "df['Net_Revenue'] = df['Gross_Revenue'] * (1 - df['Discount'])\n",
                "df['Total_Cost'] = df['Cost_Price'] * df['Quantity']\n",
                "df['Profit'] = df['Net_Revenue'] - df['Total_Cost']\n",
                "\n",
                "total_revenue = df['Net_Revenue'].sum()\n",
                "total_profit = df['Profit'].sum()\n",
                "profit_margin = (total_profit / total_revenue) * 100\n",
                "\n",
                "print(f\"Total Revenue: ${total_revenue:,.2f}\")\n",
                "print(f\"Total Profit: ${total_profit:,.2f}\")\n",
                "print(f\"Overall Profit Margin: {profit_margin:.2f}%\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 3. Segmentation & Insights\n",
                "**Insight 1: Regional Profitability**"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "region_profit = df.groupby('Region')['Profit'].sum().reset_index().sort_values(by='Profit', ascending=False)\n",
                "plt.figure(figsize=(10, 5))\n",
                "sns.barplot(data=region_profit, x='Region', y='Profit', palette='viridis')\n",
                "plt.title('Total Profit by Region')\n",
                "plt.ylabel('Profit ($)')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "**Insight 2: Underperforming Product Categories**"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "cat_summary = df.groupby('Product_Category').agg({'Net_Revenue': 'sum', 'Profit': 'sum'}).reset_index()\n",
                "cat_summary['Margin_%'] = (cat_summary['Profit'] / cat_summary['Net_Revenue']) * 100\n",
                "cat_summary = cat_summary.sort_values(by='Margin_%')\n",
                "\n",
                "plt.figure(figsize=(10, 5))\n",
                "sns.barplot(data=cat_summary, x='Product_Category', y='Margin_%', palette='magma')\n",
                "plt.title('Profit Margin by Product Category')\n",
                "plt.ylabel('Profit Margin (%)')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "**Insight 3: Seasonal Trend Lines**"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "monthly_sales = df.set_index('Order_Date').resample('ME')['Net_Revenue'].sum().reset_index()\n",
                "plt.figure(figsize=(12, 5))\n",
                "sns.lineplot(data=monthly_sales, x='Order_Date', y='Net_Revenue', marker='o')\n",
                "plt.title('Monthly Sales Trend')\n",
                "plt.ylabel('Net Revenue ($)')\n",
                "plt.xlabel('Date')\n",
                "plt.show()"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.10"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open("ECommerce_Analysis.ipynb", "w") as f:
    json.dump(notebook, f, indent=2)

print("Jupyter Notebook created successfully.")
