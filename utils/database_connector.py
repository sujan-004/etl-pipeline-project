"""
Database connector utilities for MySQL
"""
import pymysql
from config.config import MYSQL_CONFIG
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MySQLConnector:
    """MySQL database connector"""
    
    def __init__(self):
        self.config = MYSQL_CONFIG
        self.connection = None
    
    def connect(self):
        """Establish MySQL connection"""
        try:
            self.connection = pymysql.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
                charset=self.config['charset'],
                cursorclass=pymysql.cursors.DictCursor
            )
            logger.info("MySQL connection established")
            return self.connection
        except Exception as e:
            logger.error(f"MySQL connection failed: {e}")
            raise
    
    def execute_query(self, query, params=None):
        """Execute a query"""
        if not self.connection:
            self.connect()
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            self.connection.rollback()
            raise
    
    def execute_many(self, query, params_list):
        """Execute multiple queries"""
        if not self.connection:
            self.connect()
        
        try:
            with self.connection.cursor() as cursor:
                cursor.executemany(query, params_list)
                self.connection.commit()
                return cursor.rowcount
        except Exception as e:
            logger.error(f"Batch execution failed: {e}")
            self.connection.rollback()
            raise
    
    def close(self):
        """Close MySQL connection"""
        if self.connection:
            self.connection.close()
            logger.info("MySQL connection closed")

