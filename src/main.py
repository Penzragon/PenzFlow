import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pytz
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.init_db import init_database
from utils.auth import check_login, login_user, logout_user
from utils.helpers import format_currency
from config import Config

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
        st.markdown("---")
        
        page = st.selectbox(
            "Navigate to:",
            ["Dashboard", "Customers", "Products", "Sales", "Inventory", "Reports", "Settings"]
        )
        
        st.markdown("---")
        if st.button("Logout"):
            logout_user()
            st.rerun()
    
    # Main content based on selected page
    if page == "Dashboard":
        show_dashboard()
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
    elif page == "Settings":
        show_settings()

def show_dashboard():
    st.header("📈 Dashboard Overview")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Sales",
            value=format_currency(1875450000, 'IDR'),  # ~$125,430 converted to IDR
            delta="12.5%"
        )
    
    with col2:
        st.metric(
            label="Active Customers",
            value="1,234",
            delta="8.2%"
        )
    
    with col3:
        st.metric(
            label="Products in Stock",
            value="456",
            delta="-2.1%"
        )
    
    with col4:
        st.metric(
            label="Pending Orders",
            value="23",
            delta="5.0%"
        )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sales Trend")
        # Sample data for sales trend
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        sales = [12000, 15000, 13500, 18000, 16500, 19000, 21000, 18500, 17000, 22000, 20500, 25000]
        
        fig = px.line(x=dates, y=sales, title="Monthly Sales Trend")
        fig.update_layout(xaxis_title="Month", yaxis_title="Sales ($)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top Products")
        products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
        sales_data = [45, 30, 15, 7, 3]
        
        fig = px.pie(values=sales_data, names=products, title="Top Selling Products")
        st.plotly_chart(fig, use_container_width=True)

