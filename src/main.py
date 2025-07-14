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
from utils.translations import init_language, get_current_language, set_language, t
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

# Initialize database and language
init_database()
init_language()

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
    st.markdown(f'<div class="main-header"><h1>🏢 PenzFlow</h1><p>{t("app_title")}</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"### 🔐 {t('login_title')}")
        st.caption(t('login_subtitle'))
        username = st.text_input(t('username'), placeholder=f"{t('username').lower()}...")
        password = st.text_input(t('password'), type="password", placeholder=f"{t('password').lower()}...")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(t('login'), use_container_width=True):
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(t('login_success'))
                    st.rerun()
                else:
                    st.error(t('invalid_credentials'))
        
        with col_b:
            if st.button(f"Demo {t('login')}", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.username = "demo"
                st.success(t('login_success'))
                st.rerun()
        
        # Language info note
        st.markdown("---")
        st.caption(f"💡 {t('language')} dapat diubah di halaman {t('settings')} / Language can be changed in Settings page")

def show_main_app():
    # Clean header without language toggle
    st.markdown(f'<div class="main-header"><h1>📊 {t("app_title")}</h1></div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### {t('welcome')}, {st.session_state.get('username', 'User')}!")
        user_role = st.session_state.get('user_role', 'user')
        st.markdown(f"**{t('role')}:** {user_role.title()}")
        
        # Language indicator in sidebar
        current_lang = get_current_language()
        lang_display = "🇮🇩 ID" if current_lang == 'id' else "🇺🇸 EN"
        st.markdown(f"**{t('language')}:** {lang_display}")
        st.caption(f"💡 {t('settings')} → {t('language')}")
        
        st.markdown("---")
        
        # Different navigation based on user role
        if user_role in ['salesman', 'sales_manager']:
            page_options = [
                t("dashboard"), t("attendance"), t("visits"), t("mobile_orders"), 
                t("activities"), t("targets"), t("expenses"), t("dashboard") + " ERP", 
                t("customers"), t("products"), t("reports")
            ]
            page = st.selectbox(f"{t('dashboard')}:", page_options)
        else:
            page_options = [
                t("dashboard"), t("customers"), t("products"), t("sales"), 
                t("inventory"), t("reports"), t("sfa_management"), t("settings")
            ]
            page = st.selectbox(f"{t('dashboard')}:", page_options)
        
        st.markdown("---")
        if st.button(t('logout')):
            logout_user()
            st.success(t('logout_success'))
            st.rerun()
    
    # Main content based on selected page - map translated names back to English for routing
    page_mapping = {
        t("dashboard"): "Dashboard",
        t("attendance"): "Attendance", 
        t("visits"): "Customer Visits",
        t("mobile_orders"): "Mobile Orders",
        t("activities"): "Activities",
        t("targets"): "Targets", 
        t("expenses"): "Expenses",
        t("dashboard") + " ERP": "ERP Dashboard",
        t("customers"): "Customers",
        t("products"): "Products", 
        t("sales"): "Sales",
        t("inventory"): "Inventory",
        t("reports"): "Reports",
        t("sfa_management"): "SFA Management",
        t("settings"): "Settings"
    }
    
    actual_page = page_mapping.get(page, page)
    
    # Main content based on selected page
    if actual_page == "Dashboard":
        show_dashboard()
    elif actual_page == "SFA Dashboard":
        show_sfa_dashboard()
    elif actual_page == "ERP Dashboard":
        show_dashboard()
    elif actual_page == "Attendance":
        show_attendance()
    elif actual_page == "Customer Visits":
        show_customer_visits()
    elif actual_page == "Mobile Orders":
        show_mobile_orders()
    elif actual_page == "Activities":
        show_sales_activities()
    elif actual_page == "Targets":
        show_sales_targets()
    elif actual_page == "Expenses":
        show_expenses()
    elif actual_page == "Customers":
        show_customers()
    elif actual_page == "Products":
        show_products()
    elif actual_page == "Sales":
        show_sales()
    elif actual_page == "Inventory":
        show_inventory()
    elif actual_page == "Reports":
        show_reports()
    elif actual_page == "SFA Management":
        show_sfa_management()
    elif actual_page == "Settings":
        show_settings()

if __name__ == "__main__":
    main()
