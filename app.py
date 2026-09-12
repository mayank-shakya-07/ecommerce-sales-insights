import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-Commerce Sales Dashboard", page_icon="📊", layout="wide")

# Title and Description
st.title("📊 E-Commerce Sales Performance & Insights")
st.markdown("An interactive dashboard built to analyze multi-region transactional data, uncover underperforming product categories, and identify high-value customer segments.")

# Data Loading with Caching for performance
@st.cache_data
def load_data():
    df = pd.read_csv("raw_ecommerce_transactions.csv")
    df = df.drop_duplicates(subset=['Transaction_ID'])
    df['Selling_Price'] = df['Selling_Price'].astype(str).str.replace('$', '', regex=False).astype(float)
    df['Cost_Price'] = pd.to_numeric(df['Cost_Price'], errors='coerce')
    df['Cost_Price'].fillna(df['Cost_Price'].mean(), inplace=True)
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    
    # Financial Metrics
    df['Net_Revenue'] = (df['Selling_Price'] * df['Quantity']) * (1 - df['Discount'])
    df['Total_Cost'] = df['Cost_Price'] * df['Quantity']
    df['Profit'] = df['Net_Revenue'] - df['Total_Cost']
    
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Dashboard Filters")
selected_region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
selected_segment = st.sidebar.multiselect("Select Customer Segment", options=df['Customer_Segment'].dropna().unique(), default=df['Customer_Segment'].dropna().unique())

# Filter the dataframe based on selection
filtered_df = df[(df['Region'].isin(selected_region)) & (df['Customer_Segment'].isin(selected_segment))]

# --- High Level KPIs ---
st.markdown("### 📈 High-Level KPIs")
col1, col2, col3, col4 = st.columns(4)
total_revenue = filtered_df['Net_Revenue'].sum()
total_profit = filtered_df['Profit'].sum()
profit_margin = (total_profit / total_revenue) * 100 if total_revenue > 0 else 0
total_orders = filtered_df['Transaction_ID'].nunique()

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Profit Margin", f"{profit_margin:.1f}%")
col4.metric("Total Orders", f"{total_orders:,}")
st.divider()

# --- Visualizations ---
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### Profit by Region")
    region_profit = filtered_df.groupby('Region')['Profit'].sum().reset_index()
    fig_region = px.bar(region_profit, x='Region', y='Profit', color='Region', text_auto='.2s', title="Regional Profitability")
    st.plotly_chart(fig_region, use_container_width=True)

with col_right:
    st.markdown("#### Revenue by Customer Segment")
    segment_rev = filtered_df.groupby('Customer_Segment')['Net_Revenue'].sum().reset_index()
    fig_segment = px.pie(segment_rev, values='Net_Revenue', names='Customer_Segment', hole=0.4, title="Revenue Contribution by Segment")
    st.plotly_chart(fig_segment, use_container_width=True)

st.markdown("#### Seasonal Trend (Monthly Revenue)")
monthly_sales = filtered_df.set_index('Order_Date').resample('M')['Net_Revenue'].sum().reset_index()
fig_trend = px.line(monthly_sales, x='Order_Date', y='Net_Revenue', markers=True, title="Revenue Over Time")
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("#### Profit Margin by Product Category")
cat_summary = filtered_df.groupby('Product_Category').agg({'Net_Revenue': 'sum', 'Profit': 'sum'}).reset_index()
cat_summary['Margin_%'] = (cat_summary['Profit'] / cat_summary['Net_Revenue']) * 100
fig_cat = px.bar(cat_summary.sort_values('Margin_%'), x='Margin_%', y='Product_Category', orientation='h', color='Margin_%', color_continuous_scale='reds', title="Category Margins (Identifying Underperformers)")
st.plotly_chart(fig_cat, use_container_width=True)

# --- Data Table ---
with st.expander("🔍 View Raw Filtered Data"):
    st.dataframe(filtered_df[['Transaction_ID', 'Order_Date', 'Region', 'Product_Category', 'Net_Revenue', 'Profit']].head(100))
