"""
Setup script to initialize MySQL database
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.mysql_setup import setup_database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Run database setup"""
    logger.info("=" * 50)
    logger.info("Setting up MySQL database...")
    logger.info("=" * 50)
    
    try:
        setup_database()
        logger.info("\n" + "=" * 50)
        logger.info("Database setup completed successfully!")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        raise


if __name__ == "__main__":
    main()

