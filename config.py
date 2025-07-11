class Config:
    SECRET_KEY = 'your_secret_key_here'
    DEBUG = True
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False