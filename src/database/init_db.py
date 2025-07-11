import sqlite3
import os
from datetime import datetime

def get_db_path():
    """Get the database file path"""
    db_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    return os.path.join(db_dir, 'penzflow.db')

def init_database():
    """Initialize the database with required tables"""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            company TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            price DECIMAL(10,2),
            cost DECIMAL(10,2),
            stock_quantity INTEGER DEFAULT 0,
            min_stock_level INTEGER DEFAULT 0,
            max_stock_level INTEGER DEFAULT 1000,
            supplier TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Sales Orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            customer_id INTEGER,
            order_date DATE,
            total_amount DECIMAL(10,2),
            status TEXT DEFAULT 'pending',
            payment_method TEXT,
            sales_rep TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    # Order Items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price DECIMAL(10,2),
            total_price DECIMAL(10,2),
            FOREIGN KEY (order_id) REFERENCES sales_orders (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Inventory Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            transaction_type TEXT, -- 'in', 'out', 'adjustment'
            quantity INTEGER,
            reference_type TEXT, -- 'purchase', 'sale', 'adjustment'
            reference_id INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # SFA - Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            check_in_time TIMESTAMP,
            check_out_time TIMESTAMP,
            location TEXT,
            latitude REAL,
            longitude REAL,
            notes TEXT,
            status TEXT DEFAULT 'present', -- 'present', 'absent', 'late'
            date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # SFA - Customer Visits table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            customer_id INTEGER,
            visit_date TIMESTAMP,
            visit_type TEXT, -- 'sales_call', 'delivery', 'follow_up', 'complaint'
            purpose TEXT,
            notes TEXT,
            result TEXT,
            follow_up_required BOOLEAN DEFAULT 0,
            follow_up_date DATE,
            location TEXT,
            latitude REAL,
            longitude REAL,
            duration INTEGER, -- in minutes
            status TEXT DEFAULT 'planned', -- 'planned', 'in_progress', 'completed', 'cancelled'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    # SFA - Sales Targets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            target_period TEXT, -- 'monthly', 'quarterly', 'yearly'
            start_date DATE,
            end_date DATE,
            target_amount DECIMAL(15,2),
            achieved_amount DECIMAL(15,2) DEFAULT 0,
            target_visits INTEGER,
            achieved_visits INTEGER DEFAULT 0,
            target_customers INTEGER,
            achieved_customers INTEGER DEFAULT 0,
            status TEXT DEFAULT 'active', -- 'active', 'completed', 'paused'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # SFA - Sales Routes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            route_name TEXT,
            day_of_week INTEGER, -- 0=Monday, 6=Sunday
            customers TEXT, -- JSON array of customer IDs
            estimated_duration INTEGER, -- in minutes
            status TEXT DEFAULT 'active', -- 'active', 'inactive'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # SFA - Sales Activities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            customer_id INTEGER,
            activity_type TEXT, -- 'call', 'email', 'meeting', 'demo', 'proposal'
            activity_date TIMESTAMP,
            subject TEXT,
            description TEXT,
            result TEXT,
            next_action TEXT,
            next_action_date DATE,
            priority TEXT DEFAULT 'medium', -- 'low', 'medium', 'high'
            status TEXT DEFAULT 'pending', -- 'pending', 'completed', 'cancelled'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    # SFA - Mobile Orders table (for field sales)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mobile_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            customer_id INTEGER,
            visit_id INTEGER,
            order_number TEXT UNIQUE,
            order_date TIMESTAMP,
            total_amount DECIMAL(15,2),
            status TEXT DEFAULT 'draft', -- 'draft', 'submitted', 'approved', 'rejected'
            payment_terms TEXT,
            delivery_date DATE,
            special_instructions TEXT,
            discount_percentage DECIMAL(5,2) DEFAULT 0,
            tax_percentage DECIMAL(5,2) DEFAULT 11,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (visit_id) REFERENCES customer_visits (id)
        )
    ''')
    
    # SFA - Mobile Order Items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mobile_order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mobile_order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price DECIMAL(15,2),
            discount_percentage DECIMAL(5,2) DEFAULT 0,
            total_price DECIMAL(15,2),
            notes TEXT,
            FOREIGN KEY (mobile_order_id) REFERENCES mobile_orders (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # SFA - Expense Claims table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expense_claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            claim_date DATE,
            expense_type TEXT, -- 'travel', 'meal', 'accommodation', 'fuel', 'other'
            amount DECIMAL(15,2),
            description TEXT,
            receipt_path TEXT,
            status TEXT DEFAULT 'pending', -- 'pending', 'approved', 'rejected', 'paid'
            approved_by INTEGER,
            approved_date TIMESTAMP,
            remarks TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (approved_by) REFERENCES users (id)
        )
    ''')
    
    # SFA - GPS Tracking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gps_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            latitude REAL,
            longitude REAL,
            accuracy REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            activity TEXT, -- 'traveling', 'at_customer', 'break', 'office'
            battery_level INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Insert default admin user if not exists
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO users (username, password, email, role)
            VALUES ('admin', 'admin123', 'admin@penzflow.com', 'administrator')
        ''')
    
    # Insert demo user if not exists
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'demo'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO users (username, password, email, role)
            VALUES ('demo', 'demo', 'demo@penzflow.com', 'user')
        ''')
    
    # Insert salesman users if not exist
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'salesman1'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO users (username, password, email, role)
            VALUES ('salesman1', 'sales123', 'budi.santoso@penzflow.com', 'salesman')
        ''')
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'salesman2'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO users (username, password, email, role)
            VALUES ('salesman2', 'sales123', 'sari.wulandari@penzflow.com', 'salesman')
        ''')
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'manager1'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO users (username, password, email, role)
            VALUES ('manager1', 'manager123', 'ahmad.manager@penzflow.com', 'sales_manager')
        ''')
    
    # Insert sample data if tables are empty
    insert_sample_data(cursor)
    
    conn.commit()
    conn.close()

def insert_sample_data(cursor):
    """Insert sample data for demonstration"""
    
    # Check if customers table is empty
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        customers = [
            ('Budi Santoso', 'budi.santoso@email.com', '+62812-3456-7890', 'PT Teknologi Maju', 'Jl. Sudirman No. 123, Jakarta Pusat'),
            ('Sari Dewi', 'sari.dewi@email.com', '+62813-4567-8901', 'CV Bisnis Mandiri', 'Jl. Thamrin No. 456, Jakarta Selatan'),
            ('Ahmad Rahman', 'ahmad.rahman@email.com', '+62814-5678-9012', 'PT Layanan Prima', 'Jl. Gatot Subroto No. 789, Jakarta Timur'),
            ('Indira Putri', 'indira.putri@email.com', '+62815-6789-0123', 'PT Solusi Digital', 'Jl. Kuningan No. 321, Jakarta Selatan'),
            ('Rizki Pratama', 'rizki.pratama@email.com', '+62816-7890-1234', 'PT Usaha Bersama', 'Jl. Rasuna Said No. 654, Jakarta Selatan')
        ]
        
        cursor.executemany('''
            INSERT INTO customers (name, email, phone, company, address)
            VALUES (?, ?, ?, ?, ?)
        ''', customers)
    
    # Check if products table is empty
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        products = [
            ('PRD001', 'Laptop Pro', 'High-performance laptop for professionals', 'Electronics', 14999000, 11250000, 25, 10, 100, 'TechSupplier Inc'),  # ~$999 -> Rp 14,999,000
            ('PRD002', 'Wireless Mouse', 'Ergonomic wireless mouse with long battery life', 'Accessories', 449000, 225000, 150, 50, 300, 'AccessoryHub'),  # ~$30 -> Rp 449,000
            ('PRD003', 'USB Cable', 'High-speed USB-C cable 6ft', 'Cables', 149000, 60000, 200, 100, 500, 'CableCorp'),  # ~$10 -> Rp 149,000
            ('PRD004', 'Monitor Stand', 'Adjustable monitor stand for better ergonomics', 'Furniture', 749000, 375000, 45, 20, 100, 'OfficeSupply Ltd'),  # ~$50 -> Rp 749,000
            ('PRD005', 'Keyboard', 'Mechanical keyboard with RGB backlighting', 'Input Devices', 1199000, 675000, 80, 30, 150, 'KeyboardMaker')  # ~$80 -> Rp 1,199,000
        ]
        
        cursor.executemany('''
            INSERT INTO products (sku, name, description, category, price, cost, stock_quantity, min_stock_level, max_stock_level, supplier)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', products)
    
    # Check if sales_orders table is empty
    cursor.execute("SELECT COUNT(*) FROM sales_orders")
    if cursor.fetchone()[0] == 0:
        orders = [
            ('ORD001', 1, '2024-01-15', 19500000, 'completed', 'Credit Card', 'John Sales', 'First order'),  # ~$1300 -> Rp 19,500,000
            ('ORD002', 2, '2024-01-16', 1350000, 'pending', 'Cash', 'Jane Sales', 'Rush order'),  # ~$90 -> Rp 1,350,000
            ('ORD003', 3, '2024-01-17', 37500000, 'shipped', 'Bank Transfer', 'Bob Sales', 'Bulk order'),  # ~$2500 -> Rp 37,500,000
            ('ORD004', 4, '2024-01-18', 9000000, 'processing', 'Credit Card', 'Alice Sales', 'Regular order'),  # ~$600 -> Rp 9,000,000
            ('ORD005', 5, '2024-01-19', 3000000, 'completed', 'Cash', 'Charlie Sales', 'Quick sale')  # ~$200 -> Rp 3,000,000
        ]
        
        cursor.executemany('''
            INSERT INTO sales_orders (order_number, customer_id, order_date, total_amount, status, payment_method, sales_rep, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', orders)
    
    # Insert sample SFA data
    insert_sfa_sample_data(cursor)

def insert_sfa_sample_data(cursor):
    """Insert sample SFA data for demonstration"""
    from datetime import datetime, timedelta
    
    # Get salesman user IDs
    cursor.execute("SELECT id FROM users WHERE role = 'salesman'")
    salesman_ids = [row[0] for row in cursor.fetchall()]
    
    if not salesman_ids:
        return
    
    # Sample attendance data
    cursor.execute("SELECT COUNT(*) FROM attendance")
    if cursor.fetchone()[0] == 0:
        today = datetime.now().date()
        attendance_data = []
        
        for days_back in range(7):  # Last 7 days
            date = today - timedelta(days=days_back)
            for salesman_id in salesman_ids:
                check_in = datetime.combine(date, datetime.min.time().replace(hour=8, minute=30))
                check_out = datetime.combine(date, datetime.min.time().replace(hour=17, minute=0))
                attendance_data.append((
                    salesman_id, check_in, check_out, 'Jakarta Office', -6.2088, 106.8456, 
                    'Regular attendance', 'present', date
                ))
        
        cursor.executemany('''
            INSERT INTO attendance (user_id, check_in_time, check_out_time, location, latitude, longitude, notes, status, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', attendance_data)
    
    # Sample customer visits
    cursor.execute("SELECT COUNT(*) FROM customer_visits")
    if cursor.fetchone()[0] == 0:
        visits_data = [
            (salesman_ids[0], 1, datetime.now() - timedelta(hours=2), 'sales_call', 'Product demonstration', 
             'Showed new product line, customer interested', 'Customer will consider, follow up next week', 1, 
             (datetime.now() + timedelta(days=7)).date(), 'PT. Teknologi Maju', -6.2297, 106.8269, 120, 'completed'),
            (salesman_ids[0], 2, datetime.now() - timedelta(hours=4), 'follow_up', 'Follow up on previous order', 
             'Discussed delivery timeline', 'Order confirmed, delivery scheduled', 0, None, 
             'CV. Bisnis Sukses', -6.1944, 106.8229, 90, 'completed'),
            (salesman_ids[1] if len(salesman_ids) > 1 else salesman_ids[0], 3, datetime.now() - timedelta(hours=1), 
             'delivery', 'Product delivery and setup', 'Delivered products, provided training', 
             'Customer satisfied, potential for future orders', 1, (datetime.now() + timedelta(days=14)).date(), 
             'UD. Perdagangan Jaya', -6.2615, 106.7832, 150, 'completed')
        ]
        
        cursor.executemany('''
            INSERT INTO customer_visits (user_id, customer_id, visit_date, visit_type, purpose, notes, result, 
            follow_up_required, follow_up_date, location, latitude, longitude, duration, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', visits_data)
    
    # Sample sales targets
    cursor.execute("SELECT COUNT(*) FROM sales_targets")
    if cursor.fetchone()[0] == 0:
        from datetime import date
        current_month_start = date.today().replace(day=1)
        
        targets_data = []
        for salesman_id in salesman_ids:
            targets_data.append((
                salesman_id, 'monthly', current_month_start, 
                date(current_month_start.year, current_month_start.month + 1, 1) - timedelta(days=1),
                50000000,  # Rp 50 million target
                35000000,  # Rp 35 million achieved
                20, 15,    # 20 visits target, 15 achieved
                10, 8      # 10 customers target, 8 achieved
            ))
        
        cursor.executemany('''
            INSERT INTO sales_targets (user_id, target_period, start_date, end_date, target_amount, achieved_amount, 
            target_visits, achieved_visits, target_customers, achieved_customers)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', targets_data)
    
    # Sample sales activities
    cursor.execute("SELECT COUNT(*) FROM sales_activities")
    if cursor.fetchone()[0] == 0:
        activities_data = [
            (salesman_ids[0], 1, 'call', datetime.now() - timedelta(hours=3), 'Follow up call', 
             'Called to check on product satisfaction', 'Customer happy with purchase', 
             'Schedule maintenance visit', (datetime.now() + timedelta(days=30)).date(), 'medium', 'completed'),
            (salesman_ids[0], 2, 'email', datetime.now() - timedelta(hours=6), 'Product catalog', 
             'Sent new product catalog via email', 'Email delivered', 'Wait for customer response', 
             (datetime.now() + timedelta(days=3)).date(), 'low', 'completed'),
            (salesman_ids[1] if len(salesman_ids) > 1 else salesman_ids[0], 3, 'meeting', 
             datetime.now() + timedelta(hours=2), 'Contract negotiation', 
             'Discuss terms for bulk order', '', 'Prepare contract proposal', 
             (datetime.now() + timedelta(days=1)).date(), 'high', 'pending')
        ]
        
        cursor.executemany('''
            INSERT INTO sales_activities (user_id, customer_id, activity_type, activity_date, subject, description, 
            result, next_action, next_action_date, priority, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', activities_data)

def get_connection():
    """Get database connection"""
    db_path = get_db_path()
    return sqlite3.connect(db_path)
