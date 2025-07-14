import streamlit as st
import pandas as pd
from utils.helpers import format_currency
from utils.translations import t
from datetime import datetime, date, timedelta

def show_sales():
    """Sales Management Page"""
    st.header(f"💰 {t('sales')}")
    
    tab1, tab2, tab3, tab4 = st.tabs([t("sales_report"), t("new_sale"), "Outstanding Payments", "Order History"])
    
    with tab1:
        show_sales_list()
    
    with tab2:
        show_create_sale()
    
    with tab3:
        show_outstanding_payments()
    
    with tab4:
        show_order_history()

def show_sales_list():
    """Display sales list with filters"""
    st.subheader(f"📋 {t('sales_report')}")
    
    # Sample sales data with Indonesian context
    sales_data = {
        'Order ID': ['PF001', 'PF002', 'PF003', 'PF004', 'PF005', 'PF006'],
        'Date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19', '2024-01-20'],
        'Customer': ['Toko Sari Rasa', 'Warung Maju Jaya', 'Supermarket Harapan', 'Toko Berkah', 'Minimarket Sejahtera', 'Toko Makmur'],
        'Salesman': ['Budi Santoso', 'Ahmad Rahman', 'Sari Wulandari', 'Budi Santoso', 'Dewi Kusuma', 'Ahmad Rahman'],
        'Total Amount': [
            format_currency(2750000, 'IDR'),  # Mixed FMCG order
            format_currency(1320000, 'IDR'),  # Beverages order
            format_currency(5420000, 'IDR'),  # Large mixed order
            format_currency(890000, 'IDR'),   # Small snacks order
            format_currency(3150000, 'IDR'),  # Medium mixed order
            format_currency(1680000, 'IDR')   # Beverages + snacks
        ],
        'Payment Status': ['✅ Paid', '⏳ Partial', '🔴 Unpaid', '✅ Paid', '⏳ Partial', '✅ Paid'],
        'Outstanding': [
            format_currency(0, 'IDR'),
            format_currency(520000, 'IDR'),
            format_currency(5420000, 'IDR'),
            format_currency(0, 'IDR'),
            format_currency(1500000, 'IDR'),
            format_currency(0, 'IDR')
        ]
    }
    
    df = pd.DataFrame(sales_data)
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status_filter = st.selectbox(f"{t('filter')} {t('payment_status')}", 
                                   [t("all"), t("paid"), t("partial"), t("unpaid")])
    with col2:
        salesman_filter = st.selectbox(f"{t('filter')} Salesman", 
                                     ["All", "Budi Santoso", "Ahmad Rahman", "Sari Wulandari", "Dewi Kusuma"])
    with col3:
        date_from = st.date_input(t("from_date"), value=date(2024, 1, 1))
    with col4:
        date_to = st.date_input(t("to_date"), value=date.today())
    
    # Apply filters
    filtered_df = df
    if status_filter != t("all"):
        if status_filter == t("paid"):
            filtered_df = filtered_df[filtered_df['Payment Status'].str.contains('Paid')]
        elif status_filter == t("partial"):
            filtered_df = filtered_df[filtered_df['Payment Status'].str.contains('Partial')]
        elif status_filter == t("unpaid"):
            filtered_df = filtered_df[filtered_df['Payment Status'].str.contains('Unpaid')]
    
    if salesman_filter != "All":
        filtered_df = filtered_df[filtered_df['Salesman'] == salesman_filter]
    
    st.dataframe(filtered_df, use_container_width=True)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_sales = sum([2750000, 1320000, 5420000, 890000, 3150000, 1680000])
        st.metric(f"Total {t('sales')}", format_currency(total_sales, 'IDR'))
    with col2:
        paid_amount = total_sales - (520000 + 5420000 + 1500000)
        st.metric(f"{t('paid')} Amount", format_currency(paid_amount, 'IDR'))
    with col3:
        outstanding_amount = 520000 + 5420000 + 1500000
        st.metric("Outstanding", format_currency(outstanding_amount, 'IDR'))
    with col4:
        st.metric("Total Orders", len(df))

