import streamlit as st
import pandas as pd
from utils.helpers import format_currency

def show_products():
    """Product Management Page"""
    st.header("📦 Product Management")
    
    tab1, tab2, tab3 = st.tabs(["Product List", "Add New Product", "Categories"])
    
    with tab1:
        # Sample product data
        products_data = {
            'SKU': ['PRD001', 'PRD002', 'PRD003', 'PRD004', 'PRD005'],
            'Name': ['Laptop Pro', 'Wireless Mouse', 'USB Cable', 'Monitor Stand', 'Keyboard'],
            'Category': ['Electronics', 'Accessories', 'Cables', 'Furniture', 'Input Devices'],
            'Price': [format_currency(14999000, 'IDR'), format_currency(449000, 'IDR'), format_currency(149000, 'IDR'), format_currency(749000, 'IDR'), format_currency(1199000, 'IDR')],
            'Stock': [25, 150, 200, 45, 80],
            'Status': ['✅ In Stock', '✅ In Stock', '✅ In Stock', '⚠️ Low Stock', '✅ In Stock']
        }
        
        df = pd.DataFrame(products_data)
        
        # Search and filter
        col1, col2, col3 = st.columns(3)
        with col1:
            search = st.text_input("🔍 Search products", placeholder="Enter product name or SKU")
        with col2:
            category_filter = st.selectbox("Filter by Category", ["All", "Electronics", "Accessories", "Cables", "Furniture", "Input Devices"])
        with col3:
            stock_filter = st.selectbox("Filter by Stock", ["All", "In Stock", "Low Stock", "Out of Stock"])
        
        # Apply filters (simplified for demo)
        filtered_df = df
        if search:
            filtered_df = df[df['Name'].str.contains(search, case=False) | df['SKU'].str.contains(search, case=False)]
        
        st.dataframe(filtered_df, use_container_width=True)
        
        # Product actions
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📊 Stock Report"):
                st.info("Stock report feature coming soon!")
        with col2:
            if st.button("📦 Bulk Update"):
                st.info("Bulk update feature coming soon!")
        with col3:
            if st.button("🏷️ Price Update"):
                st.info("Price update feature coming soon!")
        with col4:
            if st.button("📤 Export"):
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="products.csv",
                    mime="text/csv"
                )
    
    with tab2:
        st.subheader("Add New Product")
        with st.form("add_product"):
            col1, col2 = st.columns(2)
            with col1:
                sku = st.text_input("SKU", placeholder="e.g., PRD006")
                name = st.text_input("Product Name", placeholder="e.g., Wireless Keyboard")
                category = st.selectbox("Category", ["Electronics", "Accessories", "Cables", "Furniture", "Input Devices", "Software"])
            with col2:
                price = st.number_input("Price (IDR)", min_value=0, value=500000, step=10000)
                cost = st.number_input("Cost (IDR)", min_value=0, value=300000, step=10000)
                supplier = st.text_input("Supplier", placeholder="e.g., PT. Supplier Indonesia")
            
            description = st.text_area("Description", placeholder="Detailed product description")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                initial_stock = st.number_input("Initial Stock", min_value=0, value=50, step=1)
            with col2:
                min_stock = st.number_input("Minimum Stock Level", min_value=0, value=10, step=1)
            with col3:
                max_stock = st.number_input("Maximum Stock Level", min_value=0, value=200, step=1)
            
            # Product specifications
            st.subheader("Product Specifications")
            col1, col2 = st.columns(2)
            with col1:
                weight = st.number_input("Weight (kg)", min_value=0.0, value=0.5, step=0.1)
                dimensions = st.text_input("Dimensions (cm)", placeholder="L x W x H")
            with col2:
                warranty = st.selectbox("Warranty Period", ["No Warranty", "3 months", "6 months", "1 year", "2 years", "3 years"])
                barcode = st.text_input("Barcode", placeholder="Product barcode")
            
            if st.form_submit_button("Add Product", use_container_width=True):
                if sku and name and price > 0:
                    st.success(f"✅ Product '{name}' (SKU: {sku}) added successfully!")
                    st.balloons()
                else:
                    st.error("❌ Please fill in all required fields (SKU, Name, Price)")
    
    with tab3:
        st.subheader("Product Categories")
        
        # Display categories
        categories_data = {
            'Category': ['Electronics', 'Accessories', 'Cables', 'Furniture', 'Input Devices'],
            'Products': [1, 1, 1, 1, 1],
            'Total Value': [format_currency(14999000, 'IDR'), format_currency(449000, 'IDR'), format_currency(149000, 'IDR'), format_currency(749000, 'IDR'), format_currency(1199000, 'IDR')]
        }
        
        df_categories = pd.DataFrame(categories_data)
        st.dataframe(df_categories, use_container_width=True)
        
        # Add new category
        with st.form("add_category"):
            col1, col2 = st.columns(2)
            with col1:
                new_category = st.text_input("Category Name")
            with col2:
                category_description = st.text_input("Description")
            
            if st.form_submit_button("Add Category"):
                if new_category:
                    st.success(f"✅ Category '{new_category}' added successfully!")
                else:
                    st.error("❌ Please enter a category name")

def show_product_details(sku):
    """Show detailed product information"""
    st.subheader(f"Product Details - SKU: {sku}")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Details", "Stock History", "Sales", "Suppliers"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Product Information**")
            st.write("Name: Laptop Pro")
            st.write("SKU: PRD001")
            st.write("Category: Electronics")
            st.write("Price:", format_currency(14999000, 'IDR'))
        
        with col2:
            st.write("**Stock Information**")
            st.metric("Current Stock", "25")
            st.metric("Minimum Level", "10")
            st.metric("Maximum Level", "100")
    
    with tab2:
        st.write("Stock movement history will be displayed here")
    
    with tab3:
        st.write("Sales analytics for this product will be displayed here")
    
    with tab4:
        st.write("Supplier information and purchase history will be displayed here")
