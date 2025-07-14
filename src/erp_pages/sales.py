import streamlit as st
import pandas as pd
from utils.helpers import format_currency
from datetime import datetime, date

def show_sales():
    """Sales Management Page"""
    st.header("💰 Sales Management")
    
    tab1, tab2, tab3 = st.tabs(["Sales Orders", "Create New Order", "Quotations"])
    
    with tab1:
        # Sample sales data
        sales_data = {
            'Order ID': ['ORD001', 'ORD002', 'ORD003', 'ORD004', 'ORD005'],
            'Customer': ['Budi Santoso', 'Sari Wulandari', 'Ahmad Rahman', 'Dewi Kusuma', 'Rizki Pratama'],
            'Date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19'],
            'Amount': [format_currency(19500000, 'IDR'), format_currency(1350000, 'IDR'), format_currency(37500000, 'IDR'), format_currency(9000000, 'IDR'), format_currency(3000000, 'IDR')],
            'Status': ['✅ Completed', '⏳ Pending', '🚚 Shipped', '⚙️ Processing', '✅ Completed']
        }
        
        df = pd.DataFrame(sales_data)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Completed", "Pending", "Shipped", "Processing"])
        with col2:
            date_from = st.date_input("From Date", value=date(2024, 1, 1))
        with col3:
            date_to = st.date_input("To Date", value=date.today())
        
        st.dataframe(df, use_container_width=True)
        
        # Sales actions
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📊 Sales Report"):
                st.info("Sales report feature coming soon!")
        with col2:
            if st.button("📧 Send Invoice"):
                st.info("Invoice generation feature coming soon!")
        with col3:
            if st.button("🔄 Bulk Update"):
                st.info("Bulk update feature coming soon!")
        with col4:
            if st.button("📤 Export"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="sales_orders.csv",
                    mime="text/csv"
                )
    
    with tab2:
        st.subheader("Create New Sales Order")
        with st.form("create_order"):
            # Customer selection
            col1, col2 = st.columns(2)
            with col1:
                customer = st.selectbox("Customer", ["Budi Santoso", "Sari Wulandari", "Ahmad Rahman", "Dewi Kusuma"])
                order_date = st.date_input("Order Date", value=date.today())
            with col2:
                payment_method = st.selectbox("Payment Method", ["Cash", "Bank Transfer", "Credit Card", "Check"])
                payment_terms = st.selectbox("Payment Terms", ["Cash on Delivery", "Net 30", "Net 15", "Net 7", "Advance Payment"])
            
            sales_rep = st.text_input("Sales Representative", value=st.session_state.get('username', ''))
            
            st.subheader("Order Items")
            
            # Dynamic order items
            if 'order_items' not in st.session_state:
                st.session_state.order_items = [{'product': '', 'quantity': 1, 'price': 0}]
            
            for i, item in enumerate(st.session_state.order_items):
                col1, col2, col3, col4 = st.columns([3, 1, 2, 1])
                with col1:
                    product = st.selectbox(f"Product {i+1}", ["Laptop Pro", "Wireless Mouse", "USB Cable", "Monitor Stand"], key=f"product_{i}")
                with col2:
                    quantity = st.number_input(f"Qty {i+1}", min_value=1, value=1, key=f"qty_{i}")
                with col3:
                    if product == "Laptop Pro":
                        price = 14999000
                    elif product == "Wireless Mouse":
                        price = 449000
                    elif product == "USB Cable":
                        price = 149000
                    else:
                        price = 749000
                    st.write(f"Price: {format_currency(price, 'IDR')}")
                with col4:
                    if st.button(f"❌", key=f"remove_{i}"):
                        if len(st.session_state.order_items) > 1:
                            st.session_state.order_items.pop(i)
                            st.rerun()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➕ Add Item"):
                    st.session_state.order_items.append({'product': '', 'quantity': 1, 'price': 0})
                    st.rerun()
            
            # Order summary
            st.subheader("Order Summary")
            col1, col2 = st.columns(2)
            with col1:
                discount = st.number_input("Discount (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
                tax_rate = st.number_input("Tax (%)", min_value=0.0, max_value=100.0, value=11.0, step=0.5)
            
            with col2:
                subtotal = 19500000  # Calculate based on items
                discount_amount = subtotal * (discount / 100)
                tax_amount = (subtotal - discount_amount) * (tax_rate / 100)
                total = subtotal - discount_amount + tax_amount
                
                st.metric("Subtotal", format_currency(subtotal, 'IDR'))
                st.metric("Total", format_currency(total, 'IDR'))
            
            notes = st.text_area("Order Notes", placeholder="Special instructions or comments")
            
            if st.form_submit_button("Create Order", use_container_width=True):
                st.success("✅ Sales order created successfully!")
                st.balloons()
                # Clear order items
                st.session_state.order_items = [{'product': '', 'quantity': 1, 'price': 0}]
    
    with tab3:
        st.subheader("Quotations")
        
        # Sample quotations data
        quotations_data = {
            'Quote ID': ['QUO001', 'QUO002', 'QUO003'],
            'Customer': ['Budi Santoso', 'Ahmad Rahman', 'Dewi Kusuma'],
            'Date': ['2024-01-10', '2024-01-12', '2024-01-14'],
            'Amount': [format_currency(15000000, 'IDR'), format_currency(8500000, 'IDR'), format_currency(22000000, 'IDR')],
            'Valid Until': ['2024-02-10', '2024-02-12', '2024-02-14'],
            'Status': ['📋 Pending', '✅ Accepted', '❌ Rejected']
        }
        
        df_quotes = pd.DataFrame(quotations_data)
        st.dataframe(df_quotes, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Create Quotation", use_container_width=True):
                st.info("Quotation creation feature coming soon!")
        with col2:
            if st.button("🔄 Convert to Order", use_container_width=True):
                st.info("Quote conversion feature coming soon!")

def show_order_details(order_id):
    """Show detailed order information"""
    st.subheader(f"Order Details - {order_id}")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Order Info", "Items", "Payments", "Delivery"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Order Information**")
            st.write("Order ID: ORD001")
            st.write("Customer: Budi Santoso")
            st.write("Date: 2024-01-15")
            st.write("Status: Completed")
        
        with col2:
            st.write("**Financial Summary**")
            st.metric("Subtotal", format_currency(19500000, 'IDR'))
            st.metric("Tax", format_currency(1950000, 'IDR'))
            st.metric("Total", format_currency(21450000, 'IDR'))
    
    with tab2:
        st.write("Order items will be displayed here")
    
    with tab3:
        st.write("Payment information will be displayed here")
    
    with tab4:
        st.write("Delivery tracking information will be displayed here")
