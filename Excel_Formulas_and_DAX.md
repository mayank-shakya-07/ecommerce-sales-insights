# Excel Formulas and DAX Calculations Guide

This guide provides the exact formulas and DAX calculations you can use in your Excel workbook and Power Pivot Data Model to evaluate profit margins and segment the data.

## 1. Standard Excel Formulas (If not using Power Pivot)

If you are using standard Excel tables before pivoting, create the following helper columns:

**Gross Revenue**:
```excel
=[@[Selling_Price]] * [@[Quantity]]
```

**Net Revenue (After Discount)**:
```excel
=[@[Gross Revenue]] * (1 - [@[Discount]])
```

**Total Cost**:
```excel
=[@[Cost_Price]] * [@[Quantity]]
```

**Profit**:
```excel
=[@[Net Revenue]] - [@[Total Cost]]
```

**Profit Margin %**:
```excel
=[@Profit] / [@[Net Revenue]]
```

### Using INDEX/MATCH for Segmentation Lookup
If you want to simulate bringing in external dimension data (e.g., mapping a `Product_Category` to a specific `Warehouse_Manager`), you can use `INDEX/MATCH`. 

Assume you have a mapping table named `ManagerMap` on another sheet with columns `Category` and `Manager_Name`:
```excel
=INDEX(ManagerMap[Manager_Name], MATCH([@[Product_Category]], ManagerMap[Category], 0))
```

---

## 2. DAX Calculations (For Power Pivot / Power BI)

If you loaded the cleaned data from Power Query directly into the **Data Model**, use these DAX measures to build automated financial models.

**Total Revenue**:
```dax
Total Revenue := SUMX(
    Transactions, 
    Transactions[Selling_Price] * Transactions[Quantity] * (1 - Transactions[Discount])
)
```

**Total Cost**:
```dax
Total Cost := SUMX(
    Transactions, 
    Transactions[Cost_Price] * Transactions[Quantity]
)
```

**Total Profit**:
```dax
Total Profit := [Total Revenue] - [Total Cost]
```

**Profit Margin %**:
```dax
Profit Margin % := DIVIDE([Total Profit], [Total Revenue], 0)
```

**High-Value Customer Segmentation (Calculated Column)**:
You can flag transactions or customers as "High Value" if the revenue exceeds a certain threshold (e.g., $5,000).
```dax
Customer_Tier = 
IF(
    Transactions[Selling_Price] * Transactions[Quantity] >= 5000, 
    "High-Value (Tier 1)", 
    "Standard (Tier 2)"
)
```

## 3. Segmenting the Data with Pivot Tables

Once your measures are created:
1. **Rows**: `Region`, `Product_Category`
2. **Columns**: `Customer_Segment`
3. **Values**: `[Total Revenue]`, `[Profit Margin %]`

This setup will instantly highlight which region-category combinations are underperforming (e.g., yielding negative or < 10% margins).
