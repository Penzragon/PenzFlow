import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
from utils.helpers import format_currency

def show_reports():
    """Reports & Analytics Page"""
    st.header("📋 Reports & Analytics")
    
    tab1, tab2, tab3 = st.tabs(["Sales Reports", "Inventory Reports", "Customer Reports"])
    
    with tab1:
        st.subheader("Sales Performance")
        
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=date(2024, 1, 1))
        with col2:
            end_date = st.date_input("End Date", value=date.today())
        
        # Sales metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Revenue", format_currency(678450000, 'IDR'), "15.2%")
        with col2:
            st.metric("Orders Completed", "156", "8.7%")
        with col3:
            st.metric("Average Order Value", format_currency(4350000, 'IDR'), "12.1%")
        
        # Sales chart
        dates = pd.date_range(start=start_date, end=end_date, freq='D')[:30]
        sales = [1200 + i*50 + (i%7)*200 for i in range(len(dates))]
        
        fig = px.line(x=dates, y=sales, title="Daily Sales Trend")
        st.plotly_chart(fig, use_container_width=True)
        
        # Export option
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📤 Export Sales Report"):
                st.info("Sales report export feature coming soon!")
        with col2:
            if st.button("📊 Generate Dashboard"):
                st.info("Dashboard generation feature coming soon!")
        with col3:
            if st.button("📧 Email Report"):
                st.info("Email report feature coming soon!")
    
    with tab2:
        st.subheader("Inventory Analysis")
        
        # Inventory turnover
        products = ['Laptop Pro', 'Wireless Mouse', 'USB Cable', 'Monitor Stand']
        turnover = [12, 8, 15, 6]
        
        fig = px.bar(x=products, y=turnover, title="Inventory Turnover Rate")
        fig.update_layout(xaxis_title="Products", yaxis_title="Turnover Rate")
        st.plotly_chart(fig, use_container_width=True)
        
        # Stock level analysis
        stock_data = {
            'Product': ['Laptop Pro', 'Wireless Mouse', 'USB Cable', 'Monitor Stand', 'Keyboard'],
            'Current Stock': [25, 150, 200, 5, 80],
            'Optimal Stock': [50, 200, 300, 75, 100],
            'Status': ['⚠️ Below Optimal', '✅ Good', '✅ Good', '❌ Critical', '✅ Good']
        }
        
        df_stock = pd.DataFrame(stock_data)
        st.dataframe(df_stock, use_container_width=True)
    
    with tab3:
        st.subheader("Customer Analytics")
        
        # Customer segments
        segments = ['New', 'Regular', 'VIP', 'Inactive']
        counts = [45, 120, 25, 15]
        
        fig = px.pie(values=counts, names=segments, title="Customer Segments")
        st.plotly_chart(fig, use_container_width=True)
        
        # Customer performance
        customer_data = {
            'Customer': ['PT. Teknologi Maju', 'CV. Bisnis Sukses', 'UD. Perdagangan Jaya', 'PT. Solusi Digital'],
            'Total Orders': [12, 8, 15, 6],
            'Total Value': [format_currency(150000000, 'IDR'), format_currency(80000000, 'IDR'), format_currency(200000000, 'IDR'), format_currency(60000000, 'IDR')],
            'Last Order': ['2024-01-15', '2024-01-10', '2024-01-18', '2024-01-08']
        }
        
        df_customers = pd.DataFrame(customer_data)
        st.dataframe(df_customers, use_container_width=True)
