import streamlit as st
import pandas as pd
from utils.helpers import format_currency

def show_customers():
    """Customer Management Page"""
    st.header("👥 Customer Management")
    
    tab1, tab2 = st.tabs(["Customer List", "Add New Customer"])
    
    with tab1:
        # Sample customer data
        customers_data = {
            'ID': [1, 2, 3, 4, 5],
            'Name': ['Budi Santoso', 'Sari Wulandari', 'Ahmad Rahman', 'Dewi Kusuma', 'Rizki Pratama'],
            'Email': ['budi@techcorp.co.id', 'sari@bisnis.co.id', 'ahmad@services.co.id', 'dewi@solutions.co.id', 'rizki@enterprise.co.id'],
            'Phone': ['+62812-3456-7890', '+62813-4567-8901', '+62814-5678-9012', '+62815-6789-0123', '+62816-7890-1234'],
            'Total Orders': [15, 8, 23, 12, 6],
            'Total Spent': [format_currency(81000000, 'IDR'), format_currency(42000000, 'IDR'), format_currency(133500000, 'IDR'), format_currency(63000000, 'IDR'), format_currency(27000000, 'IDR')]
        }
        
        df = pd.DataFrame(customers_data)
        st.dataframe(df, use_container_width=True)
        
        # Customer actions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊 View Analytics"):
                st.info("Customer analytics feature coming soon!")
        with col2:
            if st.button("📧 Send Email"):
                st.info("Email feature coming soon!")
        with col3:
            if st.button("📤 Export Data"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="customers.csv",
                    mime="text/csv"
                )
    
    with tab2:
        st.subheader("Add New Customer")
        with st.form("add_customer"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Customer Name", placeholder="e.g., Budi Santoso")
                email = st.text_input("Email", placeholder="e.g., budi@company.co.id")
            with col2:
                phone = st.text_input("Phone", placeholder="e.g., +62812-3456-7890")
                company = st.text_input("Company", placeholder="e.g., PT. Tech Solutions")
            
            address = st.text_area("Address", placeholder="Complete address with city and postal code")
            
            col1, col2 = st.columns(2)
            with col1:
                customer_type = st.selectbox("Customer Type", ["Corporate", "Individual", "Government", "SME"])
            with col2:
                credit_limit = st.number_input("Credit Limit (IDR)", min_value=0, value=10000000, step=1000000)
            
            notes = st.text_area("Notes", placeholder="Additional customer information")
            
            if st.form_submit_button("Add Customer", use_container_width=True):
                if name and email and phone:
                    st.success(f"✅ Customer '{name}' added successfully!")
                    st.balloons()
                else:
                    st.error("❌ Please fill in all required fields (Name, Email, Phone)")

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