def show_create_sale():
    """Create new sales order with comprehensive form"""
    st.subheader(f"🆕 {t('new_sale')}")
    
    # Basic order information - Outside form for easier interaction
    st.markdown(f"### 📋 Order Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sale_date = st.date_input(t("sale_date"), value=date.today())
        order_id = st.text_input("Order ID", value=f"PF{datetime.now().strftime('%Y%m%d%H%M')}", disabled=True)
    
    with col2:
        # Customer selection with FMCG customers
        customers = [
            "Toko Sari Rasa", "Warung Maju Jaya", "Supermarket Harapan", 
            "Toko Berkah", "Minimarket Sejahtera", "Toko Makmur",
            "Warung Bu Siti", "Toko Sembako Jaya", "Minimarket Rezeki"
        ]
        customer = st.selectbox(t("customer"), customers)
    
    with col3:
        # Salesman selection
        salesmen = ["Budi Santoso", "Ahmad Rahman", "Sari Wulandari", "Dewi Kusuma", "Rizki Pratama"]
        salesman = st.selectbox("Salesman", salesmen, 
                              index=0 if st.session_state.get('username') not in salesmen 
                              else salesmen.index(st.session_state.get('username', salesmen[0])))
    
    # Order items section - Outside form for dynamic interaction
    st.markdown(f"### 🛒 {t('order_items')}")
    
    # Initialize order items in session state
    if 'sale_items' not in st.session_state:
        st.session_state.sale_items = []
    
    # Product catalog with FMCG products
    products_catalog = {
        "Aqua 600ml": {"price": 3000, "category": "Beverages"},
        "Aqua 1L": {"price": 5000, "category": "Beverages"},
        "Aqua Galon 19L": {"price": 25000, "category": "Beverages"},
        "Indomie Goreng": {"price": 3500, "category": "Food"},
        "Indomie Soto": {"price": 3500, "category": "Food"},
        "Chitato BBQ 68g": {"price": 8000, "category": "Snacks"},
        "Chitato Sapi Panggang 68g": {"price": 8000, "category": "Snacks"},
        "Gula Pasir 1kg": {"price": 15000, "category": "Groceries"},
        "Beras Premium 5kg": {"price": 75000, "category": "Groceries"},
        "Minyak Goreng 2L": {"price": 32000, "category": "Groceries"}
    }
    
    # Add item interface
    col1, col2, col3, col4 = st.columns([3, 1, 2, 1])
    with col1:
        new_product = st.selectbox("Select Product", list(products_catalog.keys()), key="new_product")
    with col2:
        new_quantity = st.number_input(t("quantity"), min_value=1, value=1, key="new_quantity")
    with col3:
        if new_product:
            unit_price = products_catalog[new_product]["price"]
            st.write(f"Unit Price: {format_currency(unit_price, 'IDR')}")
            
            # Tiered pricing for bulk orders
            if new_quantity >= 100:
                bulk_price = int(unit_price * 0.85)  # 15% discount
                st.write(f"Bulk Price: {format_currency(bulk_price, 'IDR')}")
            elif new_quantity >= 50:
                bulk_price = int(unit_price * 0.9)   # 10% discount
                st.write(f"Bulk Price: {format_currency(bulk_price, 'IDR')}")
            else:
                bulk_price = unit_price
    with col4:
        if st.button(f"➕ {t('add_item')}", key="add_item_btn"):
            if new_product and new_quantity > 0:
                # Calculate price based on quantity
                if new_quantity >= 100:
                    price = int(unit_price * 0.85)
                elif new_quantity >= 50:
                    price = int(unit_price * 0.9)
                else:
                    price = unit_price
                
                item = {
                    'product': new_product,
                    'quantity': new_quantity,
                    'unit_price': price,
                    'subtotal': price * new_quantity
                }
                st.session_state.sale_items.append(item)
                st.rerun()
    
    # Display added items
    if st.session_state.sale_items:
        st.markdown("#### Current Order Items")
        items_data = []
        total_amount = 0
        
        for i, item in enumerate(st.session_state.sale_items):
            items_data.append({
                'Product': item['product'],
                'Quantity': item['quantity'],
                'Unit Price': format_currency(item['unit_price'], 'IDR'),
                'Subtotal': format_currency(item['subtotal'], 'IDR')
            })
            total_amount += item['subtotal']
        
        df_items = pd.DataFrame(items_data)
        st.dataframe(df_items, use_container_width=True)
        
        # Remove item functionality
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.session_state.sale_items:
                item_to_remove = st.selectbox("Remove item", 
                                            [f"{item['product']} (Qty: {item['quantity']})" 
                                             for item in st.session_state.sale_items])
        with col2:
            if st.button(f"🗑️ {t('remove_item')}", key="remove_item_btn"):
                if st.session_state.sale_items:
                    # Find and remove the selected item
                    for i, item in enumerate(st.session_state.sale_items):
                        if f"{item['product']} (Qty: {item['quantity']})" == item_to_remove:
                            st.session_state.sale_items.pop(i)
                            st.rerun()
                            break
    
    # Payment and delivery information form
    with st.form("sale_details"):
        st.markdown(f"### 💳 Payment & Delivery")
        col1, col2 = st.columns(2)
        
        with col1:
            payment_method = st.selectbox(t("payment_method"), [t("cash"), t("credit"), t("transfer"), "Check"])
            payment_status = st.selectbox(t("payment_status"), [t("paid"), t("partial"), t("unpaid")])
            
            paid_amount = 0
            if payment_status == t("partial"):
                if st.session_state.sale_items:
                    total_amount = sum(item['subtotal'] for item in st.session_state.sale_items)
                    paid_amount = st.number_input("Amount Paid (IDR)", min_value=0, max_value=total_amount, value=0)
                    st.write(f"Outstanding: {format_currency(total_amount - paid_amount, 'IDR')}")
            
        with col2:
            delivery_date = st.date_input(t("delivery_date"), value=date.today() + timedelta(days=1))
            delivery_address = st.text_area("Delivery Address", placeholder="Complete delivery address")
        
        # Order summary
        if st.session_state.sale_items:
            st.markdown(f"### 📊 Order Summary")
            col1, col2 = st.columns(2)
            
            with col1:
                subtotal = sum(item['subtotal'] for item in st.session_state.sale_items)
                discount = st.number_input(f"{t('discount')} (%)", min_value=0.0, max_value=50.0, value=0.0, step=0.5)
                tax_rate = st.number_input(f"{t('tax')} (%)", min_value=0.0, max_value=15.0, value=11.0, step=0.5)
            
            with col2:
                discount_amount = subtotal * (discount / 100)
                tax_amount = (subtotal - discount_amount) * (tax_rate / 100)
                total = subtotal - discount_amount + tax_amount
                
                st.metric(t("subtotal"), format_currency(subtotal, 'IDR'))
                st.metric(f"{t('discount')} Amount", format_currency(discount_amount, 'IDR'))
                st.metric(f"{t('tax')} Amount", format_currency(tax_amount, 'IDR'))
                st.metric(t("grand_total"), format_currency(total, 'IDR'))
        
        # Special instructions
        special_instructions = st.text_area(t("special_instructions"), 
                                          placeholder="Special delivery instructions, packaging requirements, etc.")
        
        # Form submission
        col1, col2 = st.columns(2)
        with col1:
            submit_order = st.form_submit_button(f"💾 {t('save')} Order", use_container_width=True)
        with col2:
            clear_all = st.form_submit_button("🗑️ Clear All", use_container_width=True)
        
        # Handle form submissions
        if submit_order:
            if customer and salesman and st.session_state.sale_items:
                st.success(f"✅ {t('sale_created')} Order ID: {order_id}")
                st.balloons()
                # Clear the items after successful creation
                st.session_state.sale_items = []
                st.rerun()
            else:
                st.error(f"❌ {t('error')}: Please fill customer, salesman, and add at least one item")
        
        if clear_all:
            st.session_state.sale_items = []
            st.rerun()

def show_outstanding_payments():
    """Show customers with outstanding payments"""
    st.subheader("💳 Outstanding Payments")
    
    # Outstanding payments data
    outstanding_data = {
        'Customer': ['Warung Maju Jaya', 'Supermarket Harapan', 'Minimarket Sejahtera'],
        'Order ID': ['PF002', 'PF003', 'PF005'],
        'Order Date': ['2024-01-16', '2024-01-17', '2024-01-19'],
        'Total Amount': [
            format_currency(1320000, 'IDR'),
            format_currency(5420000, 'IDR'),
            format_currency(3150000, 'IDR')
        ],
        'Paid Amount': [
            format_currency(800000, 'IDR'),
            format_currency(0, 'IDR'),
            format_currency(1650000, 'IDR')
        ],
        'Outstanding': [
            format_currency(520000, 'IDR'),
            format_currency(5420000, 'IDR'),
            format_currency(1500000, 'IDR')
        ],
        'Days Overdue': [5, 8, 2],
        'Salesman': ['Ahmad Rahman', 'Sari Wulandari', 'Dewi Kusuma']
    }
    
    df_outstanding = pd.DataFrame(outstanding_data)
    st.dataframe(df_outstanding, use_container_width=True)
    
    # Outstanding summary
    col1, col2, col3 = st.columns(3)
    with col1:
        total_outstanding = 520000 + 5420000 + 1500000
        st.metric("Total Outstanding", format_currency(total_outstanding, 'IDR'))
    with col2:
        st.metric("Overdue Orders", len(df_outstanding))
    with col3:
        avg_overdue = sum([5, 8, 2]) / len(df_outstanding)
        st.metric("Avg Days Overdue", f"{avg_overdue:.1f}")
    
    # Quick payment recording
    st.markdown("---")
    st.subheader("📝 Record Payment")
    
    with st.form("record_payment"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            payment_customer = st.selectbox("Customer", df_outstanding['Customer'].tolist())
            payment_amount = st.number_input("Payment Amount (IDR)", min_value=0, value=0)
        
        with col2:
            payment_date = st.date_input("Payment Date", value=date.today())
            payment_method = st.selectbox("Payment Method", ["Cash", "Bank Transfer", "Check"])
        
        with col3:
            payment_notes = st.text_area("Payment Notes", placeholder="Reference number, notes, etc.")
        
        if st.form_submit_button("� Record Payment", use_container_width=True):
            if payment_customer and payment_amount > 0:
                st.success(f"✅ Payment of {format_currency(payment_amount, 'IDR')} recorded for {payment_customer}")
            else:
                st.error("❌ Please select customer and enter payment amount")

def show_order_history():
    """Show complete order history with detailed information"""
    st.subheader("📚 Order History")
    
    # Comprehensive order history
    history_data = {
        'Order ID': ['PF001', 'PF002', 'PF003', 'PF004', 'PF005', 'PF006', 'PF007', 'PF008'],
        'Date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19', '2024-01-20', '2024-01-21', '2024-01-22'],
        'Customer': ['Toko Sari Rasa', 'Warung Maju Jaya', 'Supermarket Harapan', 'Toko Berkah', 
                    'Minimarket Sejahtera', 'Toko Makmur', 'Warung Bu Siti', 'Toko Sembako Jaya'],
        'Salesman': ['Budi Santoso', 'Ahmad Rahman', 'Sari Wulandari', 'Budi Santoso', 
                    'Dewi Kusuma', 'Ahmad Rahman', 'Rizki Pratama', 'Sari Wulandari'],
        'Items': ['5 items', '3 items', '8 items', '2 items', '6 items', '4 items', '3 items', '7 items'],
        'Total': [
            format_currency(2750000, 'IDR'), format_currency(1320000, 'IDR'), format_currency(5420000, 'IDR'),
            format_currency(890000, 'IDR'), format_currency(3150000, 'IDR'), format_currency(1680000, 'IDR'),
            format_currency(2100000, 'IDR'), format_currency(4320000, 'IDR')
        ],
        'Status': ['✅ Delivered', '🚚 Shipped', '⏳ Processing', '✅ Delivered', 
                  '🚚 Shipped', '✅ Delivered', '⏳ Processing', '📋 Confirmed'],
        'Payment': ['✅ Paid', '⏳ Partial', '🔴 Unpaid', '✅ Paid', '⏳ Partial', '✅ Paid', '✅ Paid', '✅ Paid']
    }
    
    df_history = pd.DataFrame(history_data)
    
    # Filters for history
    col1, col2, col3 = st.columns(3)
    with col1:
        history_customer = st.selectbox("Filter by Customer", ["All"] + list(df_history['Customer'].unique()))
    with col2:
        history_salesman = st.selectbox("Filter by Salesman", ["All"] + list(df_history['Salesman'].unique()))
    with col3:
        history_status = st.selectbox("Filter by Status", ["All", "Delivered", "Shipped", "Processing", "Confirmed"])
    
    # Apply filters
    filtered_history = df_history
    if history_customer != "All":
        filtered_history = filtered_history[filtered_history['Customer'] == history_customer]
    if history_salesman != "All":
        filtered_history = filtered_history[filtered_history['Salesman'] == history_salesman]
    if history_status != "All":
        filtered_history = filtered_history[filtered_history['Status'].str.contains(history_status)]
    
    st.dataframe(filtered_history, use_container_width=True)
    
    # Export functionality
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📤 Export History"):
            csv = filtered_history.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"order_history_{date.today().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    with col2:
        if st.button("📊 Generate Report"):
            st.info("Detailed report generation feature coming soon!")
    with col3:
        if st.button("📧 Email Report"):
            st.info("Email report feature coming soon!")
