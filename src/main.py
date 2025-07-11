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

def show_sfa_dashboard():
    st.header("📱 SFA Dashboard")
    
    user_id = st.session_state.get('user_id', 1)
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Today's Visits",
            value="3",
            delta="1"
        )
    
    with col2:
        st.metric(
            label="Orders Today",
            value=format_currency(15000000, 'IDR'),
            delta="25%"
        )
    
    with col3:
        st.metric(
            label="Monthly Target",
            value="70%",
            delta="10%"
        )
    
    with col4:
        st.metric(
            label="Active Customers",
            value="12",
            delta="2"
        )
    
    st.markdown("---")
    
    # Quick Actions
    st.subheader("Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📍 Check In", use_container_width=True):
            st.success("Checked in successfully!")
    
    with col2:
        if st.button("🏢 Visit Customer", use_container_width=True):
            st.info("Redirecting to Customer Visits...")
    
    with col3:
        if st.button("📝 New Order", use_container_width=True):
            st.info("Redirecting to Mobile Orders...")
    
    with col4:
        if st.button("💰 Add Expense", use_container_width=True):
            st.info("Redirecting to Expenses...")
    
    # Today's Schedule
    st.subheader("Today's Schedule")
    schedule_data = {
        'Time': ['09:00', '11:00', '14:00', '16:00'],
        'Activity': ['Visit PT. Teknologi Maju', 'Follow up CV. Bisnis Sukses', 'Product Demo at UD. Perdagangan', 'Team Meeting'],
        'Status': ['✅ Completed', '🟡 In Progress', '📅 Scheduled', '📅 Scheduled']
    }
    
    df_schedule = pd.DataFrame(schedule_data)
    st.dataframe(df_schedule, use_container_width=True)

def show_attendance():
    st.header("📅 Attendance Management")
    
    tab1, tab2, tab3 = st.tabs(["Check In/Out", "Attendance History", "Team Attendance"])
    
    with tab1:
        st.subheader("Daily Attendance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Check In")
            location = st.text_input("Location", value="Jakarta Office")
            
            if st.button("📍 Check In", type="primary"):
                jakarta_time = datetime.now(INDONESIA_TZ)
                st.success(f"Checked in at {jakarta_time.strftime('%H:%M:%S WIB')}")
                st.balloons()
        
        with col2:
            st.markdown("### Check Out")
            notes = st.text_area("Notes for today")
            
            if st.button("🚪 Check Out", type="secondary"):
                jakarta_time = datetime.now(INDONESIA_TZ)
                st.success(f"Checked out at {jakarta_time.strftime('%H:%M:%S WIB')}")
        
        # Current Status
        st.markdown("---")
        st.subheader("Current Status")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Status", "Checked In", "08:30 WIB")
        with col2:
            st.metric("Hours Today", "7.5", "+0.5")
        with col3:
            st.metric("Location", "Jakarta Office", "Active")
    
    with tab2:
        st.subheader("Attendance History")
        
        # Date range filter
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime.now().date() - timedelta(days=7))
        with col2:
            end_date = st.date_input("End Date", value=datetime.now().date())
        
        # Sample attendance data
        attendance_data = {
            'Date': ['11-07-2024', '10-07-2024', '09-07-2024', '08-07-2024', '05-07-2024'],
            'Check In': ['08:30 WIB', '08:45 WIB', '08:25 WIB', '08:35 WIB', '08:30 WIB'],
            'Check Out': ['17:00 WIB', '17:15 WIB', '17:30 WIB', '17:00 WIB', '17:05 WIB'],
            'Hours': ['8.5', '8.5', '9.0', '8.4', '8.6'],
            'Status': ['✅ Present', '✅ Present', '✅ Present', '✅ Present', '✅ Present']
        }
        
        df_attendance = pd.DataFrame(attendance_data)
        st.dataframe(df_attendance, use_container_width=True)
    
    with tab3:
        st.subheader("Team Attendance Overview")
        
        team_data = {
            'Salesman': ['Budi Santoso', 'Sari Wulandari', 'Ahmad Rahman'],
            'Status': ['✅ Present', '✅ Present', '❌ Absent'],
            'Check In': ['08:30 WIB', '08:45 WIB', '-'],
            'Last Location': ['Jakarta Office', 'Bandung Office', '-'],
            'Today Hours': ['7.5', '7.0', '0']
        }
        
        df_team = pd.DataFrame(team_data)
        st.dataframe(df_team, use_container_width=True)

