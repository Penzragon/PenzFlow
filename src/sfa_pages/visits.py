import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from utils.helpers import format_currency

def show_customer_visits():
    """Customer Visit Management"""
    st.header("🏃‍♂️ Customer Visits")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Today's Visits", "Plan Visit", "Visit History", "Visit Reports"])
    
    with tab1:
        st.subheader("📅 Today's Scheduled Visits")
        
        # Today's visits
        today_visits = {
            'Time': ['09:00', '10:30', '13:00', '15:00'],
            'Customer': ['PT. Teknologi Maju', 'CV. Bisnis Sukses', 'UD. Perdagangan Jaya', 'PT. Solusi Digital'],
            'Type': ['Sales Call', 'Follow Up', 'Delivery', 'Demo'],
            'Address': ['Jl. Sudirman No. 1', 'Jl. Thamrin No. 15', 'Jl. Gatot Subroto', 'Jl. Kuningan'],
            'Status': ['✅ Completed', '⏳ In Progress', '📋 Planned', '📋 Planned'],
            'Action': ['View', 'Check In', 'Start', 'Navigate']
        }
        
        df_today = pd.DataFrame(today_visits)
        
        # Display visits with action buttons
        for idx, row in df_today.iterrows():
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 2, 1])
                
                with col1:
                    st.write(f"**{row['Time']}** - {row['Customer']}")
                    st.write(f"📍 {row['Address']}")
                
                with col2:
                    st.write(f"**Type:** {row['Type']}")
                    st.write(f"**Status:** {row['Status']}")
                
                with col3:
                    if row['Status'] == '✅ Completed':
                        st.success("Done")
                    elif row['Status'] == '⏳ In Progress':
                        st.warning("Active")
                    else:
                        st.info("Pending")
                
                with col4:
                    if row['Action'] == 'Check In':
                        if st.button(f"📍 Check In", key=f"checkin_{idx}"):
                            st.success(f"Checked in at {row['Customer']}")
                    elif row['Action'] == 'Start':
                        if st.button(f"▶️ Start Visit", key=f"start_{idx}"):
                            st.info(f"Starting visit to {row['Customer']}")
                    elif row['Action'] == 'Navigate':
                        if st.button(f"🗺️ Navigate", key=f"nav_{idx}"):
                            st.info("Opening maps navigation...")
                    else:
                        if st.button(f"👁️ View", key=f"view_{idx}"):
                            show_visit_details(idx)
                
                with col5:
                    if st.button("📝", key=f"note_{idx}", help="Add note"):
                        st.text_input(f"Quick note for {row['Customer']}", key=f"quick_note_{idx}")
                
                st.markdown("---")
        
        # Quick add visit
        if st.button("➕ Add Quick Visit", use_container_width=True):
            show_quick_visit_form()
    
    with tab2:
        st.subheader("📝 Plan New Visit")
        
        with st.form("plan_visit"):
            col1, col2 = st.columns(2)
            
            with col1:
                customer = st.selectbox(
                    "Customer",
                    ["PT. Teknologi Maju", "CV. Bisnis Sukses", "UD. Perdagangan Jaya", "PT. Solusi Digital", "New Customer"]
                )
                visit_date = st.date_input("Visit Date", value=date.today())
                visit_time = st.time_input("Visit Time")
                
            with col2:
                visit_type = st.selectbox(
                    "Visit Type",
                    ["Sales Call", "Follow Up", "Delivery", "Demo", "Support", "Collection", "Survey"]
                )
                priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
                duration = st.number_input("Estimated Duration (minutes)", min_value=15, value=60, step=15)
            
            purpose = st.text_area("Visit Purpose", placeholder="Describe the main objective of this visit")
            
            # Customer contact info
            st.subheader("Contact Information")
            col1, col2 = st.columns(2)
            with col1:
                contact_person = st.text_input("Contact Person")
                phone = st.text_input("Phone Number")
            with col2:
                email = st.text_input("Email")
                address = st.text_area("Address")
            
            # Visit preparation
            st.subheader("Preparation")
            materials_needed = st.multiselect(
                "Materials Needed",
                ["Product Catalog", "Price List", "Samples", "Contracts", "Business Cards", "Laptop", "Projector"]
            )
            
            pre_visit_notes = st.text_area("Pre-visit Notes", placeholder="Any preparation notes or customer background info")
            
            if st.form_submit_button("Schedule Visit", use_container_width=True):
                st.success(f"✅ Visit scheduled with {customer} on {visit_date} at {visit_time}")
                st.balloons()
    
    with tab3:
        st.subheader("📊 Visit History")
        
        # Date range filter
        col1, col2, col3 = st.columns(3)
        with col1:
            start_date = st.date_input("From Date", value=date.today() - timedelta(days=30))
        with col2:
            end_date = st.date_input("To Date", value=date.today())
        with col3:
            status_filter = st.selectbox("Status", ["All", "Completed", "Cancelled", "Rescheduled"])
        
        # Visit history data
        history_data = {
            'Date': ['2024-01-19', '2024-01-18', '2024-01-17', '2024-01-16', '2024-01-15'],
            'Customer': ['PT. Teknologi Maju', 'CV. Bisnis Sukses', 'UD. Perdagangan Jaya', 'PT. Solusi Digital', 'CV. Maju Bersama'],
            'Type': ['Sales Call', 'Follow Up', 'Delivery', 'Demo', 'Sales Call'],
            'Duration': ['90 min', '45 min', '120 min', '75 min', '60 min'],
            'Result': ['Order placed', 'Follow up needed', 'Successful delivery', 'Demo completed', 'No interest'],
            'Value': [format_currency(15000000, 'IDR'), '-', format_currency(8500000, 'IDR'), '-', '-'],
            'Status': ['✅ Completed', '✅ Completed', '✅ Completed', '✅ Completed', '❌ No Sale']
        }
        
        df_history = pd.DataFrame(history_data)
        st.dataframe(df_history, use_container_width=True)
        
        # Visit statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Visits", "25", "5")
        with col2:
            st.metric("Success Rate", "80%", "5%")
        with col3:
            st.metric("Avg Duration", "75 min", "-5 min")
        with col4:
            st.metric("Total Value", format_currency(125000000, 'IDR'), "20%")
    
    with tab4:
        st.subheader("📈 Visit Analytics")
        
        # Visit performance metrics
        col1, col2 = st.columns(2)
        
        with col1:
            # Visit success rate by type
            visit_types = ['Sales Call', 'Follow Up', 'Delivery', 'Demo', 'Support']
            success_rates = [75, 85, 95, 70, 90]
            
            import plotly.express as px
            fig = px.bar(x=visit_types, y=success_rates, title="Success Rate by Visit Type (%)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Monthly visit trend
            months = ['Oct', 'Nov', 'Dec', 'Jan']
            visits = [18, 22, 25, 20]
            
            fig2 = px.line(x=months, y=visits, title="Monthly Visit Trend")
            st.plotly_chart(fig2, use_container_width=True)
        
        # Export options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Export Visit Report", use_container_width=True):
                csv = df_history.to_csv(index=False)
                st.download_button(
                    label="Download CSV Report",
                    data=csv,
                    file_name=f"visit_report_{date.today()}.csv",
                    mime="text/csv"
                )
        with col2:
            if st.button("📊 Generate Analysis", use_container_width=True):
                st.info("Detailed analytics report generation coming soon!")

def show_visit_details(visit_id):
    """Show detailed visit information"""
    st.subheader(f"Visit Details #{visit_id}")
    
    # Visit information
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Customer:** PT. Teknologi Maju")
        st.write("**Date:** 2024-01-20")
        st.write("**Time:** 09:00 - 10:30")
        st.write("**Type:** Sales Call")
        st.write("**Status:** Completed")
    
    with col2:
        st.write("**Contact:** Budi Manager")
        st.write("**Phone:** +62812-3456-7890")
        st.write("**Address:** Jl. Sudirman No. 1")
        st.write("**Duration:** 90 minutes")
        st.write("**Result:** Order placed")
    
    # Visit notes
    st.subheader("Visit Notes")
    st.text_area("Notes", value="Customer showed strong interest in our new product line. Discussed pricing and delivery terms. Order for 10 units confirmed.", disabled=True)
    
    # Follow up actions
    st.subheader("Follow Up Actions")
    st.write("- Send formal quotation")
    st.write("- Schedule delivery for next week")
    st.write("- Follow up on payment terms")

def show_quick_visit_form():
    """Show quick visit form"""
    with st.form("quick_visit"):
        st.subheader("Quick Visit Entry")
        
        col1, col2 = st.columns(2)
        with col1:
            customer = st.text_input("Customer Name")
            visit_type = st.selectbox("Type", ["Sales Call", "Follow Up", "Delivery", "Demo"])
        with col2:
            visit_time = st.time_input("Time", value=datetime.now().time())
            duration = st.number_input("Duration (min)", value=60)
        
        notes = st.text_area("Quick Notes")
        
        if st.form_submit_button("Add Visit"):
            st.success(f"Quick visit added for {customer}")
