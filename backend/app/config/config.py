import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', '7d8f9e0a1b2c3d4e5f6g7h8i9j0k1l2m')
    
    # Database Configuration
    # Fix: Process backslash escaping from .env
    _raw_server = os.getenv('DB_SERVER', r'.\SQLEXPRESS')
    DB_SERVER = _raw_server.replace('\\\\', '\\') if '\\\\' in _raw_server else _raw_server
    DB_NAME = os.getenv('DB_NAME', 'StudentAssistantDB')
    DB_USERNAME = os.getenv('DB_USERNAME', 'sa')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '0946483539')
    DB_DRIVER = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '9a8b7c6d5e4f3g2h1i0j9k8l7m6n5o4p')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

# Export config dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}