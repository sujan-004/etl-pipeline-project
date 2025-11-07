"""
Reset database (drops and recreates - deletes all data!)
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database_connector import MySQLConnector
from config.config import MYSQL_CONFIG

def reset_database():
    """Drop and recreate database"""
    print("WARNING: This will DELETE ALL DATA!")
    response = input("Are you sure? (yes/no): ")
    if response.lower() != 'yes':
        print("Cancelled.")
        return
    
    mysql = MySQLConnector()
    mysql.connect()
    mysql.execute_query(f"DROP DATABASE IF EXISTS {MYSQL_CONFIG['database']}")
    mysql.execute_query(f"CREATE DATABASE {MYSQL_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    mysql.close()
    print("Database reset complete. Run: python scripts/setup_database.py")

if __name__ == "__main__":
    reset_database()