def show_customer_visits():
    st.header("🏢 Customer Visits")
    
    tab1, tab2, tab3 = st.tabs(["New Visit", "Today's Visits", "Visit History"])
    
    with tab1:
        st.subheader("Plan New Customer Visit")
        
        with st.form("new_visit"):
            col1, col2 = st.columns(2)
            
            with col1:
                customer = st.selectbox("Customer", ["PT. Teknologi Maju", "CV. Bisnis Sukses", "UD. Perdagangan Jaya", "Toko Elektronik Sejahtera"])
                visit_type = st.selectbox("Visit Type", ["Sales Call", "Delivery", "Follow Up", "Complaint Handling", "Product Demo"])
                visit_date = st.datetime_input("Visit Date & Time", value=datetime.now())
            
            with col2:
                purpose = st.text_area("Purpose of Visit")
                location = st.text_input("Location", placeholder="Customer's address")
                estimated_duration = st.number_input("Estimated Duration (minutes)", min_value=15, max_value=480, value=60)
            
            special_notes = st.text_area("Special Notes")
            
            if st.form_submit_button("📅 Schedule Visit", type="primary"):
                st.success("Visit scheduled successfully!")
                st.info(f"Visit to {customer} scheduled for {visit_date.strftime('%d %B %Y at %H:%M WIB')}")
    
    with tab2:
        st.subheader("Today's Scheduled Visits")
        
        visits_today = {
            'Time': ['09:00 WIB', '11:30 WIB', '14:00 WIB'],
            'Customer': ['PT. Teknologi Maju', 'CV. Bisnis Sukses', 'UD. Perdagangan Jaya'],
            'Type': ['Sales Call', 'Follow Up', 'Product Demo'],
            'Status': ['✅ Completed', '🟡 In Progress', '📅 Scheduled'],
            'Action': ['View Report', 'Continue', 'Start Visit']
        }
        
        df_visits_today = pd.DataFrame(visits_today)
        st.dataframe(df_visits_today, use_container_width=True)
        
        # Quick Start Visit
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🚀 Start Next Visit", type="primary"):
                st.success("Visit started! Timer running...")
        
        with col2:
            if st.button("📍 Get Directions"):
                st.info("Opening GPS navigation...")
        
        with col3:
            if st.button("📞 Call Customer"):
                st.info("Initiating call...")
    
    with tab3:
        st.subheader("Visit History & Reports")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_customer = st.selectbox("Filter by Customer", ["All", "PT. Teknologi Maju", "CV. Bisnis Sukses", "UD. Perdagangan Jaya"])
        with col2:
            filter_type = st.selectbox("Filter by Type", ["All", "Sales Call", "Delivery", "Follow Up", "Product Demo"])
        with col3:
            filter_status = st.selectbox("Filter by Status", ["All", "Completed", "Cancelled", "Rescheduled"])
        
        # Visit history data
        visit_history = {
            'Date': ['10-07-2024', '09-07-2024', '08-07-2024', '05-07-2024'],
            'Customer': ['PT. Teknologi Maju', 'CV. Bisnis Sukses', 'UD. Perdagangan Jaya', 'Toko Elektronik Sejahtera'],
            'Type': ['Sales Call', 'Follow Up', 'Delivery', 'Product Demo'],
            'Duration': ['120 min', '90 min', '150 min', '180 min'],
            'Result': ['Order Placed', 'Payment Received', 'Delivered', 'Demo Completed'],
            'Follow Up': ['2 weeks', 'None', '1 month', '1 week']
        }
        
        df_history = pd.DataFrame(visit_history)
        st.dataframe(df_history, use_container_width=True)

