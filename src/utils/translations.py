"""
Internationalization module for PenzFlow
Supports English and Indonesian languages
"""
import streamlit as st

# Translation dictionaries
TRANSLATIONS = {
    'en': {
        # General
        'app_title': 'PenzFlow - ERP & SFA System',
        'language': 'Language',
        'welcome': 'Welcome',
        'login': 'Login',
        'logout': 'Logout',
        'username': 'Username',
        'password': 'Password',
        'role': 'Role',
        'submit': 'Submit',
        'cancel': 'Cancel',
        'save': 'Save',
        'delete': 'Delete',
        'edit': 'Edit',
        'add': 'Add',
        'search': 'Search',
        'filter': 'Filter',
        'export': 'Export',
        'import': 'Import',
        'refresh': 'Refresh',
        'back': 'Back',
        'next': 'Next',
        'previous': 'Previous',
        'close': 'Close',
        'confirm': 'Confirm',
        'success': 'Success',
        'error': 'Error',
        'warning': 'Warning',
        'info': 'Information',
        'loading': 'Loading...',
        'no_data': 'No data available',
        'total': 'Total',
        'amount': 'Amount',
        'quantity': 'Quantity',
        'price': 'Price',
        'date': 'Date',
        'time': 'Time',
        'name': 'Name',
        'description': 'Description',
        'status': 'Status',
        'active': 'Active',
        'inactive': 'Inactive',
        
        # Navigation
        'dashboard': 'Dashboard',
        'customers': 'Customers',
        'products': 'Products',
        'sales': 'Sales',
        'inventory': 'Inventory',
        'reports': 'Reports',
        'settings': 'Settings',
        'sfa_management': 'SFA Management',
        'field_sales': 'Field Sales',
        'visits': 'Customer Visits',
        'mobile_orders': 'Mobile Orders',
        'activities': 'Sales Activities',
        'targets': 'Sales Targets',
        'expenses': 'Expenses',
        'attendance': 'Attendance',
        
        # Login
        'login_title': 'Login to PenzFlow',
        'login_subtitle': 'Enter your credentials to access the system',
        'invalid_credentials': 'Invalid username or password',
        'login_required': 'Please login to access this page',
        'login_success': 'Login successful!',
        'logout_success': 'Logged out successfully',
        
        # Dashboard
        'overview': 'Overview',
        'total_revenue': 'Total Revenue',
        'total_orders': 'Total Orders',
        'total_customers': 'Total Customers',
        'active_sfa': 'Active SFA',
        'recent_activities': 'Recent Activities',
        'sales_chart': 'Sales Chart',
        'monthly_revenue': 'Monthly Revenue',
        'daily_orders': 'Daily Orders',
        
        # Products
        'product_list': 'Product List',
        'add_product': 'Add Product',
        'product_name': 'Product Name',
        'product_code': 'Product Code',
        'category': 'Category',
        'base_price': 'Base Price',
        'stock_quantity': 'Stock Quantity',
        'minimum_stock': 'Minimum Stock',
        'variants_pricing': 'Variants & Pricing',
        'categories': 'Categories',
        'variant_name': 'Variant Name',
        'variant_price': 'Variant Price',
        'tier_name': 'Tier Name',
        'min_quantity': 'Minimum Quantity',
        'tier_price': 'Tier Price',
        'add_variant': 'Add Variant',
        'add_tier': 'Add Pricing Tier',
        'product_added': 'Product added successfully!',
        'variant_added': 'Variant added successfully!',
        'tier_added': 'Pricing tier added successfully!',
        
        # Customers
        'customer_list': 'Customer List',
        'add_customer': 'Add Customer',
        'customer_name': 'Customer Name',
        'customer_code': 'Customer Code',
        'phone': 'Phone',
        'email': 'Email',
        'address': 'Address',
        'city': 'City',
        'customer_type': 'Customer Type',
        'credit_limit': 'Credit Limit',
        'payment_terms': 'Payment Terms',
        'assigned_sfa': 'Assigned SFA',
        'customer_added': 'Customer added successfully!',
        
        # Sales
        'new_sale': 'New Sale',
        'sale_date': 'Sale Date',
        'customer': 'Customer',
        'product': 'Product',
        'variant': 'Variant',
        'unit_price': 'Unit Price',
        'subtotal': 'Subtotal',
        'discount': 'Discount',
        'tax': 'Tax',
        'grand_total': 'Grand Total',
        'payment_method': 'Payment Method',
        'payment_status': 'Payment Status',
        'paid': 'Paid',
        'partial': 'Partial',
        'unpaid': 'Unpaid',
        'cash': 'Cash',
        'credit': 'Credit',
        'transfer': 'Transfer',
        'add_item': 'Add Item',
        'remove_item': 'Remove Item',
        'sale_created': 'Sale created successfully!',
        
        # Field Sales / SFA
        'check_in': 'Check In',
        'check_out': 'Check Out',
        'visit_customer': 'Visit Customer',
        'visit_purpose': 'Visit Purpose',
        'visit_notes': 'Visit Notes',
        'visit_result': 'Visit Result',
        'follow_up': 'Follow Up',
        'order_taken': 'Order Taken',
        'no_order': 'No Order',
        'create_order': 'Create Order',
        'order_items': 'Order Items',
        'delivery_date': 'Delivery Date',
        'special_instructions': 'Special Instructions',
        'expense_type': 'Expense Type',
        'expense_amount': 'Expense Amount',
        'expense_description': 'Expense Description',
        'receipt': 'Receipt',
        'fuel': 'Fuel',
        'meals': 'Meals',
        'transportation': 'Transportation',
        'other': 'Other',
        
        # Reports
        'sales_report': 'Sales Report',
        'customer_report': 'Customer Report',
        'product_report': 'Product Report',
        'sfa_report': 'SFA Report',
        'date_range': 'Date Range',
        'from_date': 'From Date',
        'to_date': 'To Date',
        'generate_report': 'Generate Report',
        'download_pdf': 'Download PDF',
        'download_excel': 'Download Excel',
        'all': 'All',
        'general': 'General',
    },
    
    'id': {
        # General - Indonesian
        'app_title': 'PenzFlow - Sistem ERP & SFA',
        'language': 'Bahasa',
        'welcome': 'Selamat Datang',
        'login': 'Masuk',
        'logout': 'Keluar',
        'username': 'Nama Pengguna',
        'password': 'Kata Sandi',
        'role': 'Peran',
        'submit': 'Kirim',
        'cancel': 'Batal',
        'save': 'Simpan',
        'delete': 'Hapus',
        'edit': 'Edit',
        'add': 'Tambah',
        'search': 'Cari',
        'filter': 'Filter',
        'export': 'Ekspor',
        'import': 'Impor',
        'refresh': 'Refresh',
        'back': 'Kembali',
        'next': 'Berikutnya',
        'previous': 'Sebelumnya',
        'close': 'Tutup',
        'confirm': 'Konfirmasi',
        'success': 'Berhasil',
        'error': 'Error',
        'warning': 'Peringatan',
        'info': 'Informasi',
        'loading': 'Memuat...',
        'no_data': 'Tidak ada data',
        'total': 'Total',
        'amount': 'Jumlah',
        'quantity': 'Kuantitas',
        'price': 'Harga',
        'date': 'Tanggal',
        'time': 'Waktu',
        'name': 'Nama',
        'description': 'Deskripsi',
        'status': 'Status',
        'active': 'Aktif',
        'inactive': 'Tidak Aktif',
        
        # Navigation - Indonesian
        'dashboard': 'Dashboard',
        'customers': 'Pelanggan',
        'products': 'Produk',
        'sales': 'Penjualan',
        'inventory': 'Inventori',
        'reports': 'Laporan',
        'settings': 'Pengaturan',
        'sfa_management': 'Manajemen SFA',
        'field_sales': 'Sales Lapangan',
        'visits': 'Kunjungan Pelanggan',
        'mobile_orders': 'Pesanan Mobile',
        'activities': 'Aktivitas Penjualan',
        'targets': 'Target Penjualan',
        'expenses': 'Pengeluaran',
        'attendance': 'Absensi',
        
        # Login - Indonesian
        'login_title': 'Masuk ke PenzFlow',
        'login_subtitle': 'Masukkan kredensial Anda untuk mengakses sistem',
        'invalid_credentials': 'Nama pengguna atau kata sandi tidak valid',
        'login_required': 'Silakan login untuk mengakses halaman ini',
        'login_success': 'Login berhasil!',
        'logout_success': 'Logout berhasil',
        
        # Dashboard - Indonesian
        'overview': 'Ringkasan',
        'total_revenue': 'Total Pendapatan',
        'total_orders': 'Total Pesanan',
        'total_customers': 'Total Pelanggan',
        'active_sfa': 'SFA Aktif',
        'recent_activities': 'Aktivitas Terbaru',
        'sales_chart': 'Grafik Penjualan',
        'monthly_revenue': 'Pendapatan Bulanan',
        'daily_orders': 'Pesanan Harian',
        
        # Products - Indonesian
        'product_list': 'Daftar Produk',
        'add_product': 'Tambah Produk',
        'product_name': 'Nama Produk',
        'product_code': 'Kode Produk',
        'category': 'Kategori',
        'base_price': 'Harga Dasar',
        'stock_quantity': 'Jumlah Stok',
        'minimum_stock': 'Stok Minimum',
        'variants_pricing': 'Varian & Harga',
        'categories': 'Kategori',
        'variant_name': 'Nama Varian',
        'variant_price': 'Harga Varian',
        'tier_name': 'Nama Tingkatan',
        'min_quantity': 'Kuantitas Minimum',
        'tier_price': 'Harga Tingkatan',
        'add_variant': 'Tambah Varian',
        'add_tier': 'Tambah Tingkat Harga',
        'product_added': 'Produk berhasil ditambahkan!',
        'variant_added': 'Varian berhasil ditambahkan!',
        'tier_added': 'Tingkat harga berhasil ditambahkan!',
        
        # Customers - Indonesian
        'customer_list': 'Daftar Pelanggan',
        'add_customer': 'Tambah Pelanggan',
        'customer_name': 'Nama Pelanggan',
        'customer_code': 'Kode Pelanggan',
        'phone': 'Telepon',
        'email': 'Email',
        'address': 'Alamat',
        'city': 'Kota',
        'customer_type': 'Tipe Pelanggan',
        'credit_limit': 'Limit Kredit',
        'payment_terms': 'Syarat Pembayaran',
        'assigned_sfa': 'SFA yang Ditugaskan',
        'customer_added': 'Pelanggan berhasil ditambahkan!',
        
        # Sales - Indonesian
        'new_sale': 'Penjualan Baru',
        'sale_date': 'Tanggal Penjualan',
        'customer': 'Pelanggan',
        'product': 'Produk',
        'variant': 'Varian',
        'unit_price': 'Harga Satuan',
        'subtotal': 'Subtotal',
        'discount': 'Diskon',
        'tax': 'Pajak',
        'grand_total': 'Total Keseluruhan',
        'payment_method': 'Metode Pembayaran',
        'payment_status': 'Status Pembayaran',
        'paid': 'Lunas',
        'partial': 'Sebagian',
        'unpaid': 'Belum Bayar',
        'cash': 'Tunai',
        'credit': 'Kredit',
        'transfer': 'Transfer',
        'add_item': 'Tambah Item',
        'remove_item': 'Hapus Item',
        'sale_created': 'Penjualan berhasil dibuat!',
        
        # Field Sales / SFA - Indonesian
        'check_in': 'Check In',
        'check_out': 'Check Out',
        'visit_customer': 'Kunjungi Pelanggan',
        'visit_purpose': 'Tujuan Kunjungan',
        'visit_notes': 'Catatan Kunjungan',
        'visit_result': 'Hasil Kunjungan',
        'follow_up': 'Tindak Lanjut',
        'order_taken': 'Pesanan Diambil',
        'no_order': 'Tidak Ada Pesanan',
        'create_order': 'Buat Pesanan',
        'order_items': 'Item Pesanan',
        'delivery_date': 'Tanggal Pengiriman',
        'special_instructions': 'Instruksi Khusus',
        'expense_type': 'Jenis Pengeluaran',
        'expense_amount': 'Jumlah Pengeluaran',
        'expense_description': 'Deskripsi Pengeluaran',
        'receipt': 'Kwitansi',
        'fuel': 'Bahan Bakar',
        'meals': 'Makan',
        'transportation': 'Transportasi',
        'other': 'Lainnya',
        
        # Reports - Indonesian
        'sales_report': 'Laporan Penjualan',
        'customer_report': 'Laporan Pelanggan',
        'product_report': 'Laporan Produk',
        'sfa_report': 'Laporan SFA',
        'date_range': 'Rentang Tanggal',
        'from_date': 'Dari Tanggal',
        'to_date': 'Sampai Tanggal',
        'generate_report': 'Buat Laporan',
        'download_pdf': 'Unduh PDF',
        'download_excel': 'Unduh Excel',
        'all': 'Semua',
        'general': 'Umum',
    }
}

def get_text(key, lang='en'):
    """
    Get translated text for a given key and language
    
    Args:
        key (str): Translation key
        lang (str): Language code ('en' or 'id')
    
    Returns:
        str: Translated text or key if translation not found
    """
    return TRANSLATIONS.get(lang, {}).get(key, key)

def init_language():
    """Initialize language in session state if not already set"""
    if 'language' not in st.session_state:
        st.session_state.language = 'id'  # Default to Indonesian

def get_current_language():
    """Get current language from session state"""
    return st.session_state.get('language', 'id')

def set_language(lang):
    """Set language in session state"""
    st.session_state.language = lang

def t(key):
    """
    Shorthand function to get translation for current language
    
    Args:
        key (str): Translation key
    
    Returns:
        str: Translated text
    """
    current_lang = get_current_language()
    return get_text(key, current_lang)
