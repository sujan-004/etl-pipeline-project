"""
Test MySQL database connection
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database_connector import MySQLConnector

def test_mysql():
    """Test MySQL connection"""
    try:
        print("Testing MySQL connection...")
        mysql = MySQLConnector()
        mysql.connect()
        
        result = mysql.execute_query("SELECT DATABASE() as db, VERSION() as version")
        if result:
            print(f"Connected: {result[0]['db']} (MySQL {result[0]['version']})")
        
        tables = mysql.execute_query("SHOW TABLES")
        if tables:
            print(f"Tables found: {len(tables)}")
        
        mysql.close()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_mysql()
