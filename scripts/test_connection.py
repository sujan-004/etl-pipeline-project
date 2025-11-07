"""
Test MySQL database connection
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database_connector import MySQLConnector
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_mysql():
    """Test MySQL connection"""
    try:
        logger.info("Testing MySQL connection...")
        mysql = MySQLConnector()
        mysql.connect()
        
        # Test query
        result = mysql.execute_query("SELECT DATABASE() as db, VERSION() as version")
        if result:
            logger.info(f"✅ MySQL connected successfully!")
            logger.info(f"   Database: {result[0]['db']}")
            logger.info(f"   Version: {result[0]['version']}")
        
        # Check tables
        tables = mysql.execute_query("SHOW TABLES")
        if tables:
            logger.info(f"   Tables found: {len(tables)}")
            for table in tables[:10]:  # Show first 10
                logger.info(f"   - {list(table.values())[0]}")
        
        mysql.close()
        return True
    except Exception as e:
        logger.error(f"❌ MySQL connection failed: {e}")
        return False


def main():
    """Run connection test"""
    logger.info("=" * 50)
    logger.info("MySQL Database Connection Test")
    logger.info("=" * 50)
    
    mysql_ok = test_mysql()
    
    logger.info("\n" + "=" * 50)
    if mysql_ok:
        logger.info("✅ MySQL: Ready")
    else:
        logger.info("❌ MySQL: Not Ready - Fix connection before proceeding")
        logger.info("   Check your MySQL credentials in config/config.py")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()

