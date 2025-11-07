"""
Extract data from staging tables
"""
from utils.database_connector import MySQLConnector
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Extractor:
    """Extract data from staging tables"""
    
    def __init__(self):
        self.mysql = MySQLConnector()
        self.mysql.connect()
    
    def extract_orders(self, last_run_time=None, limit=1000):
        """Extract orders from staging table"""
        try:
            if last_run_time:
                query = """
                SELECT * FROM staging_orders 
                WHERE created_at > %s 
                ORDER BY created_at ASC
                LIMIT %s
                """
                params = (last_run_time, limit)
            else:
                query = """
                SELECT * FROM staging_orders 
                ORDER BY created_at ASC
                LIMIT %s
                """
                params = (limit,)
            
            results = self.mysql.execute_query(query, params)
            logger.info(f"Extracted {len(results)} orders")
            return results
        except Exception as e:
            logger.error(f"Failed to extract orders: {e}")
            return []
    
    def extract_clicks(self, last_run_time=None, limit=1000):
        """Extract clicks from staging table"""
        try:
            if last_run_time:
                query = """
                SELECT * FROM staging_clicks 
                WHERE created_at > %s 
                ORDER BY created_at ASC
                LIMIT %s
                """
                params = (last_run_time, limit)
            else:
                query = """
                SELECT * FROM staging_clicks 
                ORDER BY created_at ASC
                LIMIT %s
                """
                params = (limit,)
            
            results = self.mysql.execute_query(query, params)
            logger.info(f"Extracted {len(results)} clicks")
            return results
        except Exception as e:
            logger.error(f"Failed to extract clicks: {e}")
            return []
    
    def extract_customer_events(self, last_run_time=None, limit=1000):
        """Extract customer events from staging table"""
        try:
            if last_run_time:
                query = """
                SELECT * FROM staging_customer_events 
                WHERE created_at > %s 
                ORDER BY created_at ASC
                LIMIT %s
                """
                params = (last_run_time, limit)
            else:
                query = """
                SELECT * FROM staging_customer_events 
                ORDER BY created_at ASC
                LIMIT %s
                """
                params = (limit,)
            
            results = self.mysql.execute_query(query, params)
            logger.info(f"Extracted {len(results)} customer events")
            return results
        except Exception as e:
            logger.error(f"Failed to extract customer events: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        self.mysql.close()


