import streamlit as st
import pandas as pd
from datetime import datetime
from utils.helpers import format_currency

def show_sales_activities():
    """Sales Activities Management"""
    st.header("📋 Sales Activities")
    
    tab1, tab2, tab3 = st.tabs(["Today's Activities", "Schedule Activity", "Activity History"])
    
    with tab1:
        st.subheader("Today's Planned Activities")
        
        activities_today = {
            'Time': ['09:00 WIB', '10:30 WIB', '13:00 WIB', '15:00 WIB'],
            'Type': ['📞 Call', '📧 Email', '🤝 Meeting', '📊 Proposal'],
            'Customer': ['PT. Teknologi Maju', 'CV. Bisnis Sukses', 'UD. Perdagangan Jaya', 'Toko Elektronik Sejahtera'],
            'Subject': ['Follow up quotation', 'Send product catalog', 'Contract discussion', 'Proposal presentation'],
            'Priority': ['🔴 High', '🟡 Medium', '🔴 High', '🟢 Low'],
            'Status': ['✅ Done', '⏳ Pending', '📅 Scheduled', '📅 Scheduled']
        }
        
        df_activities = pd.DataFrame(activities_today)
        st.dataframe(df_activities, use_container_width=True)
        
        # Quick actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📞 Start Next Call"):
                st.success("Initiating call to CV. Bisnis Sukses...")
        
        with col2:
            if st.button("✅ Mark as Complete"):
                st.success("Activity marked as complete!")
        
        with col3:
            if st.button("⏭️ Reschedule"):
                st.info("Opening reschedule dialog...")
    
    with tab2:
        st.subheader("Schedule New Activity")
        
        with st.form("new_activity"):
            col1, col2 = st.columns(2)
            
            with col1:
                activity_type = st.selectbox("Activity Type", ["Call", "Email", "Meeting", "Demo", "Proposal", "Follow-up"])
                customer = st.selectbox("Customer", ["PT. Teknologi Maju", "CV. Bisnis Sukses", "UD. Perdagangan Jaya"])
                activity_date = st.datetime_input("Date & Time")
                priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            
            with col2:
                subject = st.text_input("Subject")
                description = st.text_area("Description")
                reminder = st.selectbox("Reminder", ["15 minutes before", "30 minutes before", "1 hour before", "1 day before"])
            
            if st.form_submit_button("📅 Schedule Activity"):
                st.success("Activity scheduled successfully!")
    
    with tab3:
        st.subheader("Activity History & Results")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_type = st.selectbox("Activity Type", ["All", "Call", "Email", "Meeting", "Demo"])
        with col2:
            filter_customer = st.selectbox("Customer", ["All", "PT. Teknologi Maju", "CV. Bisnis Sukses"])
        with col3:
            date_range = st.selectbox("Date Range", ["Last 7 days", "Last 30 days", "Last 3 months"])
        
        activity_history = {
            'Date': ['10-07-2024', '09-07-2024', '08-07-2024', '05-07-2024'],
            'Type': ['Call', 'Meeting', 'Email', 'Demo'],
            'Customer': ['PT. Teknologi Maju', 'CV. Bisnis Sukses', 'UD. Perdagangan Jaya', 'Toko Elektronik Sejahtera'],
            'Subject': ['Product inquiry follow-up', 'Contract negotiation', 'Quotation sent', 'Product demonstration'],
            'Result': ['Interested, will decide next week', 'Contract signed', 'Waiting for approval', 'Very interested, requested proposal'],
            'Next Action': ['Follow up call', 'Delivery coordination', 'Follow up', 'Send proposal']
        }
        
        df_history = pd.DataFrame(activity_history)
        st.dataframe(df_history, use_container_width=True)
