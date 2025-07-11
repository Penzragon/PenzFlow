import streamlit as st
from datetime import datetime
import pandas as pd
import pytz

# Indonesian timezone
INDONESIA_TZ = pytz.timezone('Asia/Jakarta')

def get_indonesia_time():
    """Get current time in Indonesian timezone (GMT+7)"""
    return datetime.now(INDONESIA_TZ)

def format_currency(amount, currency='IDR'):
    """Format amount as currency"""
    if currency == 'USD':
        return f"${amount:,.2f}"
    elif currency == 'EUR':
        return f"€{amount:,.2f}"
    elif currency == 'GBP':
        return f"£{amount:,.2f}"
    elif currency == 'IDR':
        # Format Indonesian Rupiah without decimal places
        return f"Rp {amount:,.0f}"
    else:
        return f"{amount:,.2f} {currency}"

def format_date(date_obj, format_str='%d-%m-%Y'):
    """Format date object to string using Indonesian date format (DD-MM-YYYY)"""
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime(format_str)

def format_datetime(datetime_obj, format_str='%d-%m-%Y %H:%M WIB'):
    """Format datetime object to string with Indonesian timezone"""
    if isinstance(datetime_obj, str):
        return datetime_obj
    if datetime_obj.tzinfo is None:
        # If naive datetime, assume it's UTC and convert to Indonesian time
        datetime_obj = pytz.UTC.localize(datetime_obj).astimezone(INDONESIA_TZ)
    return datetime_obj.strftime(format_str)

def format_phone(phone):
    """Format phone number"""
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, phone))
    
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone

def generate_order_number():
    """Generate unique order number"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"ORD{timestamp}"

def generate_sku(category, sequence):
    """Generate SKU for products"""
    category_code = category[:3].upper()
    return f"{category_code}{sequence:03d}"

def calculate_total_with_tax(subtotal, tax_rate=0.08):
    """Calculate total amount including tax"""
    tax_amount = subtotal * tax_rate
    total = subtotal + tax_amount
    return {
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'total': total
    }

def validate_email(email):
    """Simple email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Simple phone validation"""
    digits = ''.join(filter(str.isdigit, phone))
    return len(digits) >= 10

def get_status_color(status):
    """Get color for status indicators"""
    status_colors = {
        'active': 'green',
        'inactive': 'red',
        'pending': 'orange',
        'completed': 'green',
        'shipped': 'blue',
        'processing': 'orange',
        'cancelled': 'red',
        'in_stock': 'green',
        'low_stock': 'orange',
        'out_of_stock': 'red'
    }
    return status_colors.get(status.lower(), 'gray')

def create_download_link(df, filename, text="Download CSV"):
    """Create download link for DataFrame"""
    csv = df.to_csv(index=False)
    st.download_button(
        label=text,
        data=csv,
        file_name=filename,
        mime='text/csv'
    )

def show_success_message(message):
    """Show success message with custom styling"""
    st.success(f"✅ {message}")

def show_error_message(message):
    """Show error message with custom styling"""
    st.error(f"❌ {message}")

def show_warning_message(message):
    """Show warning message with custom styling"""
    st.warning(f"⚠️ {message}")

def show_info_message(message):
    """Show info message with custom styling"""
    st.info(f"ℹ️ {message}")

def create_metric_card(title, value, delta=None, help_text=None):
    """Create a styled metric card"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if delta:
            st.metric(
                label=title,
                value=value,
                delta=delta,
                help=help_text
            )
        else:
            st.metric(
                label=title,
                value=value,
                help=help_text
            )

def safe_divide(numerator, denominator):
    """Safe division that handles division by zero"""
    if denominator == 0:
        return 0
    return numerator / denominator

def get_date_range_options():
    """Get predefined date range options"""
    from datetime import datetime, timedelta
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    year_ago = today - timedelta(days=365)
    
    return {
        'Today': (today, today),
        'Yesterday': (yesterday, yesterday),
        'Last 7 Days': (week_ago, today),
        'Last 30 Days': (month_ago, today),
        'Last Year': (year_ago, today)
    }

def export_to_excel(dataframes_dict, filename):
    """Export multiple DataFrames to Excel with different sheets"""
    from io import BytesIO
    import pandas as pd
    
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for sheet_name, df in dataframes_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    output.seek(0)
    
    st.download_button(
        label=f"📄 Download {filename}",
        data=output.getvalue(),
        file_name=filename,
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
