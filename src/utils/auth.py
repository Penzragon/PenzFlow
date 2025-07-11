import streamlit as st
import sqlite3
from datetime import datetime
from database.init_db import get_connection

def check_login():
    """Check if user is logged in"""
    return st.session_state.get('logged_in', False)

def login_user(username, password):
    """Authenticate user login"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, role FROM users 
            WHERE username = ? AND password = ?
        ''', (username, password))
        
        user = cursor.fetchone()
        
        if user:
            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP 
                WHERE username = ?
            ''', (username,))
            conn.commit()
            
            # Set session state
            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.session_state.username = user[1]
            st.session_state.user_role = user[2]
            
            conn.close()
            return True
        
        conn.close()
        return False
        
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return False

def logout_user():
    """Log out the current user"""
    keys_to_remove = ['logged_in', 'user_id', 'username', 'user_role']
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]

def get_current_user():
    """Get current logged in user information"""
    if check_login():
        return {
            'id': st.session_state.get('user_id'),
            'username': st.session_state.get('username'),
            'role': st.session_state.get('user_role')
        }
    return None

def require_login():
    """Decorator to require login for certain functions"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not check_login():
                st.error("Please log in to access this feature.")
                st.stop()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def has_permission(required_role):
    """Check if current user has required permission level"""
    if not check_login():
        return False
    
    user_role = st.session_state.get('user_role', '')
    
    role_hierarchy = {
        'administrator': 5,
        'sales_manager': 4,
        'manager': 3,
        'salesman': 2,
        'sales_rep': 2,
        'user': 1,
        'viewer': 0
    }
    
    user_level = role_hierarchy.get(user_role, 0)
    required_level = role_hierarchy.get(required_role, 0)
    
    return user_level >= required_level
