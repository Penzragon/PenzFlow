import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timedelta
from utils.helpers import format_currency
from database.init_db import get_connection

def show_sfa_dashboard():
    """SFA Dashboard for Sales Team"""
    st.header("📱 SFA Dashboard")
    
    user_role = st.session_state.get('user_role', 'user')
    username = st.session_state.get('username', 'User')
    
    # Quick stats for salesman
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Today's Visits",
            value="3",
            delta="1"
        )
    
    with col2:
        st.metric(
            label="This Month Sales",
            value=format_currency(35000000, 'IDR'),
            delta="15.2%"
        )
    
    with col3:
        st.metric(
            label="Target Achievement",
            value="70%",
            delta="5%"
        )
    
    with col4:
        st.metric(
            label="Active Customers",
            value="8",
            delta="2"
        )
    
    st.markdown("---")
    
    # Today's Schedule
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📅 Today's Schedule")
        
        # Sample schedule data
        schedule_data = {
            'Time': ['09:00', '10:30', '13:00', '15:00'],
            'Customer': ['PT. Teknologi Maju', 'CV. Bisnis Sukses', 'UD. Perdagangan Jaya', 'PT. Solusi Digital'],
            'Type': ['Sales Call', 'Follow Up', 'Delivery', 'Demo'],
            'Status': ['✅ Completed', '⏳ In Progress', '📋 Planned', '📋 Planned']
        }
        
        df_schedule = pd.DataFrame(schedule_data)
        st.dataframe(df_schedule, use_container_width=True)
        
        # Quick actions
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("🎯 Check In", use_container_width=True):
                st.success("✅ Checked in successfully!")
        with col_b:
            if st.button("📍 Add Visit", use_container_width=True):
                st.info("Redirecting to visit creation...")
        with col_c:
            if st.button("📱 Quick Order", use_container_width=True):
                st.info("Redirecting to mobile order...")
    
    with col2:
        st.subheader("🎯 Monthly Targets")
        
        # Target progress
        target_data = {
            'Metric': ['Sales Amount', 'Number of Visits', 'New Customers'],
            'Target': [50000000, 20, 10],
            'Achieved': [35000000, 15, 8],
            'Progress': [70, 75, 80]
        }
        
        for i, row in enumerate(target_data['Metric']):
            progress = target_data['Progress'][i]
            if row == 'Sales Amount':
                st.metric(
                    label=row,
                    value=f"{format_currency(target_data['Achieved'][i], 'IDR')} / {format_currency(target_data['Target'][i], 'IDR')}",
                    delta=f"{progress}%"
                )
            else:
                st.metric(
                    label=row,
                    value=f"{target_data['Achieved'][i]} / {target_data['Target'][i]}",
                    delta=f"{progress}%"
                )
            st.progress(progress / 100)
    
    # Recent Activities
    st.subheader("📊 Recent Activities")
    
    activities_data = {
        'Time': ['1 hour ago', '3 hours ago', 'Yesterday', '2 days ago'],
        'Activity': ['Visit completed', 'Order created', 'Customer call', 'Product demo'],
        'Customer': ['PT. Teknologi Maju', 'CV. Bisnis Sukses', 'UD. Perdagangan Jaya', 'PT. Solusi Digital'],
        'Result': ['Interested in bulk order', format_currency(5500000, 'IDR') + ' order', 'Scheduled follow-up', 'Demo successful']
    }
    
    df_activities = pd.DataFrame(activities_data)
    st.dataframe(df_activities, use_container_width=True)
    
    # Performance Chart
    st.subheader("📈 Performance Trend")
    
    # Sample performance data
    dates = pd.date_range(start=date.today() - timedelta(days=30), end=date.today(), freq='D')
    sales = [500000 + i*50000 + (i%7)*200000 for i in range(len(dates))]
    visits = [1 + (i%5) for i in range(len(dates))]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_sales = px.line(x=dates, y=sales, title="Daily Sales Trend (Last 30 Days)")
        fig_sales.update_layout(xaxis_title="Date", yaxis_title="Sales (IDR)")
        st.plotly_chart(fig_sales, use_container_width=True)
    
    with col2:
        fig_visits = px.bar(x=dates[-7:], y=visits[-7:], title="Daily Visits (Last 7 Days)")
        fig_visits.update_layout(xaxis_title="Date", yaxis_title="Number of Visits")
        st.plotly_chart(fig_visits, use_container_width=True)

