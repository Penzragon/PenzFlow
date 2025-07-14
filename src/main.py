import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pytz
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Database and utilities
from database.init_db import init_database
from utils.auth import check_login, login_user, logout_user
from utils.helpers import format_currency
from config import Config

# ERP Pages
from erp_pages.dashboard import show_dashboard
from erp_pages.customers import show_customers
from erp_pages.products import show_products
from erp_pages.sales import show_sales
from erp_pages.inventory import show_inventory
from erp_pages.reports import show_reports
from erp_pages.settings import show_settings
from erp_pages.sfa_management import show_sfa_management

# SFA Pages  
from sfa_pages.dashboard import show_sfa_dashboard, show_attendance
from sfa_pages.visits import show_customer_visits
from sfa_pages.mobile_orders import show_mobile_orders
from sfa_pages.activities import show_sales_activities
from sfa_pages.targets import show_sales_targets
from sfa_pages.expenses import show_expenses

# Set Indonesian timezone
INDONESIA_TZ = pytz.timezone('Asia/Jakarta')

# Configure page
st.set_page_config(
    page_title="PenzFlow - ERP & SFA System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_database()

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Check if user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        show_login_page()
    else:
        show_main_app()

def show_login_page():
    st.markdown('<div class="main-header"><h1>🏢 PenzFlow</h1><p>Enterprise Resource Planning & Sales Force Automation</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Login", use_container_width=True):
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        with col_b:
            if st.button("Demo Login", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.username = "demo"
                st.rerun()

def show_main_app():
    # Header
    st.markdown('<div class="main-header"><h1>📊 PenzFlow Dashboard</h1></div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.get('username', 'User')}!")
        user_role = st.session_state.get('user_role', 'user')
        st.markdown(f"**Role:** {user_role.title()}")
        st.markdown("---")
        
        # Different navigation based on user role
        if user_role in ['salesman', 'sales_manager']:
            page = st.selectbox(
                "Navigate to:",
                ["SFA Dashboard", "Attendance", "Customer Visits", "Mobile Orders", "Activities", "Targets", "Expenses", "ERP Dashboard", "Customers", "Products", "Reports"]
            )
        else:
            page = st.selectbox(
                "Navigate to:",
                ["Dashboard", "Customers", "Products", "Sales", "Inventory", "Reports", "SFA Management", "Settings"]
            )
        
        st.markdown("---")
        if st.button("Logout"):
            logout_user()
            st.rerun()
    
    # Main content based on selected page
    if page == "Dashboard":
        show_dashboard()
    elif page == "SFA Dashboard":
        show_sfa_dashboard()
    elif page == "ERP Dashboard":
        show_dashboard()
    elif page == "Attendance":
        show_attendance()
    elif page == "Customer Visits":
        show_customer_visits()
    elif page == "Mobile Orders":
        show_mobile_orders()
    elif page == "Activities":
        show_sales_activities()
    elif page == "Targets":
        show_sales_targets()
    elif page == "Expenses":
        show_expenses()
    elif page == "Customers":
        show_customers()
    elif page == "Products":
        show_products()
    elif page == "Sales":
        show_sales()
    elif page == "Inventory":
        show_inventory()
    elif page == "Reports":
        show_reports()
    elif page == "SFA Management":
        show_sfa_management()
    elif page == "Settings":
        show_settings()

if __name__ == "__main__":
    main()
