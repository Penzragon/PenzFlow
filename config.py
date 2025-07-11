import os

class Config:
    # Application settings
    APP_NAME = "PenzFlow - ERP & SFA System"
    VERSION = "1.0.0"
    
    # Database configuration
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'penzflow.db')
    
    # Security settings
    SECRET_KEY = 'penzflow_secret_key_change_in_production'
    SESSION_TIMEOUT = 3600  # 1 hour in seconds
    
    # Business settings
    DEFAULT_CURRENCY = 'USD'
    DEFAULT_TAX_RATE = 0.08  # 8%
    DEFAULT_TIMEZONE = 'UTC'
    
    # Pagination settings
    ITEMS_PER_PAGE = 50
    
    # Email settings (for future use)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    
    # File upload settings
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx'}
    
    # Report settings
    REPORTS_DIR = os.path.join(os.path.dirname(__file__), 'reports')
    BACKUP_DIR = os.path.join(os.path.dirname(__file__), 'backups')
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    
class TestingConfig(Config):
    TESTING = True
    DATABASE_PATH = ':memory:'

# Default configuration
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}