def show_customers():
    st.header("👥 Customer Management")
    
    tab1, tab2 = st.tabs(["Customer List", "Add New Customer"])
    
    with tab1:
        # Sample customer data
        customers_data = {
            'ID': [1, 2, 3, 4, 5],
            'Name': ['Budi Santoso', 'Sari Dewi', 'Ahmad Rahman', 'Indira Putri', 'Rizki Pratama'],
            'Email': ['budi.santoso@email.com', 'sari.dewi@email.com', 'ahmad.rahman@email.com', 'indira.putri@email.com', 'rizki.pratama@email.com'],
            'Phone': ['+62812-3456-7890', '+62813-4567-8901', '+62814-5678-9012', '+62815-6789-0123', '+62816-7890-1234'],  # Indonesian phone format
            'Total Orders': [15, 8, 23, 12, 6],
            'Total Spent': [format_currency(81000000, 'IDR'), format_currency(42000000, 'IDR'), format_currency(133500000, 'IDR'), format_currency(63000000, 'IDR'), format_currency(27000000, 'IDR')]
        }
        
        df = pd.DataFrame(customers_data)
        st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.subheader("Add New Customer")
        with st.form("add_customer"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Customer Name")
                email = st.text_input("Email")
            with col2:
                phone = st.text_input("Phone")
                company = st.text_input("Company")
            
            address = st.text_area("Address")
            
            if st.form_submit_button("Add Customer"):
                st.success("Customer added successfully!")

def show_products():
    st.header("📦 Product Management")
    
    tab1, tab2 = st.tabs(["Product List", "Add New Product"])
    
    with tab1:
        # Sample product data
        products_data = {
            'SKU': ['PRD001', 'PRD002', 'PRD003', 'PRD004', 'PRD005'],
            'Name': ['Laptop Pro', 'Wireless Mouse', 'USB Cable', 'Monitor Stand', 'Keyboard'],
            'Category': ['Electronics', 'Accessories', 'Cables', 'Furniture', 'Input Devices'],
            'Price': [format_currency(14999000, 'IDR'), format_currency(449000, 'IDR'), format_currency(149000, 'IDR'), format_currency(749000, 'IDR'), format_currency(1199000, 'IDR')],
            'Stock': [25, 150, 200, 45, 80],
            'Status': ['In Stock', 'In Stock', 'In Stock', 'Low Stock', 'In Stock']
        }
        
        df = pd.DataFrame(products_data)
        st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.subheader("Add New Product")
        with st.form("add_product"):
            col1, col2 = st.columns(2)
            with col1:
                sku = st.text_input("SKU")
                name = st.text_input("Product Name")
                category = st.selectbox("Category", ["Electronics", "Accessories", "Cables", "Furniture", "Input Devices"])
            with col2:
                price = st.number_input("Price", min_value=0.01, format="%.2f")
                stock = st.number_input("Initial Stock", min_value=0, step=1)
                supplier = st.text_input("Supplier")
            
            description = st.text_area("Description")
            
            if st.form_submit_button("Add Product"):
                st.success("Product added successfully!")

def show_sales():
    st.header("💰 Sales Management")
    
    tab1, tab2 = st.tabs(["Sales Orders", "Create New Order"])
    
    with tab1:
        # Sample sales data
        sales_data = {
            'Order ID': ['ORD001', 'ORD002', 'ORD003', 'ORD004', 'ORD005'],
            'Customer': ['Budi Santoso', 'Sari Dewi', 'Ahmad Rahman', 'Indira Putri', 'Rizki Pratama'],
            'Date': ['15-01-2024', '16-01-2024', '17-01-2024', '18-01-2024', '19-01-2024'],  # Indonesian date format DD-MM-YYYY
            'Amount': [format_currency(19500000, 'IDR'), format_currency(1350000, 'IDR'), format_currency(37500000, 'IDR'), format_currency(9000000, 'IDR'), format_currency(3000000, 'IDR')],
            'Status': ['Completed', 'Pending', 'Shipped', 'Processing', 'Completed']
        }
        
        df = pd.DataFrame(sales_data)
        st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.subheader("Create New Sales Order")
        with st.form("create_order"):
            col1, col2 = st.columns(2)
            with col1:
                customer = st.selectbox("Customer", ["Budi Santoso", "Sari Dewi", "Ahmad Rahman", "Indira Putri", "Rizki Pratama"])
                order_date = st.date_input("Order Date")
            with col2:
                payment_method = st.selectbox("Payment Method", ["Credit Card", "Cash", "Bank Transfer", "Transfer Bank", "QRIS"])  # Added Indonesian payment methods
                sales_rep = st.text_input("Sales Representative")
            
            st.subheader("Order Items")
            product = st.selectbox("Product", ["Laptop Pro", "Wireless Mouse", "USB Cable", "Monitor Stand"])
            quantity = st.number_input("Quantity", min_value=1, step=1)
            
            if st.form_submit_button("Create Order"):
                st.success("Sales order created successfully!")

def show_inventory():
    st.header("📊 Inventory Management")
    
    # Inventory summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Products", "125")
    with col2:
        st.metric("Low Stock Items", "8")
    with col3:
        st.metric("Out of Stock", "3")
    
    st.markdown("---")
    
    # Inventory table
    inventory_data = {
        'Product': ['Laptop Pro', 'Wireless Mouse', 'USB Cable', 'Monitor Stand', 'Keyboard'],
        'Current Stock': [25, 150, 200, 5, 80],
        'Min Stock Level': [10, 50, 100, 20, 30],
        'Max Stock Level': [100, 300, 500, 100, 150],
        'Reorder Point': [15, 75, 150, 30, 45],
        'Status': ['✅ Good', '✅ Good', '✅ Good', '⚠️ Low', '✅ Good']
    }
    
    df = pd.DataFrame(inventory_data)
    st.dataframe(df, use_container_width=True)
    
    # Stock level chart
    st.subheader("Stock Levels")
    fig = px.bar(df, x='Product', y='Current Stock', color='Status', 
                 title="Current Stock Levels by Product")
    st.plotly_chart(fig, use_container_width=True)

def show_reports():
    st.header("📋 Reports & Analytics")
    
    tab1, tab2, tab3 = st.tabs(["Sales Reports", "Inventory Reports", "Customer Reports"])
    
    with tab1:
        st.subheader("Sales Performance")
        
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")
        
        # Sales metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Revenue", format_currency(678450000, 'IDR'), "15.2%")  # ~$45,230 -> Rp 678,450,000
        with col2:
            st.metric("Orders Completed", "156", "8.7%")
        with col3:
            st.metric("Average Order Value", format_currency(4350000, 'IDR'), "12.1%")  # ~$290 -> Rp 4,350,000
        
        # Sales chart
        dates = pd.date_range(start=start_date, end=end_date, freq='D')[:30]
        sales = [1200 + i*50 + (i%7)*200 for i in range(len(dates))]
        
        fig = px.line(x=dates, y=sales, title="Daily Sales Trend")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Inventory Analysis")
        
        # Inventory turnover
        products = ['Product A', 'Product B', 'Product C', 'Product D']
        turnover = [12, 8, 15, 6]
        
        fig = px.bar(x=products, y=turnover, title="Inventory Turnover Rate")
        fig.update_layout(xaxis_title="Products", yaxis_title="Turnover Rate")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Customer Analytics")
        
        # Customer segments
        segments = ['New', 'Regular', 'VIP', 'Inactive']
        counts = [45, 120, 25, 15]
        
        fig = px.pie(values=counts, names=segments, title="Customer Segments")
        st.plotly_chart(fig, use_container_width=True)

def show_settings():
    st.header("⚙️ Settings")
    
    tab1, tab2, tab3 = st.tabs(["General", "Users", "System"])
    
    with tab1:
        st.subheader("General Settings")
        company_name = st.text_input("Company Name", value="PenzFlow Corp")
        currency = st.selectbox("Currency", ["IDR", "USD", "EUR", "GBP", "JPY"], index=0)
        timezone = st.selectbox("Timezone", ["Asia/Jakarta (GMT+7)", "UTC", "EST", "PST", "GMT"], index=0)
        
        if st.button("Save General Settings"):
            st.success("Settings saved successfully!")
    
    with tab2:
        st.subheader("User Management")
        
        # User list
        users_data = {
            'Username': ['admin', 'sales1', 'manager', 'demo'],
            'Role': ['Administrator', 'Sales Rep', 'Manager', 'Demo User'],
            'Status': ['Active', 'Active', 'Active', 'Active'],
            'Last Login': ['20-01-2024', '19-01-2024', '20-01-2024', '20-01-2024']  # Indonesian date format
        }
        
        df = pd.DataFrame(users_data)
        st.dataframe(df, use_container_width=True)
        
        st.subheader("Add New User")
        with st.form("add_user"):
            col1, col2 = st.columns(2)
            with col1:
                new_username = st.text_input("Username")
                new_role = st.selectbox("Role", ["Administrator", "Manager", "Sales Rep", "Viewer"])
            with col2:
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Add User"):
                st.success("User added successfully!")
    
    with tab3:
        st.subheader("System Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Version:** 1.0.0")
            st.info("**Database:** SQLite")
            st.info("**Framework:** Streamlit")
        
        with col2:
            st.info("**Last Backup:** 20-01-2024 14:30 WIB")  # Indonesian datetime format
            st.info("**System Status:** Healthy")
            st.info("**Uptime:** 15 days")
        
        if st.button("Create Backup"):
            st.success("Backup created successfully!")

if __name__ == "__main__":
    main()