def show_mobile_orders():
    st.header("📱 Mobile Orders")
    
    tab1, tab2, tab3 = st.tabs(["Create Order", "Draft Orders", "Order History"])
    
    with tab1:
        st.subheader("Create New Order")
        
        with st.form("mobile_order"):
            # Customer and basic info
            col1, col2 = st.columns(2)
            
            with col1:
                customer = st.selectbox("Customer", ["PT. Teknologi Maju", "CV. Bisnis Sukses", "UD. Perdagangan Jaya"])
                visit_reference = st.selectbox("Related Visit", ["Current Visit", "Previous Visit - 10/07", "Standalone Order"])
                payment_terms = st.selectbox("Payment Terms", ["Cash", "Credit 30 days", "Credit 60 days", "Credit 90 days"])
            
            with col2:
                delivery_date = st.date_input("Delivery Date", value=datetime.now().date() + timedelta(days=3))
                special_discount = st.number_input("Special Discount (%)", min_value=0.0, max_value=50.0, value=0.0)
                special_instructions = st.text_area("Special Instructions")
            
            # Product selection
            st.subheader("Order Items")
            
            # Dynamic product addition
            if 'order_items' not in st.session_state:
                st.session_state.order_items = []
            
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            with col1:
                product = st.selectbox("Product", ["Laptop Pro", "Wireless Mouse", "USB Cable", "Monitor Stand", "Keyboard"])
            with col2:
                quantity = st.number_input("Quantity", min_value=1, value=1, key="new_quantity")
            with col3:
                unit_price = st.number_input("Unit Price (IDR)", min_value=0, value=1000000, key="new_price")
            with col4:
                if st.button("➕ Add"):
                    st.session_state.order_items.append({
                        'product': product,
                        'quantity': quantity,
                        'unit_price': unit_price,
                        'total': quantity * unit_price
                    })
                    st.rerun()
            
            # Display current items
            if st.session_state.order_items:
                st.subheader("Order Summary")
                
                items_df = pd.DataFrame(st.session_state.order_items)
                items_df['Unit Price'] = items_df['unit_price'].apply(lambda x: format_currency(x, 'IDR'))
                items_df['Total'] = items_df['total'].apply(lambda x: format_currency(x, 'IDR'))
                
                st.dataframe(items_df[['product', 'quantity', 'Unit Price', 'Total']], use_container_width=True)
                
                # Order totals
                subtotal = sum(item['total'] for item in st.session_state.order_items)
                discount_amount = subtotal * (special_discount / 100)
                tax_amount = (subtotal - discount_amount) * 0.11  # 11% PPN
                grand_total = subtotal - discount_amount + tax_amount
                
                col1, col2 = st.columns(2)
                with col2:
                    st.markdown(f"**Subtotal:** {format_currency(subtotal, 'IDR')}")
                    st.markdown(f"**Discount ({special_discount}%):** -{format_currency(discount_amount, 'IDR')}")
                    st.markdown(f"**PPN (11%):** {format_currency(tax_amount, 'IDR')}")
                    st.markdown(f"**Grand Total:** {format_currency(grand_total, 'IDR')}")
            
            # Form submission
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.form_submit_button("💾 Save as Draft", type="secondary"):
                    st.success("Order saved as draft!")
            
            with col2:
                if st.form_submit_button("📤 Submit Order", type="primary"):
                    st.success("Order submitted successfully!")
                    st.session_state.order_items = []  # Clear items
            
            with col3:
                if st.form_submit_button("🗑️ Clear All"):
                    st.session_state.order_items = []
                    st.rerun()
    
    with tab2:
        st.subheader("Draft Orders")
        
        draft_orders = {
            'Order #': ['MOB001', 'MOB002', 'MOB003'],
            'Customer': ['PT. Teknologi Maju', 'CV. Bisnis Sukses', 'UD. Perdagangan Jaya'],
            'Created': ['10-07-2024', '09-07-2024', '08-07-2024'],
            'Total': [format_currency(15000000, 'IDR'), format_currency(8500000, 'IDR'), format_currency(22000000, 'IDR')],
            'Items': ['3 items', '2 items', '5 items'],
            'Action': ['Edit', 'Edit', 'Edit']
        }
        
        df_drafts = pd.DataFrame(draft_orders)
        st.dataframe(df_drafts, use_container_width=True)
    
    with tab3:
        st.subheader("Submitted Orders")
        
        submitted_orders = {
            'Order #': ['ORD001', 'ORD002', 'ORD003', 'ORD004'],
            'Customer': ['PT. Teknologi Maju', 'CV. Bisnis Sukses', 'UD. Perdagangan Jaya', 'Toko Elektronik Sejahtera'],
            'Date': ['08-07-2024', '05-07-2024', '03-07-2024', '01-07-2024'],
            'Total': [format_currency(19500000, 'IDR'), format_currency(8500000, 'IDR'), format_currency(37500000, 'IDR'), format_currency(12000000, 'IDR')],
            'Status': ['✅ Approved', '🟡 Pending', '✅ Delivered', '✅ Paid']
        }
        
        df_submitted = pd.DataFrame(submitted_orders)
        st.dataframe(df_submitted, use_container_width=True)

