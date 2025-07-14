import streamlit as st
import pandas as pd
from utils.helpers import format_currency
from utils.translations import t

def show_customers():
    """Customer Management Page"""
    st.header(f"👥 {t('customers')}")
    
    tab1, tab2 = st.tabs([t("customer_list"), t("add_customer")])
    
    with tab1:
        # Sample customer data with Indonesian FMCG context
        customers_data = {
            'ID': [1, 2, 3, 4, 5, 6, 7, 8],
            'Name': ['Toko Sari Rasa', 'Warung Maju Jaya', 'Supermarket Harapan', 'Toko Berkah', 
                    'Minimarket Sejahtera', 'Toko Makmur', 'Warung Bu Siti', 'Toko Sembako Jaya'],
            'Owner': ['Budi Santoso', 'Sari Wulandari', 'Ahmad Rahman', 'Dewi Kusuma', 
                     'Rizki Pratama', 'Maya Sari', 'Siti Nurhaliza', 'Joko Widodo'],
            'Phone': ['+62812-3456-7890', '+62813-4567-8901', '+62814-5678-9012', '+62815-6789-0123', 
                     '+62816-7890-1234', '+62817-8901-2345', '+62818-9012-3456', '+62819-0123-4567'],
            'Type': ['Retail', 'Warung', 'Supermarket', 'Retail', 'Minimarket', 'Retail', 'Warung', 'Retail'],
            'Total Orders': [15, 8, 23, 12, 6, 18, 9, 14],
            'Total Spent': [
                format_currency(81000000, 'IDR'), format_currency(42000000, 'IDR'), 
                format_currency(133500000, 'IDR'), format_currency(63000000, 'IDR'), 
                format_currency(27000000, 'IDR'), format_currency(95000000, 'IDR'),
                format_currency(38000000, 'IDR'), format_currency(72000000, 'IDR')
            ],
            'Outstanding': [
                format_currency(0, 'IDR'), format_currency(520000, 'IDR'), 
                format_currency(5420000, 'IDR'), format_currency(0, 'IDR'), 
                format_currency(1500000, 'IDR'), format_currency(0, 'IDR'),
                format_currency(0, 'IDR'), format_currency(850000, 'IDR')
            ]
        }
        
        df = pd.DataFrame(customers_data)
        
        # Search and filter
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input(f"🔍 {t('search')} {t('customers')}", 
                                      placeholder=f"{t('customer_name')} atau owner")
        with col2:
            type_filter = st.selectbox(f"{t('filter')} {t('customer_type')}", 
                                     [t("all"), "Retail", "Warung", "Supermarket", "Minimarket"])
        with col3:
            outstanding_filter = st.selectbox("Filter Outstanding", 
                                            [t("all"), "Has Outstanding", "No Outstanding"])
        
        # Apply filters
        filtered_df = df
        if search_term:
            filtered_df = df[
                df['Name'].str.contains(search_term, case=False) | 
                df['Owner'].str.contains(search_term, case=False)
            ]
        if type_filter != t("all"):
            filtered_df = filtered_df[filtered_df['Type'] == type_filter]
        if outstanding_filter == "Has Outstanding":
            filtered_df = filtered_df[~filtered_df['Outstanding'].str.contains('Rp0')]
        elif outstanding_filter == "No Outstanding":
            filtered_df = filtered_df[filtered_df['Outstanding'].str.contains('Rp0')]
        
        st.dataframe(filtered_df, use_container_width=True)
        
        # Customer actions
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📊 View Analytics"):
                st.info("Customer analytics feature coming soon!")
        with col2:
            if st.button("📧 Send Email"):
                st.info("Email feature coming soon!")
        with col3:
            if st.button("� Payment Reminder"):
                st.info("Payment reminder feature coming soon!")
        with col4:
            if st.button("�📤 Export Data"):
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="customers.csv",
                    mime="text/csv"
                )
    
    with tab2:
        st.subheader(t("add_customer"))
        with st.form("add_customer"):
            # Basic information
            st.markdown(f"### 📋 Basic Information")
            col1, col2 = st.columns(2)
            with col1:
                store_name = st.text_input(t("customer_name"), placeholder="e.g., Toko Berkah Jaya")
                owner_name = st.text_input("Owner Name", placeholder="e.g., Budi Santoso")
                phone = st.text_input(t("phone"), placeholder="e.g., +62812-3456-7890")
            with col2:
                email = st.text_input(t("email"), placeholder="e.g., toko@email.co.id")
                customer_type = st.selectbox(t("customer_type"), 
                                           ["Retail", "Warung", "Supermarket", "Minimarket", "Wholesaler"])
                customer_code = st.text_input(t("customer_code"), 
                                            placeholder="Auto-generated if empty")
            
            # Address information
            st.markdown(f"### 📍 Address Information")
            col1, col2 = st.columns(2)
            with col1:
                address = st.text_area(t("address"), 
                                     placeholder="Jl. Raya No. 123, RT/RW 001/002")
                city = st.text_input(t("city"), placeholder="e.g., Jakarta, Surabaya, Bandung")
            with col2:
                district = st.text_input("District/Kecamatan", placeholder="e.g., Kemayoran")
                postal_code = st.text_input("Postal Code", placeholder="e.g., 12345")
            
            # Business information
            st.markdown(f"### 💼 Business Information")
            col1, col2 = st.columns(2)
            with col1:
                credit_limit = st.number_input(t("credit_limit") + " (IDR)", 
                                             min_value=0, value=5000000, step=500000)
                payment_terms = st.selectbox(t("payment_terms"), 
                                           ["Cash", "Net 7", "Net 15", "Net 30", "Net 45"])
            with col2:
                assigned_salesman = st.selectbox("Assigned Salesman", 
                                               ["Budi Santoso", "Ahmad Rahman", "Sari Wulandari", 
                                                "Dewi Kusuma", "Rizki Pratama"])
                preferred_delivery = st.selectbox("Preferred Delivery Day", 
                                                ["Any Day", "Monday", "Tuesday", "Wednesday", 
                                                 "Thursday", "Friday", "Saturday"])
            
            # Additional information
            notes = st.text_area("Notes", 
                                placeholder="Additional customer information, special requirements, etc.")
            
            if st.form_submit_button(t("add_customer"), use_container_width=True):
                if store_name and owner_name and phone:
                    st.success(f"✅ {t('customer_added')} '{store_name}'!")
                    st.balloons()
                else:
                    st.error(f"❌ {t('error')}: Please fill in store name, owner name, and phone")

def show_customer_details(customer_id):
    """Show detailed customer information"""
    st.subheader(f"Customer Details - ID: {customer_id}")
    
    # Customer info tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Profile", "Orders", "Payments", "Activities"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Basic Information**")
            st.write("Name: Budi Santoso")
            st.write("Email: budi@techcorp.co.id")
            st.write("Phone: +62812-3456-7890")
            st.write("Company: PT. Tech Corp")
        
        with col2:
            st.write("**Statistics**")
            st.metric("Total Orders", "15")
            st.metric("Total Spent", format_currency(81000000, 'IDR'))
            st.metric("Average Order", format_currency(5400000, 'IDR'))
    
    with tab2:
        st.write("Recent orders will be displayed here")
    
    with tab3:
        st.write("Payment history will be displayed here")
    
    with tab4:
        st.write("Customer activities and interactions will be displayed here")
