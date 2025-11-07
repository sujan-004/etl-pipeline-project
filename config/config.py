"""
Configuration file for the ETL Pipeline Project
"""
import os
from dotenv import load_dotenv

load_dotenv()

# MySQL Configuration
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', 'ecommerce_db'),
    'charset': 'utf8mb4'
}


# Flask Generator Configuration
FLASK_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True
}

# ETL Configuration
ETL_CONFIG = {
    'batch_size': 1000,
    'sleep_interval': 5  # seconds between ETL runs
}