def show_sales_activities():
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

def show_sales_targets():
    st.header("🎯 Sales Targets & Performance")
    
    tab1, tab2, tab3 = st.tabs(["Current Targets", "Performance Analytics", "Target History"])
    
    with tab1:
        st.subheader("Monthly Targets - July 2024")
        
        # Progress metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Sales Target",
                value=format_currency(50000000, 'IDR'),
                delta=f"{format_currency(35000000, 'IDR')} achieved (70%)"
            )
        
        with col2:
            st.metric(
                label="Visit Target",
                value="20 visits",
                delta="15 completed (75%)"
            )
        
        with col3:
            st.metric(
                label="Customer Target",
                value="10 new customers",
                delta="8 acquired (80%)"
            )
        
        with col4:
            st.metric(
                label="Conversion Rate",
                value="65%",
                delta="15% above target"
            )
        
        # Progress bars
        st.markdown("---")
        st.subheader("Progress Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sales progress
            sales_progress = 70
            st.markdown(f"**Sales Progress: {sales_progress}%**")
            st.progress(sales_progress / 100)
            
            # Visits progress
            visits_progress = 75
            st.markdown(f"**Visits Progress: {visits_progress}%**")
            st.progress(visits_progress / 100)
        
        with col2:
            # Customers progress
            customers_progress = 80
            st.markdown(f"**New Customers Progress: {customers_progress}%**")
            st.progress(customers_progress / 100)
            
            # Overall progress
            overall_progress = (sales_progress + visits_progress + customers_progress) / 3
            st.markdown(f"**Overall Progress: {overall_progress:.0f}%**")
            st.progress(overall_progress / 100)
    
    with tab2:
        st.subheader("Performance Analytics")
        
        # Monthly performance chart
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
        targets = [45000000, 48000000, 50000000, 52000000, 50000000, 55000000, 50000000]
        achieved = [43000000, 49000000, 48000000, 54000000, 52000000, 53000000, 35000000]  # July in progress
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=targets, mode='lines+markers', name='Target', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=months, y=achieved, mode='lines+markers', name='Achieved', line=dict(color='green')))
        
        fig.update_layout(
            title="Monthly Sales Performance",
            xaxis_title="Month",
            yaxis_title="Sales (IDR)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance by customer type
        col1, col2 = st.columns(2)
        
        with col1:
            customer_types = ['New Customers', 'Existing Customers', 'Returning Customers']
            sales_by_type = [15000000, 18000000, 7000000]
            
            fig_pie = px.pie(values=sales_by_type, names=customer_types, title="Sales by Customer Type")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Top performing products
            products = ['Laptop Pro', 'Monitor Stand', 'Keyboard', 'Mouse', 'USB Cable']
            product_sales = [20000000, 8000000, 5000000, 1500000, 500000]
            
            fig_bar = px.bar(x=products, y=product_sales, title="Top Performing Products")
            fig_bar.update_layout(xaxis_title="Products", yaxis_title="Sales (IDR)")
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab3:
        st.subheader("Target History")
        
        target_history = {
            'Period': ['Jul 2024', 'Jun 2024', 'May 2024', 'Apr 2024', 'Mar 2024'],
            'Sales Target': [format_currency(50000000, 'IDR'), format_currency(55000000, 'IDR'), format_currency(50000000, 'IDR'), format_currency(52000000, 'IDR'), format_currency(50000000, 'IDR')],
            'Sales Achieved': [format_currency(35000000, 'IDR'), format_currency(53000000, 'IDR'), format_currency(52000000, 'IDR'), format_currency(54000000, 'IDR'), format_currency(48000000, 'IDR')],
            'Achievement %': ['70%', '96%', '104%', '104%', '96%'],
            'Visit Target': ['20', '25', '20', '22', '20'],
            'Visits Done': ['15', '24', '21', '23', '19'],
            'Status': ['🟡 In Progress', '✅ Achieved', '✅ Exceeded', '✅ Exceeded', '✅ Achieved']
        }
        
        df_targets = pd.DataFrame(target_history)
        st.dataframe(df_targets, use_container_width=True)

def show_expenses():
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

def show_sfa_management():
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

if __name__ == "__main__":
    main()
