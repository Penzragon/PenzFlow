import streamlit as st
import pandas as pd
from datetime import datetime
from utils.helpers import format_currency

def show_expenses():
    """Expense Management for Sales Team"""
    st.header("💰 Expense Management")
    
    tab1, tab2, tab3 = st.tabs(["Submit Expense", "Pending Claims", "Expense History"])
    
    with tab1:
        st.subheader("Submit New Expense Claim")
        
        with st.form("expense_claim"):
            col1, col2 = st.columns(2)
            
            with col1:
                expense_date = st.date_input("Expense Date", value=datetime.now().date())
                expense_type = st.selectbox("Expense Type", ["Travel", "Meal", "Accommodation", "Fuel", "Parking", "Toll", "Other"])
                amount = st.number_input("Amount (IDR)", min_value=0, value=50000)
            
            with col2:
                customer_related = st.selectbox("Related to Customer", ["None", "PT. Teknologi Maju", "CV. Bisnis Sukses", "UD. Perdagangan Jaya"])
                visit_related = st.selectbox("Related to Visit", ["None", "Morning visit", "Afternoon visit"])
                receipt = st.file_uploader("Upload Receipt", type=['jpg', 'jpeg', 'png', 'pdf'])
            
            description = st.text_area("Description", placeholder="Describe the expense and its business purpose")
            
            if st.form_submit_button("📤 Submit Claim"):
                st.success(f"Expense claim for {format_currency(amount, 'IDR')} submitted successfully!")
    
    with tab2:
        st.subheader("Pending Expense Claims")
        
        pending_claims = {
            'Date': ['10-07-2024', '09-07-2024', '08-07-2024'],
            'Type': ['Travel', 'Meal', 'Fuel'],
            'Amount': [format_currency(100000, 'IDR'), format_currency(75000, 'IDR'), format_currency(150000, 'IDR')],
            'Description': ['Travel to customer site', 'Business lunch with client', 'Fuel for customer visits'],
            'Status': ['🟡 Pending', '🟡 Pending', '🟡 Pending'],
            'Submitted': ['2 days ago', '3 days ago', '4 days ago']
        }
        
        df_pending = pd.DataFrame(pending_claims)
        st.dataframe(df_pending, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Pending", format_currency(325000, 'IDR'))
        with col2:
            st.metric("Claims This Month", format_currency(850000, 'IDR'))
    
    with tab3:
        st.subheader("Expense History")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_type = st.selectbox("Expense Type", ["All", "Travel", "Meal", "Fuel", "Other"])
        with col2:
            filter_status = st.selectbox("Status", ["All", "Approved", "Pending", "Rejected"])
        with col3:
            filter_month = st.selectbox("Month", ["July 2024", "June 2024", "May 2024"])
        
        expense_history = {
            'Date': ['05-07-2024', '03-07-2024', '01-07-2024', '28-06-2024'],
            'Type': ['Travel', 'Meal', 'Fuel', 'Parking'],
            'Amount': [format_currency(120000, 'IDR'), format_currency(85000, 'IDR'), format_currency(200000, 'IDR'), format_currency(25000, 'IDR')],
            'Status': ['✅ Approved', '✅ Approved', '✅ Approved', '✅ Approved'],
            'Approved By': ['Manager Ahmad', 'Manager Ahmad', 'Manager Ahmad', 'Manager Ahmad'],
            'Paid Date': ['08-07-2024', '06-07-2024', '04-07-2024', '02-07-2024']
        }
        
        df_history = pd.DataFrame(expense_history)
        st.dataframe(df_history, use_container_width=True)
        
        # Summary
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("This Month", format_currency(1175000, 'IDR'))
        with col2:
            st.metric("Last Month", format_currency(950000, 'IDR'))
        with col3:
            st.metric("Average/Month", format_currency(1062500, 'IDR'))
        with col4:
            st.metric("YTD Total", format_currency(7437500, 'IDR'))
