"""
Test MySQL connection with different passwords
Helps identify the correct MySQL root password
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
from config.config import MYSQL_CONFIG
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_connection(host, port, user, password, database=None):
    """Test MySQL connection with given credentials"""
    try:
        if database:
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                charset='utf8mb4'
            )
        else:
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                charset='utf8mb4'
            )
        connection.close()
        return True
    except pymysql.err.OperationalError as e:
        if "Access denied" in str(e):
            return False, "Access denied"
        else:
            return False, str(e)
    except Exception as e:
        return False, str(e)


def main():
    """Test MySQL connection"""
    logger.info("=" * 70)
    logger.info("MySQL Password Test Tool")
    logger.info("=" * 70)
    logger.info("")
    logger.info("Current Configuration:")
    logger.info(f"  Host: {MYSQL_CONFIG['host']}")
    logger.info(f"  Port: {MYSQL_CONFIG['port']}")
    logger.info(f"  User: {MYSQL_CONFIG['user']}")
    logger.info(f"  Password: {'*' * len(MYSQL_CONFIG['password']) if MYSQL_CONFIG['password'] else '(empty)'}")
    logger.info(f"  Database: {MYSQL_CONFIG['database']}")
    logger.info("")
    
    # Test current password
    logger.info("Testing current password...")
    result = test_connection(
        MYSQL_CONFIG['host'],
        MYSQL_CONFIG['port'],
        MYSQL_CONFIG['user'],
        MYSQL_CONFIG['password']
    )
    
    if result is True:
        logger.info("✅ SUCCESS! Current password is correct!")
        logger.info("")
        logger.info("You can proceed with database setup:")
        logger.info("  python scripts/setup_database.py")
        return
    
    logger.warning("❌ Current password is INCORRECT")
    logger.info("")
    logger.info("=" * 70)
    logger.info("SOLUTIONS")
    logger.info("=" * 70)
    logger.info("")
    
    logger.info("Option 1: Update Password in Configuration")
    logger.info("")
    logger.info("Step 1: Find your MySQL root password")
    logger.info("  - Check if you set it during MySQL installation")
    logger.info("  - Check XAMPP: MySQL root user usually has NO password (empty)")
    logger.info("  - Check if you wrote it down during installation")
    logger.info("")
    logger.info("Step 2: Update config/config.py or create .env file")
    logger.info("")
    logger.info("  Edit config/config.py:")
    logger.info("    MYSQL_CONFIG = {")
    logger.info("        'password': 'your_actual_password',  # Update this")
    logger.info("        ...")
    logger.info("    }")
    logger.info("")
    logger.info("  Or create .env file in project root:")
    logger.info("    MYSQL_PASSWORD=your_actual_password")
    logger.info("")
    
    logger.info("Option 2: Reset MySQL Root Password")
    logger.info("")
    logger.info("If you forgot your MySQL root password:")
    logger.info("")
    logger.info("Method A - Using MySQL (if you can access it):")
    logger.info("  1. Connect to MySQL with another user or skip password:")
    logger.info("  2. Run: ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';")
    logger.info("  3. Update config/config.py with new password")
    logger.info("")
    logger.info("Method B - Reset via MySQL Configuration (XAMPP):")
    logger.info("  1. Stop MySQL service")
    logger.info("  2. Edit MySQL configuration file")
    logger.info("  3. Add: skip-grant-tables under [mysqld]")
    logger.info("  4. Start MySQL")
    logger.info("  5. Connect without password and reset")
    logger.info("")
    
    logger.info("Option 3: Create New MySQL User (Recommended)")
    logger.info("")
    logger.info("Instead of using root, create a new user:")
    logger.info("")
    logger.info("1. Connect to MySQL (if possible):")
    logger.info("   mysql -u root -p")
    logger.info("")
    logger.info("2. Create new user:")
    logger.info("   CREATE USER 'etl_user'@'localhost' IDENTIFIED BY 'etl_password';")
    logger.info("   GRANT ALL PRIVILEGES ON *.* TO 'etl_user'@'localhost';")
    logger.info("   FLUSH PRIVILEGES;")
    logger.info("")
    logger.info("3. Update config/config.py:")
    logger.info("   MYSQL_USER = 'etl_user'")
    logger.info("   MYSQL_PASSWORD = 'etl_password'")
    logger.info("")
    
    logger.info("Option 4: Test Common Passwords")
    logger.info("")
    logger.info("Common MySQL root passwords:")
    logger.info("  - (empty/no password)")
    logger.info("  - 'root'")
    logger.info("  - 'password'")
    logger.info("  - 'admin'")
    logger.info("")
    logger.info("To test a password, update config/config.py and run this script again")
    logger.info("")
    logger.info("=" * 70)
    logger.info("")
    logger.info("Quick Test - Try empty password (common for XAMPP):")
    logger.info("")
    
    # Test empty password
    logger.info("Testing with empty password...")
    result = test_connection(
        MYSQL_CONFIG['host'],
        MYSQL_CONFIG['port'],
        MYSQL_CONFIG['user'],
        ""
    )
    
    if result is True:
        logger.info("✅ SUCCESS! MySQL root password is EMPTY (no password)")
        logger.info("")
        logger.info("Update config/config.py:")
        logger.info("    'password': '',  # or os.getenv('MYSQL_PASSWORD', '')")
        logger.info("")
        logger.info("Or create .env file with:")
        logger.info("    MYSQL_PASSWORD=")
    else:
        logger.warning("❌ Empty password also doesn't work")
        logger.info("")
        logger.info("You need to find or reset your MySQL root password")
        logger.info("See solutions above")


if __name__ == "__main__":
    main()

