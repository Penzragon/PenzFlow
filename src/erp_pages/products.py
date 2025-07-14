import streamlit as st
import pandas as pd
from datetime import datetime
from utils.helpers import format_currency

def show_products():
    """Product Management Page for FMCG Business"""
    st.header("📦 Product Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Product List", "Add Product", "Variants & Pricing", "Categories"])
    
    with tab1:
        st.subheader("Product Catalog")
        
        # Search and filter
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search Products", placeholder="Product name or SKU")
        with col2:
            category_filter = st.selectbox("Filter by Category", ["All", "Beverages", "Snacks", "Dairy", "Personal Care", "Household"])
        with col3:
            status_filter = st.selectbox("Filter by Status", ["All", "Active", "Inactive", "Low Stock", "Out of Stock"])
        
        # FMCG product data with variants
        products_data = {
            'SKU': ['AQU001', 'AQU002', 'AQU003', 'IND001', 'IND002', 'CHT001', 'CHT002', 'SGR001'],
            'Product': ['Aqua 600ml', 'Aqua 1L', 'Aqua Galon 19L', 'Indomie Goreng', 'Indomie Soto', 'Chitato BBQ 68g', 'Chitato Sapi Panggang 68g', 'Gula Pasir 1kg'],
            'Brand': ['Aqua', 'Aqua', 'Aqua', 'Indomie', 'Indomie', 'Chitato', 'Chitato', 'Gulaku'],
            'Category': ['Beverages', 'Beverages', 'Beverages', 'Food', 'Food', 'Snacks', 'Snacks', 'Groceries'],
            'Unit Price (1pc)': [format_currency(3000, 'IDR'), format_currency(5000, 'IDR'), format_currency(25000, 'IDR'), format_currency(3500, 'IDR'), format_currency(3500, 'IDR'), format_currency(8000, 'IDR'), format_currency(8000, 'IDR'), format_currency(15000, 'IDR')],
            'Bulk Price (>50)': [format_currency(2700, 'IDR'), format_currency(4500, 'IDR'), format_currency(22000, 'IDR'), format_currency(3200, 'IDR'), format_currency(3200, 'IDR'), format_currency(7200, 'IDR'), format_currency(7200, 'IDR'), format_currency(13500, 'IDR')],
            'Stock': [1200, 800, 150, 2000, 1500, 500, 600, 300],
            'Status': ['✅ Active', '✅ Active', '⚠️ Low Stock', '✅ Active', '✅ Active', '✅ Active', '✅ Active', '⚠️ Low Stock']
        }
        
        df = pd.DataFrame(products_data)
        
        # Apply filters
        filtered_df = df
        if search_term:
            filtered_df = df[df['Product'].str.contains(search_term, case=False) | df['SKU'].str.contains(search_term, case=False)]
        if category_filter != "All":
            filtered_df = filtered_df[filtered_df['Category'] == category_filter]
        if status_filter != "All":
            if status_filter == "Low Stock":
                filtered_df = filtered_df[filtered_df['Status'].str.contains('Low Stock')]
            else:
                filtered_df = filtered_df[filtered_df['Status'].str.contains(status_filter)]
        
        st.dataframe(filtered_df, use_container_width=True)
        
        # Product actions
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📊 Stock Report"):
                st.info("Stock report feature coming soon!")
        with col2:
            if st.button("🏷️ Update Prices"):
                st.info("Price update feature coming soon!")
        with col3:
            if st.button("📦 Restock Alert"):
                st.info("Restock management feature coming soon!")
        with col4:
            if st.button("📤 Export Catalog"):
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="product_catalog.csv",
                    mime="text/csv"
                )
    
    with tab2:
        st.subheader("Add New Product")
        
        with st.form("add_product"):
            # Basic product information
            st.markdown("### Basic Information")
            col1, col2 = st.columns(2)
            
            with col1:
                product_name = st.text_input("Product Name", placeholder="e.g., Aqua")
                brand = st.text_input("Brand", placeholder="e.g., Aqua, Indomie")
                category = st.selectbox("Category", ["Beverages", "Snacks", "Dairy", "Personal Care", "Household", "Food", "Groceries"])
            
            with col2:
                sku = st.text_input("SKU", placeholder="e.g., AQU004")
                barcode = st.text_input("Barcode", placeholder="Product barcode")
                supplier = st.text_input("Supplier", placeholder="Supplier name")
            
            description = st.text_area("Product Description", placeholder="Detailed product description")
            
            # Product specifications
            st.markdown("### Product Specifications")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                weight = st.number_input("Weight (grams)", min_value=0, value=0, step=1)
                volume = st.text_input("Volume/Size", placeholder="e.g., 600ml, 1L, 68g")
            
            with col2:
                shelf_life = st.number_input("Shelf Life (days)", min_value=0, value=365, step=1)
                min_stock = st.number_input("Minimum Stock Level", min_value=0, value=50, step=1)
            
            with col3:
                max_stock = st.number_input("Maximum Stock Level", min_value=0, value=1000, step=1)
                initial_stock = st.number_input("Initial Stock", min_value=0, value=100, step=1)
            
            if st.form_submit_button("Add Product", use_container_width=True):
                if product_name and sku and brand:
                    st.success(f"✅ Product '{product_name}' (SKU: {sku}) added successfully!")
                    st.info("You can now add variants and pricing tiers in the 'Variants & Pricing' tab.")
                    st.balloons()
                else:
                    st.error("❌ Please fill in all required fields (Product Name, SKU, Brand)")
    
    with tab3:
        st.subheader("Product Variants & Pricing Tiers")
        
        # Select a product to manage variants
        col1, col2 = st.columns(2)
        with col1:
            selected_product = st.selectbox("Select Product to Manage", ["Aqua", "Indomie", "Chitato", "Gula Pasir"])
        with col2:
            st.info(f"Managing variants for: **{selected_product}**")
        
        # Existing variants
        if selected_product == "Aqua":
            variants_data = {
                'Variant': ['600ml', '1L', 'Galon 19L'],
                'SKU': ['AQU001', 'AQU002', 'AQU003'],
                'Unit Price': [format_currency(3000, 'IDR'), format_currency(5000, 'IDR'), format_currency(25000, 'IDR')],
                'Bulk Price (>50)': [format_currency(2700, 'IDR'), format_currency(4500, 'IDR'), format_currency(22000, 'IDR')],
                'Wholesale (>100)': [format_currency(2500, 'IDR'), format_currency(4200, 'IDR'), format_currency(20000, 'IDR')],
                'Stock': [1200, 800, 150]
            }
        else:
            variants_data = {
                'Variant': ['Sample Variant'],
                'SKU': ['SAMPLE001'],
                'Unit Price': [format_currency(5000, 'IDR')],
                'Bulk Price (>50)': [format_currency(4500, 'IDR')],
                'Wholesale (>100)': [format_currency(4000, 'IDR')],
                'Stock': [500]
            }
        
        df_variants = pd.DataFrame(variants_data)
        st.dataframe(df_variants, use_container_width=True)
        
        # Add new variant
        st.markdown("---")
        st.subheader("Add New Variant")
        
        with st.form("add_variant"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                variant_name = st.text_input("Variant Name", placeholder="e.g., 1.5L, 250ml")
                variant_sku = st.text_input("Variant SKU", placeholder="e.g., AQU004")
            
            with col2:
                unit_price = st.number_input("Unit Price (IDR)", min_value=0, value=5000, step=100)
                bulk_price = st.number_input("Bulk Price >50pcs (IDR)", min_value=0, value=4500, step=100)
            
            with col3:
                wholesale_price = st.number_input("Wholesale >100pcs (IDR)", min_value=0, value=4000, step=100)
                initial_stock = st.number_input("Initial Stock", min_value=0, value=100, step=1)
            
            variant_description = st.text_area("Variant Description", placeholder="Specific details about this variant")
            
            if st.form_submit_button("Add Variant", use_container_width=True):
                if variant_name and variant_sku:
                    st.success(f"✅ Variant '{variant_name}' added to {selected_product}!")
                else:
                    st.error("❌ Please fill in variant name and SKU")
        
        # Pricing tier management
        st.markdown("---")
        st.subheader("Pricing Tier Rules")
        
        pricing_rules = {
            'Tier': ['Unit Price', 'Bulk Price', 'Wholesale Price'],
            'Min Quantity': [1, 50, 100],
            'Discount %': ['0%', '10%', '20%'],
            'Description': ['Single unit purchase', 'Bulk purchase discount', 'Wholesale/distributor price']
        }
        
        df_pricing = pd.DataFrame(pricing_rules)
        st.dataframe(df_pricing, use_container_width=True)
        
        if st.button("🔧 Configure Pricing Rules"):
            st.info("Advanced pricing configuration feature coming soon!")
    
    with tab4:
        st.subheader("Product Categories")
        
        # Display categories
        categories_data = {
            'Category': ['Beverages', 'Snacks', 'Dairy', 'Personal Care', 'Household', 'Food', 'Groceries'],
            'Products': [3, 2, 0, 0, 0, 2, 1],
            'Total Value': [
                format_currency(75600000, 'IDR'),  # Aqua variants
                format_currency(12800000, 'IDR'),  # Chitato variants
                format_currency(0, 'IDR'),
                format_currency(0, 'IDR'),
                format_currency(0, 'IDR'),
                format_currency(14000000, 'IDR'),  # Indomie variants
                format_currency(4500000, 'IDR')    # Sugar
            ],
            'Avg Price': [
                format_currency(11000, 'IDR'),
                format_currency(8000, 'IDR'),
                format_currency(0, 'IDR'),
                format_currency(0, 'IDR'),
                format_currency(0, 'IDR'),
                format_currency(3500, 'IDR'),
                format_currency(15000, 'IDR')
            ]
        }
        
        df_categories = pd.DataFrame(categories_data)
        st.dataframe(df_categories, use_container_width=True)
        
        # Add new category
        st.markdown("---")
        st.subheader("Add New Category")
        
        with st.form("add_category"):
            col1, col2 = st.columns(2)
            
            with col1:
                category_name = st.text_input("Category Name", placeholder="e.g., Frozen Foods")
                category_code = st.text_input("Category Code", placeholder="e.g., FRZ")
            
            with col2:
                category_description = st.text_area("Description", placeholder="Category description")
            
            if st.form_submit_button("Add Category", use_container_width=True):
                if category_name and category_code:
                    st.success(f"✅ Category '{category_name}' added successfully!")
                else:
                    st.error("❌ Please fill in category name and code")
        
        # Category management
        st.markdown("---")
        st.subheader("Category Management")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊 Category Report"):
                st.info("Category performance report coming soon!")
        with col2:
            if st.button("🔄 Merge Categories"):
                st.info("Category merge feature coming soon!")
        with col3:
            if st.button("📤 Export Categories"):
                csv = df_categories.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="categories.csv",
                    mime="text/csv"
                )
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
