import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import format_currency

def show_inventory():
    """Inventory Management Page"""
    st.header("📊 Inventory Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Stock Overview", "Stock Movements", "Adjustments", "Alerts"])
    
    with tab1:
        # Inventory summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Products", "125", "5")
        with col2:
            st.metric("Low Stock Items", "8", "-2")
        with col3:
            st.metric("Out of Stock", "3", "1")
        with col4:
            st.metric("Total Value", format_currency(2500000000, 'IDR'), "8.5%")
        
        st.markdown("---")
        
        # Inventory table
        inventory_data = {
            'Product': ['Laptop Pro', 'Wireless Mouse', 'USB Cable', 'Monitor Stand', 'Keyboard'],
            'SKU': ['PRD001', 'PRD002', 'PRD003', 'PRD004', 'PRD005'],
            'Current Stock': [25, 150, 200, 5, 80],
            'Min Level': [10, 50, 100, 20, 30],
            'Max Level': [100, 300, 500, 100, 150],
            'Reorder Point': [15, 75, 150, 30, 45],
            'Value': [format_currency(374975000, 'IDR'), format_currency(67350000, 'IDR'), format_currency(29800000, 'IDR'), format_currency(3745000, 'IDR'), format_currency(95920000, 'IDR')],
            'Status': ['✅ Good', '✅ Good', '✅ Good', '⚠️ Low', '✅ Good']
        }
        
        df = pd.DataFrame(inventory_data)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Good", "Low", "Out of Stock"])
        with col2:
            category_filter = st.selectbox("Filter by Category", ["All", "Electronics", "Accessories", "Cables", "Furniture"])
        with col3:
            search = st.text_input("🔍 Search", placeholder="Product name or SKU")
        
        st.dataframe(df, use_container_width=True)
        
        # Stock level chart
        st.subheader("Stock Levels Visualization")
        fig = px.bar(df, x='Product', y='Current Stock', color='Status', 
                     title="Current Stock Levels by Product",
                     color_discrete_map={'✅ Good': 'green', '⚠️ Low': 'orange', '❌ Out': 'red'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Actions
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📦 Stock Take", use_container_width=True):
                st.info("Stock take feature coming soon!")
        with col2:
            if st.button("📋 Generate PO", use_container_width=True):
                st.info("Purchase order generation coming soon!")
        with col3:
            if st.button("📊 Stock Report", use_container_width=True):
                st.info("Stock report feature coming soon!")
        with col4:
            if st.button("📤 Export", use_container_width=True):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="inventory.csv",
                    mime="text/csv"
                )
    
    with tab2:
        st.subheader("Stock Movements")
        
        # Sample stock movements
        movements_data = {
            'Date': ['2024-01-20', '2024-01-19', '2024-01-18', '2024-01-17', '2024-01-16'],
            'Product': ['Laptop Pro', 'Wireless Mouse', 'USB Cable', 'Monitor Stand', 'Keyboard'],
            'Type': ['Sale', 'Purchase', 'Sale', 'Adjustment', 'Sale'],
            'Quantity': [-2, +50, -10, -1, -3],
            'Reference': ['ORD001', 'PO001', 'ORD002', 'ADJ001', 'ORD003'],
            'Balance': [25, 150, 200, 5, 80]
        }
        
        df_movements = pd.DataFrame(movements_data)
        st.dataframe(df_movements, use_container_width=True)
        
        # Movement chart
        st.subheader("Stock Movement Trend")
        movement_chart_data = pd.DataFrame({
            'Date': pd.date_range('2024-01-01', periods=20, freq='D'),
            'In': [10, 0, 50, 0, 20, 0, 0, 30, 0, 15, 0, 40, 0, 0, 25, 0, 10, 0, 35, 0],
            'Out': [5, 8, 3, 12, 6, 9, 4, 7, 10, 2, 11, 6, 8, 5, 3, 9, 7, 12, 4, 8]
        })
        
        fig_movement = px.line(movement_chart_data, x='Date', y=['In', 'Out'], 
                              title="Daily Stock Movements (In vs Out)")
        st.plotly_chart(fig_movement, use_container_width=True)
    
    with tab3:
        st.subheader("Stock Adjustments")
        
        # Create adjustment form
        with st.form("stock_adjustment"):
            col1, col2 = st.columns(2)
            with col1:
                product = st.selectbox("Product", ["Laptop Pro", "Wireless Mouse", "USB Cable", "Monitor Stand", "Keyboard"])
                adjustment_type = st.selectbox("Adjustment Type", ["Increase", "Decrease", "Set to Value"])
            
            with col2:
                quantity = st.number_input("Quantity", min_value=0, value=1)
                reason = st.selectbox("Reason", ["Damaged", "Lost", "Found", "Correction", "Transfer", "Other"])
            
            notes = st.text_area("Notes", placeholder="Detailed explanation for the adjustment")
            
            if st.form_submit_button("Submit Adjustment", use_container_width=True):
                st.success(f"✅ Stock adjustment for '{product}' submitted successfully!")
        
        st.markdown("---")
        
        # Recent adjustments
        st.subheader("Recent Adjustments")
        adjustments_data = {
            'Date': ['2024-01-20', '2024-01-18', '2024-01-15'],
            'Product': ['Monitor Stand', 'Laptop Pro', 'USB Cable'],
            'Type': ['Decrease', 'Decrease', 'Increase'],
            'Quantity': [-1, -1, +25],
            'Reason': ['Damaged', 'Lost', 'Found'],
            'By': ['Admin', 'Manager', 'Staff']
        }
        
        df_adjustments = pd.DataFrame(adjustments_data)
        st.dataframe(df_adjustments, use_container_width=True)
    
    with tab4:
        st.subheader("Inventory Alerts")
        
        # Alert summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.error("**Critical Alerts: 3**")
        with col2:
            st.warning("**Low Stock Alerts: 8**")
        with col3:
            st.info("**Reorder Alerts: 5**")
        
        # Detailed alerts
        alerts_data = {
            'Priority': ['🔴 Critical', '🟡 Low Stock', '🟡 Low Stock', '🔵 Reorder', '🔵 Reorder'],
            'Product': ['Monitor Stand', 'Wireless Headset', 'Power Bank', 'Laptop Pro', 'USB Cable'],
            'Current Stock': [5, 8, 12, 25, 200],
            'Min Level': [20, 15, 25, 10, 100],
            'Recommended Action': ['Immediate Purchase', 'Order Soon', 'Order Soon', 'Consider Reorder', 'Monitor'],
            'Supplier': ['OfficeSupply Ltd', 'AudioTech', 'PowerCorp', 'TechSupplier Inc', 'CableCorp']
        }
        
        df_alerts = pd.DataFrame(alerts_data)
        st.dataframe(df_alerts, use_container_width=True)
        
        # Alert actions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📧 Send Alert Emails", use_container_width=True):
                st.success("Alert emails sent to purchasing team!")
        with col2:
            if st.button("📋 Generate Purchase Orders", use_container_width=True):
                st.info("Automatic PO generation feature coming soon!")

def show_stock_details(product_sku):
    """Show detailed stock information for a specific product"""
    st.subheader(f"Stock Details - {product_sku}")
    
    tab1, tab2, tab3 = st.tabs(["Current Status", "Movement History", "Forecasting"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current Stock", "25")
            st.metric("Available Stock", "23")
            st.metric("Reserved Stock", "2")
        
        with col2:
            st.metric("Min Level", "10")
            st.metric("Max Level", "100")
            st.metric("Reorder Point", "15")
    
    with tab2:
        st.write("Detailed movement history will be displayed here")
    
    with tab3:
        st.write("Stock forecasting and demand planning will be displayed here")
