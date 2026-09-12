import csv
import random
from datetime import datetime, timedelta
import uuid

def generate_ecommerce_data(filename, num_records=52000):
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America']
    countries_by_region = {
        'North America': ['USA', 'Canada', 'Mexico'],
        'Europe': ['UK', 'Germany', 'France', 'Italy', 'Spain'],
        'Asia Pacific': ['China', 'Japan', 'Australia', 'India'],
        'Latin America': ['Brazil', 'Argentina', 'Chile']
    }
    segments = ['Consumer', 'Corporate', 'Home Office']
    categories = {
        'Electronics': ['Laptops', 'Smartphones', 'Tablets', 'Accessories'],
        'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
        'Office Supplies': ['Paper', 'Binders', 'Art', 'Envelopes'],
        'Clothing': ['Men', 'Women', 'Kids', 'Shoes']
    }

    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 12, 31)
    days_range = (end_date - start_date).days

    records = []
    
    # Generate base records
    for i in range(num_records):
        tx_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        
        # Introduce some duplicates (about 2% of the time, we duplicate the previous transaction ID)
        if i > 0 and random.random() < 0.02:
            tx_id = records[-1][0]

        order_date = start_date + timedelta(days=random.randint(0, days_range))
        # Add seasonality: More sales in Nov/Dec
        if random.random() < 0.2:
            order_date = datetime(order_date.year, random.choice([11, 12]), random.randint(1, 28))

        customer_id = f"CUST-{random.randint(1000, 5000)}"
        segment = random.choices(segments, weights=[0.5, 0.3, 0.2])[0]
        
        region = random.choice(regions)
        country = random.choice(countries_by_region[region])
        
        category = random.choice(list(categories.keys()))
        sub_category = random.choice(categories[category])
        product_name = f"{sub_category} Model {random.randint(100, 999)}"
        
        cost_price = round(random.uniform(10.0, 500.0), 2)
        # 10% to 50% margin
        margin = random.uniform(1.1, 1.5)
        selling_price = round(cost_price * margin, 2)
        
        quantity = random.randint(1, 10)
        discount = round(random.choice([0.0, 0.0, 0.0, 0.05, 0.1, 0.15, 0.2]), 2)
        
        # Introduce data quality issues for Power Query to clean
        # Null values
        if random.random() < 0.01:
            segment = ""
        if random.random() < 0.01:
            cost_price = ""
            
        # Format issues
        str_selling_price = f"${selling_price}" if random.random() < 0.05 else selling_price
        
        records.append([
            tx_id,
            order_date.strftime("%Y-%m-%d"),
            customer_id,
            segment,
            region,
            country,
            category,
            sub_category,
            product_name,
            cost_price,
            str_selling_price,
            quantity,
            discount
        ])

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Transaction_ID", "Order_Date", "Customer_ID", "Customer_Segment", 
            "Region", "Country", "Product_Category", "Product_SubCategory", 
            "Product_Name", "Cost_Price", "Selling_Price", "Quantity", "Discount"
        ])
        writer.writerows(records)

if __name__ == "__main__":
    generate_ecommerce_data("raw_ecommerce_transactions.csv")
    print("Successfully generated 52,000+ records to raw_ecommerce_transactions.csv")
