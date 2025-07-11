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
            ('John Doe', 'john@email.com', '+1234567890', 'Tech Corp', '123 Main St, City'),
            ('Jane Smith', 'jane@email.com', '+1234567891', 'Business Inc', '456 Oak Ave, Town'),
            ('Bob Johnson', 'bob@email.com', '+1234567892', 'Services LLC', '789 Pine Rd, Village'),
            ('Alice Brown', 'alice@email.com', '+1234567893', 'Solutions Ltd', '321 Elm St, County'),
            ('Charlie Wilson', 'charlie@email.com', '+1234567894', 'Enterprises Co', '654 Maple Dr, District')
        ]
        
        cursor.executemany('''
            INSERT INTO customers (name, email, phone, company, address)
            VALUES (?, ?, ?, ?, ?)
        ''', customers)
    
    # Check if products table is empty
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        products = [
            ('PRD001', 'Laptop Pro', 'High-performance laptop for professionals', 'Electronics', 999.99, 750.00, 25, 10, 100, 'TechSupplier Inc'),
            ('PRD002', 'Wireless Mouse', 'Ergonomic wireless mouse with long battery life', 'Accessories', 29.99, 15.00, 150, 50, 300, 'AccessoryHub'),
            ('PRD003', 'USB Cable', 'High-speed USB-C cable 6ft', 'Cables', 9.99, 4.00, 200, 100, 500, 'CableCorp'),
            ('PRD004', 'Monitor Stand', 'Adjustable monitor stand for better ergonomics', 'Furniture', 49.99, 25.00, 45, 20, 100, 'OfficeSupply Ltd'),
            ('PRD005', 'Keyboard', 'Mechanical keyboard with RGB backlighting', 'Input Devices', 79.99, 45.00, 80, 30, 150, 'KeyboardMaker')
        ]
        
        cursor.executemany('''
            INSERT INTO products (sku, name, description, category, price, cost, stock_quantity, min_stock_level, max_stock_level, supplier)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', products)
    
    # Check if sales_orders table is empty
    cursor.execute("SELECT COUNT(*) FROM sales_orders")
    if cursor.fetchone()[0] == 0:
        orders = [
            ('ORD001', 1, '2024-01-15', 1299.99, 'completed', 'Credit Card', 'John Sales', 'First order'),
            ('ORD002', 2, '2024-01-16', 89.99, 'pending', 'Cash', 'Jane Sales', 'Rush order'),
            ('ORD003', 3, '2024-01-17', 2499.99, 'shipped', 'Bank Transfer', 'Bob Sales', 'Bulk order'),
            ('ORD004', 4, '2024-01-18', 599.99, 'processing', 'Credit Card', 'Alice Sales', 'Regular order'),
            ('ORD005', 5, '2024-01-19', 199.99, 'completed', 'Cash', 'Charlie Sales', 'Quick sale')
        ]
        
        cursor.executemany('''
            INSERT INTO sales_orders (order_number, customer_id, order_date, total_amount, status, payment_method, sales_rep, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', orders)

def get_connection():
    """Get database connection"""
    db_path = get_db_path()
    return sqlite3.connect(db_path)
