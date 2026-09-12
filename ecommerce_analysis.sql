-- ========================================================================
-- E-Commerce Sales Performance & Insights - SQL Analysis Script
-- ========================================================================
-- This script mirrors the Power Query, DAX, and Tableau logic using SQL.
-- It demonstrates how to perform data cleaning, financial modeling, 
-- and segmentation in a relational database (e.g., PostgreSQL, SQL Server).

-- ------------------------------------------------------------------------
-- Phase 1: Data Cleaning & Normalization (Simulating Power Query)
-- ------------------------------------------------------------------------

-- 1. Create a CTE or View to deduplicate the raw transaction records
--    and clean the formatting issues (e.g., removing '$' from prices).
CREATE OR REPLACE VIEW cleaned_transactions AS
WITH Deduplicated AS (
    SELECT 
        *,
        ROW_NUMBER() OVER(PARTITION BY Transaction_ID ORDER BY Order_Date DESC) as rn
    FROM raw_ecommerce_transactions
)
SELECT 
    Transaction_ID,
    CAST(Order_Date AS DATE) AS Order_Date,
    Customer_ID,
    COALESCE(NULLIF(Customer_Segment, ''), 'Unknown') AS Customer_Segment,
    Region,
    Country,
    Product_Category,
    Product_SubCategory,
    Product_Name,
    CAST(COALESCE(NULLIF(Cost_Price, ''), '0') AS DECIMAL(10,2)) AS Cost_Price,
    CAST(REPLACE(Selling_Price, '$', '') AS DECIMAL(10,2)) AS Selling_Price,
    Quantity,
    Discount
FROM Deduplicated
WHERE rn = 1;


-- ------------------------------------------------------------------------
-- Phase 2: Financial Modeling (Simulating DAX & standard Excel formulas)
-- ------------------------------------------------------------------------

-- 2. Create a comprehensive view calculating Gross Revenue, Net Revenue, Cost, and Profit
CREATE OR REPLACE VIEW financial_model AS
SELECT 
    Transaction_ID,
    Order_Date,
    Customer_Segment,
    Region,
    Country,
    Product_Category,
    Product_SubCategory,
    (Selling_Price * Quantity) AS Gross_Revenue,
    (Selling_Price * Quantity * (1 - Discount)) AS Net_Revenue,
    (Cost_Price * Quantity) AS Total_Cost,
    ((Selling_Price * Quantity * (1 - Discount)) - (Cost_Price * Quantity)) AS Profit
FROM cleaned_transactions;


-- ------------------------------------------------------------------------
-- Phase 3: Segmentation & Insights (Simulating Pivot Tables & Tableau)
-- ------------------------------------------------------------------------

-- Insight A: Underperforming Product Categories by Region
-- Objective: Uncover categories with low profit margins to optimize inventory.
SELECT 
    Region,
    Product_Category,
    SUM(Net_Revenue) AS Total_Revenue,
    SUM(Profit) AS Total_Profit,
    (SUM(Profit) / SUM(Net_Revenue)) * 100 AS Profit_Margin_Percent
FROM financial_model
GROUP BY 
    Region, 
    Product_Category
HAVING (SUM(Profit) / SUM(Net_Revenue)) < 0.15 -- Flagging margins under 15%
ORDER BY Profit_Margin_Percent ASC;


-- Insight B: High-Value Customer Segments
-- Objective: Identify which segments drive the most profit vs. volume.
SELECT 
    Customer_Segment,
    COUNT(DISTINCT Transaction_ID) AS Total_Orders,
    SUM(Net_Revenue) AS Total_Revenue,
    SUM(Profit) AS Total_Profit,
    (SUM(Net_Revenue) / COUNT(DISTINCT Transaction_ID)) AS Average_Order_Value
FROM financial_model
GROUP BY Customer_Segment
ORDER BY Total_Revenue DESC;


-- Insight C: Seasonal Trend Lines (Monthly Revenue & Profit)
-- Objective: Data prep for a Tableau time-series trend line.
SELECT 
    DATE_TRUNC('month', Order_Date) AS Sales_Month,
    SUM(Net_Revenue) AS Monthly_Revenue,
    SUM(Profit) AS Monthly_Profit
FROM financial_model
GROUP BY DATE_TRUNC('month', Order_Date)
ORDER BY Sales_Month ASC;

-- ========================================================================
-- End of Script
-- ========================================================================
