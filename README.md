# E-Commerce Sales Performance & Insights

This repository contains the dataset and project guide for an end-to-end Data Analytics project leveraging Advanced Excel (Power Query, Pivot Tables, DAX, INDEX/MATCH) and Tableau. 

## Project Overview

**Objective**: Analyze multi-region e-commerce transaction data to uncover underperforming product categories, identify high-value customer segments, and provide actionable recommendations for inventory optimization.

**Tools Used**:
- **Microsoft Excel**: Data Cleaning (Power Query), Data Modeling, Financial Calculations (DAX, INDEX/MATCH, Pivot Tables)
- **Tableau**: Interactive Data Visualization, Storyboarding, Forecasting

## Dataset Details
- **File**: `raw_ecommerce_transactions.csv`
- **Volume**: 52,000+ transaction records.
- **Characteristics**: Contains raw data with intentional duplicates, missing values, and formatting inconsistencies to simulate real-world data engineering challenges.

## Step-by-Step Implementation Guide

### Phase 1: Data Cleaning & Structuring (Excel Power Query)
1. Open Excel and navigate to `Data` -> `Get Data` -> `From Text/CSV` to load `raw_ecommerce_transactions.csv`.
2. Click **Transform Data** to open the Power Query Editor.
3. **Remove Duplicates**: Select the `Transaction_ID` column, right-click, and choose "Remove Duplicates" to normalize the schema.
4. **Handle Missing Values**: Filter out or impute blank values in `Customer_Segment` and `Cost_Price`.
5. **Clean Data Types**: Identify strings with `$` symbols in the `Selling_Price` column. Replace the `$` symbol and convert the column to a Decimal Number type.
6. **Load**: Close & Load the cleaned data into a new worksheet or directly into the Excel Data Model.

### Phase 2: Financial Modeling & Analysis (Excel)
1. **Profit Margin Calculations**: 
   - Add new calculated columns using DAX (if using Power Pivot) or standard formulas to calculate `Revenue`, `Total_Cost`, and `Profit`.
   - `Revenue = Selling_Price * Quantity * (1 - Discount)`
   - `Total_Cost = Cost_Price * Quantity`
   - `Profit = Revenue - Total_Cost`
2. **Advanced Lookups**: Use `INDEX/MATCH` combinations to map product categories against external reference tables (if you decide to expand the dataset with dimension tables).
3. **Pivot Tables**: 
   - Build a Pivot Table to analyze Profit by `Product_Category` and `Region`.
   - Identify underperforming product sub-categories based on negative or low profit margins.
   - Segment high-value customers by summing Revenue grouped by `Customer_Segment`.

### Phase 3: Interactive Dashboarding & Storyboarding (Tableau)
1. Connect Tableau Desktop/Public to the cleaned Excel file.
2. **Regional Heatmaps**: 
   - Drag `Country` or `Region` to the view and map `Profit` to color intensity. This reveals top-performing and underperforming regions.
3. **Seasonal Trend Lines & Forecasts**: 
   - Plot `Order_Date` (Continuous Month) against `Revenue`. 
   - Add a Tableau Forecast model to predict sales for the next 3-6 months.
4. **Customer & Product Segmentation**: 
   - Create bar charts or scatter plots detailing Sales vs. Profit across different `Product_Categories` and `Customer_Segments`.
5. **Storyboard**: 
   - Assemble these visualizations into a cohesive Tableau Storyboard, highlighting key insights and a narrative flow.

### Phase 4: Actionable Recommendations
Based on the analysis, draft a summary report concluding:
- Which regions require inventory reallocation due to high sales velocity.
- Which product categories should be discontinued or remarketed due to low margins.
- Marketing strategies tailored to the "Corporate" or "Consumer" segments based on their purchasing behavior.
