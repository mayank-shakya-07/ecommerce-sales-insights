# Tableau Storyboard Build Guide

This document outlines the exact steps to build the interactive Tableau Storyboard mentioned in your portfolio project, utilizing the `raw_ecommerce_transactions.csv` (or the cleaned Excel version).

## Step 1: Connect to Data & Prepare
1. Open Tableau Desktop or Tableau Public.
2. Select **Connect -> To a File -> Text file** (or Microsoft Excel if you saved the Power Query output).
3. Ensure Tableau correctly identifies `Order_Date` as a Date data type, and the geographic fields (`Country`, `Region`) as geographical roles.
4. *Optional*: Create a calculated field for Profit Margin if you didn't do it in Excel:
   - **Name**: `Profit Margin %`
   - **Formula**: `SUM([Profit]) / SUM([Net_Revenue])`
   - **Format**: Change Default Properties -> Number Format to Percentage.

---

## Step 2: Build the Individual Sheets

### Sheet 1: Regional Profit Heatmap
*Uncover underperforming regions.*
- **Map Layer**: Double click `Country` to generate a map.
- **Color**: Drag `Profit` to the Color mark. Change the color palette to Red-Green Diverging so negative profits (if any) are highlighted in red.
- **Label**: Drag `Region` and `Profit` to the Label mark.
- **Tooltip**: Add `Net_Revenue` and `Profit Margin %` to the Tooltip to provide more context on hover.

### Sheet 2: Seasonal Trend Lines & Forecasts
*Identify seasonal spikes and predict future sales.*
- **Columns**: Right-click and drag `Order_Date` to Columns. Select the continuous **Month(Order_Date)** (the green pill).
- **Rows**: Drag `Net_Revenue` to Rows.
- **Analytics Pane**: 
  - Drag a **Trend Line** onto the view (Linear).
  - Drag a **Forecast** onto the view. Tableau will automatically predict the next few months based on the historical seasonality.

### Sheet 3: Category Performance Matrix
*Identify underperforming product categories.*
- **Columns**: Drag `Product_Category` to Columns.
- **Rows**: Drag `Profit Margin %` to Rows.
- **Color**: Drag `Profit Margin %` to Color. Set a threshold where anything below 15% is marked orange/red.
- **Detail**: Drag `Product_SubCategory` to Detail, changing the mark type to a Circle or Bar to see the breakdown within each category.

### Sheet 4: Customer Segment Contribution
*Find high-value customer segments.*
- **Columns**: Drag `Customer_Segment` to Columns.
- **Rows**: Drag `Net_Revenue` and `Profit` to Rows (Dual Axis).
- **Format**: Synchronize the axes, make Revenue a Bar chart and Profit a Line chart or Circle.

---

## Step 3: Assemble the Storyboard / Dashboard
1. Create a new **Dashboard** (size: Automatic or 1200x800).
2. Drag **Sheet 1 (Map)** to the top half of the dashboard.
3. Drag **Sheet 2 (Trend Line)** to the bottom left.
4. Drag **Sheet 3 (Category Matrix)** to the bottom right.
5. **Add Interactivity (Filters)**: 
   - Click the Map sheet on the dashboard and select the **"Use as Filter"** funnel icon. Now, when a user clicks a country, the trend lines and category margins will update to show only that country's data!
   - Add a Quick Filter for `Order_Date` (Year/Quarter) and `Customer_Segment`. Apply them to all worksheets.

## Step 4: Publish
- Go to **Server -> Tableau Public -> Save to Tableau Public**.
- Add the link to the published dashboard directly in your GitHub `README.md` and on your resume!
