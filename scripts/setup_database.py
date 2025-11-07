"""
Setup MySQL database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.mysql_setup import setup_database

if __name__ == "__main__":
    setup_database()