def show_attendance():
    """Attendance Management"""
    st.header("⏰ Attendance Management")
    
    tab1, tab2, tab3 = st.tabs(["Check In/Out", "My Attendance", "Team Attendance"])
    
    with tab1:
        st.subheader("📍 Current Status")
        
        # Mock current status
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("**Status:** Not Checked In")
            st.write("**Last Check In:** Yesterday 08:30")
        
        with col2:
            st.write("**Current Time:**")
            st.write(datetime.now().strftime("%H:%M:%S"))
            st.write("**Date:**")
            st.write(datetime.now().strftime("%Y-%m-%d"))
        
        with col3:
            st.write("**Location:**")
            st.write("Jakarta Office")
            st.write("**GPS:** -6.2088, 106.8456")
        
        # Check in/out buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🟢 Check In", use_container_width=True):
                st.success("✅ Checked in successfully at " + datetime.now().strftime("%H:%M:%S"))
                st.balloons()
        
        with col2:
            if st.button("🔴 Check Out", use_container_width=True):
                st.success("✅ Checked out successfully at " + datetime.now().strftime("%H:%M:%S"))
        
        # Manual entry form
        st.markdown("---")
        st.subheader("✏️ Manual Entry")
        
        with st.form("manual_attendance"):
            col1, col2 = st.columns(2)
            with col1:
                entry_date = st.date_input("Date", value=date.today())
                check_in_time = st.time_input("Check In Time")
            
            with col2:
                check_out_time = st.time_input("Check Out Time")
                reason = st.selectbox("Reason", ["Forgot to check in", "System error", "Field work", "Other"])
            
            notes = st.text_area("Notes", placeholder="Additional explanation")
            
            if st.form_submit_button("Submit Manual Entry"):
                st.success("✅ Manual attendance entry submitted for approval!")
    
    with tab2:
        st.subheader("📊 My Attendance History")
        
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From", value=date.today() - timedelta(days=30))
        with col2:
            end_date = st.date_input("To", value=date.today())
        
        # Sample attendance data
        attendance_data = {
            'Date': ['2024-01-20', '2024-01-19', '2024-01-18', '2024-01-17', '2024-01-16'],
            'Check In': ['08:30', '08:25', '08:45', '08:30', '08:20'],
            'Check Out': ['17:00', '17:15', '16:45', '17:30', '17:00'],
            'Hours': ['8:30', '8:50', '8:00', '9:00', '8:40'],
            'Status': ['✅ Present', '✅ Present', '⚠️ Late', '✅ Present', '✅ Present'],
            'Location': ['Office', 'Office', 'Field', 'Office', 'Office']
        }
        
        df_attendance = pd.DataFrame(attendance_data)
        st.dataframe(df_attendance, use_container_width=True)
        
        # Attendance summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Days", "20")
        with col2:
            st.metric("Present", "19", "95%")
        with col3:
            st.metric("Late", "1", "5%")
        with col4:
            st.metric("Average Hours", "8.6")
    
    with tab3:
        # Only show for managers
        user_role = st.session_state.get('user_role', 'user')
        if user_role in ['sales_manager', 'administrator']:
            st.subheader("👥 Team Attendance Overview")
            
            # Team attendance data
            team_data = {
                'Employee': ['Budi Santoso', 'Sari Wulandari', 'Ahmad Rahman'],
                'Status': ['✅ Present', '✅ Present', '❌ Absent'],
                'Check In': ['08:30', '08:25', '-'],
                'Location': ['Jakarta Office', 'Field Visit', '-'],
                'Today Hours': ['7:30', '6:45', '0:00']
            }
            
            df_team = pd.DataFrame(team_data)
            st.dataframe(df_team, use_container_width=True)
            
            # Team stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Present Today", "2/3", "67%")
            with col2:
                st.metric("Avg Arrival", "08:27")
            with col3:
                st.metric("Team Performance", "92%", "3%")
        else:
            st.info("Team attendance view is only available for managers.")
