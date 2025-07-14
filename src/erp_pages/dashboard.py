import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.helpers import format_currency

def show_dashboard():
    """Main ERP Dashboard"""
    st.header("📈 Dashboard Overview")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Sales",
            value=format_currency(1875450000, 'IDR'),  # ~$125,430 converted to IDR
            delta="12.5%"
        )
    
    with col2:
        st.metric(
            label="Active Customers",
            value="1,234",
            delta="8.2%"
        )
    
    with col3:
        st.metric(
            label="Products in Stock",
            value="456",
            delta="-2.1%"
        )
    
    with col4:
        st.metric(
            label="Pending Orders",
            value="23",
            delta="5.0%"
        )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sales Trend")
        # Sample data for sales trend
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        sales = [18000000, 22500000, 20250000, 27000000, 24750000, 28500000, 31500000, 27750000, 25500000, 33000000, 30750000, 37500000]
        
        fig = px.line(x=dates, y=sales, title="Monthly Sales Trend")
        fig.update_layout(xaxis_title="Month", yaxis_title="Sales (IDR)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top Products")
        products = ['Laptop Pro', 'Wireless Mouse', 'USB Cable', 'Monitor Stand', 'Keyboard']
        sales_data = [45, 30, 15, 7, 3]
        
        fig = px.pie(values=sales_data, names=products, title="Top Selling Products")
        st.plotly_chart(fig, use_container_width=True)
