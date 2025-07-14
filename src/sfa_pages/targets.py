import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import format_currency

def show_sales_targets():
    """Sales Targets & Performance Management"""
    st.header("🎯 Sales Targets & Performance")
    
    tab1, tab2, tab3 = st.tabs(["Current Targets", "Performance Analytics", "Target History"])
    
    with tab1:
        st.subheader("Monthly Targets - July 2024")
        
        # Progress metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Sales Target",
                value=format_currency(50000000, 'IDR'),
                delta=f"{format_currency(35000000, 'IDR')} achieved (70%)"
            )
        
        with col2:
            st.metric(
                label="Visit Target",
                value="20 visits",
                delta="15 completed (75%)"
            )
        
        with col3:
            st.metric(
                label="Customer Target",
                value="10 new customers",
                delta="8 acquired (80%)"
            )
        
        with col4:
            st.metric(
                label="Conversion Rate",
                value="65%",
                delta="15% above target"
            )
        
        # Progress bars
        st.markdown("---")
        st.subheader("Progress Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sales progress
            sales_progress = 70
            st.markdown(f"**Sales Progress: {sales_progress}%**")
            st.progress(sales_progress / 100)
            
            # Visits progress
            visits_progress = 75
            st.markdown(f"**Visits Progress: {visits_progress}%**")
            st.progress(visits_progress / 100)
        
        with col2:
            # Customers progress
            customers_progress = 80
            st.markdown(f"**New Customers Progress: {customers_progress}%**")
            st.progress(customers_progress / 100)
            
            # Overall progress
            overall_progress = (sales_progress + visits_progress + customers_progress) / 3
            st.markdown(f"**Overall Progress: {overall_progress:.0f}%**")
            st.progress(overall_progress / 100)
    
    with tab2:
        st.subheader("Performance Analytics")
        
        # Monthly performance chart
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
        targets = [45000000, 48000000, 50000000, 52000000, 50000000, 55000000, 50000000]
        achieved = [43000000, 49000000, 48000000, 54000000, 52000000, 53000000, 35000000]  # July in progress
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=targets, mode='lines+markers', name='Target', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=months, y=achieved, mode='lines+markers', name='Achieved', line=dict(color='green')))
        
        fig.update_layout(
            title="Monthly Sales Performance",
            xaxis_title="Month",
            yaxis_title="Sales (IDR)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance by customer type
        col1, col2 = st.columns(2)
        
        with col1:
            customer_types = ['New Customers', 'Existing Customers', 'Returning Customers']
            sales_by_type = [15000000, 18000000, 7000000]
            
            fig_pie = px.pie(values=sales_by_type, names=customer_types, title="Sales by Customer Type")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Top performing products
            products = ['Laptop Pro', 'Monitor Stand', 'Keyboard', 'Mouse', 'USB Cable']
            product_sales = [20000000, 8000000, 5000000, 1500000, 500000]
            
            fig_bar = px.bar(x=products, y=product_sales, title="Top Performing Products")
            fig_bar.update_layout(xaxis_title="Products", yaxis_title="Sales (IDR)")
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab3:
        st.subheader("Target History")
        
        target_history = {
            'Period': ['Jul 2024', 'Jun 2024', 'May 2024', 'Apr 2024', 'Mar 2024'],
            'Sales Target': [format_currency(50000000, 'IDR'), format_currency(55000000, 'IDR'), format_currency(50000000, 'IDR'), format_currency(52000000, 'IDR'), format_currency(50000000, 'IDR')],
            'Sales Achieved': [format_currency(35000000, 'IDR'), format_currency(53000000, 'IDR'), format_currency(52000000, 'IDR'), format_currency(54000000, 'IDR'), format_currency(48000000, 'IDR')],
            'Achievement %': ['70%', '96%', '104%', '104%', '96%'],
            'Visit Target': ['20', '25', '20', '22', '20'],
            'Visits Done': ['15', '24', '21', '23', '19'],
            'Status': ['🟡 In Progress', '✅ Achieved', '✅ Exceeded', '✅ Exceeded', '✅ Achieved']
        }
        
        df_targets = pd.DataFrame(target_history)
        st.dataframe(df_targets, use_container_width=True)
