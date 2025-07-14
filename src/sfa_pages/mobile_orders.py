import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.helpers import format_currency

def show_mobile_orders():
    """Mobile Order Management for Field Sales"""
    st.header("📱 Mobile Orders")
    
    tab1, tab2, tab3 = st.tabs(["Create Order", "My Orders", "Order Templates"])
    
    with tab1:
        st.subheader("📝 Create New Order")
        
        # Order header
        with st.form("mobile_order"):
            # Customer selection
            col1, col2 = st.columns(2)
            with col1:
                customer = st.selectbox(
                    "Select Customer",
                    ["PT. Teknologi Maju", "CV. Bisnis Sukses", "UD. Perdagangan Jaya", "PT. Solusi Digital", "New Customer"]
                )
                if customer == "New Customer":
                    new_customer_name = st.text_input("Customer Name")
                    new_customer_phone = st.text_input("Phone Number")
            
            with col2:
                order_date = st.date_input("Order Date", value=date.today())
                payment_terms = st.selectbox("Payment Terms", ["Cash", "Net 7", "Net 15", "Net 30"])
            
            # Visit reference
            visit_ref = st.selectbox("Link to Visit", ["Current Visit", "Standalone Order", "Follow-up Visit"])
            
            st.markdown("---")
            st.subheader("🛒 Order Items")
            
            # Initialize order items in session state
            if 'mobile_order_items' not in st.session_state:
                st.session_state.mobile_order_items = []
            
            # Product selection
            col1, col2, col3, col4, col5 = st.columns([3, 1, 2, 2, 1])
            
            with col1:
                product = st.selectbox("Product", ["Laptop Pro", "Wireless Mouse", "USB Cable", "Monitor Stand", "Keyboard"])
            with col2:
                quantity = st.number_input("Qty", min_value=1, value=1)
            with col3:
                # Auto-fill price based on product
                if product == "Laptop Pro":
                    unit_price = 14999000
                elif product == "Wireless Mouse":
                    unit_price = 449000
                elif product == "USB Cable":
                    unit_price = 149000
                elif product == "Monitor Stand":
                    unit_price = 749000
                else:
                    unit_price = 1199000
                
                st.write(f"Unit Price: {format_currency(unit_price, 'IDR')}")
            with col4:
                discount = st.number_input("Discount %", min_value=0.0, max_value=50.0, value=0.0, step=0.5)
            with col5:
                if st.button("➕ Add"):
                    item_total = unit_price * quantity * (1 - discount/100)
                    st.session_state.mobile_order_items.append({
                        'product': product,
                        'quantity': quantity,
                        'unit_price': unit_price,
                        'discount': discount,
                        'total': item_total
                    })
                    st.success(f"Added {product}")
            
            # Display added items
            if st.session_state.mobile_order_items:
                st.subheader("📋 Order Summary")
                
                items_data = []
                total_amount = 0
                
                for i, item in enumerate(st.session_state.mobile_order_items):
                    items_data.append({
                        'Product': item['product'],
                        'Quantity': item['quantity'],
                        'Unit Price': format_currency(item['unit_price'], 'IDR'),
                        'Discount': f"{item['discount']}%",
                        'Total': format_currency(item['total'], 'IDR')
                    })
                    total_amount += item['total']
                    
                    # Remove button for each item
                    if st.button(f"❌ Remove {item['product']}", key=f"remove_{i}"):
                        st.session_state.mobile_order_items.pop(i)
                        st.rerun()
                
                df_items = pd.DataFrame(items_data)
                st.dataframe(df_items, use_container_width=True)
                
                # Order totals
                col1, col2 = st.columns(2)
                with col1:
                    additional_discount = st.number_input("Additional Discount %", min_value=0.0, max_value=20.0, value=0.0)
                    tax_rate = st.number_input("Tax %", min_value=0.0, value=11.0)
                
                with col2:
                    subtotal = total_amount
                    additional_discount_amount = subtotal * (additional_discount / 100)
                    taxable_amount = subtotal - additional_discount_amount
                    tax_amount = taxable_amount * (tax_rate / 100)
                    final_total = taxable_amount + tax_amount
                    
                    st.metric("Subtotal", format_currency(subtotal, 'IDR'))
                    st.metric("Total Discount", format_currency(additional_discount_amount, 'IDR'))
                    st.metric("Tax", format_currency(tax_amount, 'IDR'))
                    st.metric("**Final Total**", format_currency(final_total, 'IDR'))
            
            # Order notes
            special_instructions = st.text_area("Special Instructions", placeholder="Delivery notes, customer requirements, etc.")
            
            # Submit order
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.form_submit_button("💾 Save as Draft", use_container_width=True):
                    st.info("Order saved as draft!")
            
            with col2:
                if st.form_submit_button("📤 Submit Order", use_container_width=True):
                    if st.session_state.mobile_order_items:
                        st.success("✅ Order submitted successfully!")
                        st.balloons()
                        # Clear items after submission
                        st.session_state.mobile_order_items = []
                    else:
                        st.error("Please add at least one item to the order")
            
            with col3:
                if st.form_submit_button("🖨️ Print & Submit", use_container_width=True):
                    st.info("Generating printable order...")
    
    with tab2:
        st.subheader("📊 My Order History")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Status", ["All", "Draft", "Submitted", "Approved", "Rejected"])
        with col2:
            date_from = st.date_input("From", value=date.today().replace(day=1))
        with col3:
            date_to = st.date_input("To", value=date.today())
        
        # Order history data
        orders_data = {
            'Order #': ['MO001', 'MO002', 'MO003', 'MO004', 'MO005'],
            'Date': ['2024-01-20', '2024-01-19', '2024-01-18', '2024-01-17', '2024-01-16'],
            'Customer': ['PT. Teknologi Maju', 'CV. Bisnis Sukses', 'UD. Perdagangan Jaya', 'PT. Solusi Digital', 'CV. Maju Bersama'],
            'Amount': [format_currency(15000000, 'IDR'), format_currency(2500000, 'IDR'), format_currency(8500000, 'IDR'), format_currency(12000000, 'IDR'), format_currency(3200000, 'IDR')],
            'Status': ['✅ Approved', '📋 Submitted', '✅ Approved', '❌ Rejected', '💾 Draft'],
            'Items': ['3 items', '2 items', '5 items', '1 item', '2 items']
        }
        
        df_orders = pd.DataFrame(orders_data)
        
        # Order statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Orders", "25", "5")
        with col2:
            st.metric("This Month", "8", "3")
        with col3:
            st.metric("Approval Rate", "85%", "5%")
        with col4:
            st.metric("Total Value", format_currency(125000000, 'IDR'), "15%")
        
        # Orders table
        for idx, row in df_orders.iterrows():
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1])
                
                with col1:
                    st.write(f"**{row['Order #']}** - {row['Date']}")
                    st.write(f"👤 {row['Customer']}")
                
                with col2:
                    st.write(f"**Amount:** {row['Amount']}")
                    st.write(f"**Items:** {row['Items']}")
                
                with col3:
                    if row['Status'] == '✅ Approved':
                        st.success(row['Status'])
                    elif row['Status'] == '❌ Rejected':
                        st.error(row['Status'])
                    elif row['Status'] == '💾 Draft':
                        st.info(row['Status'])
                    else:
                        st.warning(row['Status'])
                
                with col4:
                    if st.button("👁️", key=f"view_order_{idx}", help="View details"):
                        show_order_details(row['Order #'])
                
                with col5:
                    if row['Status'] == '💾 Draft':
                        if st.button("✏️", key=f"edit_order_{idx}", help="Edit"):
                            st.info(f"Editing order {row['Order #']}")
                    else:
                        if st.button("📄", key=f"invoice_{idx}", help="Invoice"):
                            st.info(f"Generating invoice for {row['Order #']}")
                
                st.markdown("---")
    
    with tab3:
        st.subheader("📋 Order Templates")
        
        st.info("Create reusable order templates for frequently ordered product combinations.")
        
        # Create new template
        with st.expander("➕ Create New Template"):
            template_name = st.text_input("Template Name", placeholder="e.g., Standard Office Package")
            template_description = st.text_area("Description", placeholder="Describe what this template contains")
            
            # Template items
            st.write("**Template Items:**")
            template_items = st.multiselect(
                "Select Products",
                ["Laptop Pro", "Wireless Mouse", "USB Cable", "Monitor Stand", "Keyboard"]
            )
            
            if st.button("💾 Save Template"):
                if template_name and template_items:
                    st.success(f"Template '{template_name}' saved successfully!")
                else:
                    st.error("Please provide a name and select at least one product")
        
        # Existing templates
        templates_data = {
            'Template': ['Basic Office Setup', 'Executive Package', 'Bulk Order Standard'],
            'Items': ['3 products', '5 products', '2 products'],
            'Est. Value': [format_currency(5000000, 'IDR'), format_currency(25000000, 'IDR'), format_currency(50000000, 'IDR')],
            'Usage': ['15 times', '8 times', '3 times']
        }
        
        df_templates = pd.DataFrame(templates_data)
        
        for idx, row in df_templates.iterrows():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**{row['Template']}**")
                st.write(f"Items: {row['Items']} | Value: {row['Est. Value']} | Used: {row['Usage']}")
            
            with col2:
                if st.button("📝 Use Template", key=f"use_template_{idx}"):
                    st.success(f"Loading template: {row['Template']}")
            
            with col3:
                if st.button("✏️ Edit", key=f"edit_template_{idx}"):
                    st.info(f"Editing template: {row['Template']}")

def show_order_details(order_number):
    """Show detailed order information"""
    st.subheader(f"Order Details - {order_number}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Order Information**")
        st.write(f"Order #: {order_number}")
        st.write("Customer: PT. Teknologi Maju")
        st.write("Date: 2024-01-20")
        st.write("Status: Approved")
        st.write("Payment Terms: Net 30")
    
    with col2:
        st.write("**Financial Summary**")
        st.metric("Subtotal", format_currency(15000000, 'IDR'))
        st.metric("Tax", format_currency(1650000, 'IDR'))
        st.metric("Total", format_currency(16650000, 'IDR'))
    
    # Order items
    st.subheader("Order Items")
    items_detail = {
        'Product': ['Laptop Pro', 'Wireless Mouse', 'USB Cable'],
        'Quantity': [1, 2, 5],
        'Unit Price': [format_currency(14999000, 'IDR'), format_currency(449000, 'IDR'), format_currency(149000, 'IDR')],
        'Total': [format_currency(14999000, 'IDR'), format_currency(898000, 'IDR'), format_currency(745000, 'IDR')]
    }
    
    df_items_detail = pd.DataFrame(items_detail)
    st.dataframe(df_items_detail, use_container_width=True)
