import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import format_currency

def show_sfa_management():
    """SFA Management for Administrators and Managers"""
    st.header("📊 SFA Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Team Overview", "Sales Performance", "Attendance Reports", "Activity Tracking"])
    
    with tab1:
        st.subheader("Sales Team Overview")
        
        team_performance = {
            'Salesman': ['Budi Santoso', 'Sari Wulandari', 'Ahmad Rahman'],
            'Monthly Target': [format_currency(50000000, 'IDR'), format_currency(45000000, 'IDR'), format_currency(40000000, 'IDR')],
            'Achievement': [format_currency(35000000, 'IDR'), format_currency(42000000, 'IDR'), format_currency(30000000, 'IDR')],
            'Achievement %': ['70%', '93%', '75%'],
            'Visits This Month': ['15/20', '18/18', '12/16'],
            'Active Customers': ['12', '15', '10'],
            'Status': ['🟡 On Track', '✅ Excellent', '🟡 Needs Support']
        }
        
        df_team = pd.DataFrame(team_performance)
        st.dataframe(df_team, use_container_width=True)
        
        # Team actions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊 Generate Team Report"):
                st.info("Team report generation feature coming soon!")
        with col2:
            if st.button("🎯 Set Team Targets"):
                st.info("Target setting feature coming soon!")
        with col3:
            if st.button("📧 Send Team Update"):
                st.info("Team communication feature coming soon!")
    
    with tab2:
        st.subheader("Sales Performance Analytics")
        
        # Team performance chart
        salesmen = ['Budi Santoso', 'Sari Wulandari', 'Ahmad Rahman']
        targets = [50000000, 45000000, 40000000]
        achievements = [35000000, 42000000, 30000000]
        
        fig = go.Figure(data=[
            go.Bar(name='Target', x=salesmen, y=targets, marker_color='lightblue'),
            go.Bar(name='Achievement', x=salesmen, y=achievements, marker_color='darkblue')
        ])
        
        fig.update_layout(
            title="Sales Target vs Achievement",
            xaxis_title="Sales Team",
            yaxis_title="Sales (IDR)",
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Team Target", format_currency(135000000, 'IDR'))
        with col2:
            st.metric("Team Achievement", format_currency(107000000, 'IDR'))
        with col3:
            st.metric("Team Performance", "79%", "5% above average")
    
    with tab3:
        st.subheader("Attendance Reports")
        
        attendance_summary = {
            'Salesman': ['Budi Santoso', 'Sari Wulandari', 'Ahmad Rahman'],
            'Days Present': ['20/22', '21/22', '18/22'],
            'Attendance %': ['91%', '95%', '82%'],
            'Avg Check-in': ['08:30', '08:25', '08:45'],
            'Avg Hours/Day': ['8.5', '8.7', '8.2'],
            'Field Time %': ['75%', '80%', '70%']
        }
        
        df_attendance = pd.DataFrame(attendance_summary)
        st.dataframe(df_attendance, use_container_width=True)
        
        # Attendance chart
        attendance_data = [91, 95, 82]
        colors = ['orange' if x < 90 else 'green' for x in attendance_data]
        
        fig = px.bar(x=salesmen, y=attendance_data, title="Team Attendance Percentage", 
                     color=attendance_data, color_continuous_scale='RdYlGn')
        fig.update_layout(xaxis_title="Sales Team", yaxis_title="Attendance %")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Activity Tracking")
        
        activity_summary = {
            'Salesman': ['Budi Santoso', 'Sari Wulandari', 'Ahmad Rahman'],
            'Calls Made': ['45', '52', '38'],
            'Emails Sent': ['23', '31', '19'],
            'Meetings': ['12', '15', '10'],
            'Orders Created': ['8', '11', '6'],
            'Conversion Rate': ['18%', '21%', '16%']
        }
        
        df_activities = pd.DataFrame(activity_summary)
        st.dataframe(df_activities, use_container_width=True)
        
        # Activity performance chart
        activities = ['Calls', 'Emails', 'Meetings', 'Orders']
        budi_data = [45, 23, 12, 8]
        sari_data = [52, 31, 15, 11]
        ahmad_data = [38, 19, 10, 6]
        
        fig = go.Figure(data=[
            go.Bar(name='Budi Santoso', x=activities, y=budi_data),
            go.Bar(name='Sari Wulandari', x=activities, y=sari_data),
            go.Bar(name='Ahmad Rahman', x=activities, y=ahmad_data)
        ])
        
        fig.update_layout(
            title="Team Activity Comparison",
            xaxis_title="Activity Type",
            yaxis_title="Count",
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True)
