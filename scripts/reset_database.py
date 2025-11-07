"""
Reset and recreate database (use with caution - deletes all data!)
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database_connector import MySQLConnector
from config.config import MYSQL_CONFIG
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def reset_database():
    """Drop and recreate database"""
    try:
        logger.warning("=" * 70)
        logger.warning("WARNING: This will DELETE ALL DATA in the database!")
        logger.warning("=" * 70)
        
        response = input("\nAre you sure you want to reset the database? (yes/no): ")
        if response.lower() != 'yes':
            logger.info("Database reset cancelled.")
            return
        
        mysql = MySQLConnector()
        mysql.connect()
        
        # Drop database
        logger.info(f"Dropping database '{MYSQL_CONFIG['database']}'...")
        mysql.execute_query(f"DROP DATABASE IF EXISTS {MYSQL_CONFIG['database']}")
        logger.info("✅ Database dropped")
        
        # Recreate database
        logger.info(f"Creating database '{MYSQL_CONFIG['database']}'...")
        mysql.execute_query(f"CREATE DATABASE {MYSQL_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        logger.info("✅ Database created")
        
        mysql.close()
        logger.info("")
        logger.info("Database reset complete! Now run:")
        logger.info("  python scripts/setup_database.py")
        
    except Exception as e:
        logger.error(f"Database reset failed: {e}")
        raise


if __name__ == "__main__":
    reset_database()

