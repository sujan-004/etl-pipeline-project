"""
Check MySQL installation and connection
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import MYSQL_CONFIG
import socket
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_mysql_port():
    """Check if MySQL port is accessible"""
    host = MYSQL_CONFIG['host']
    port = MYSQL_CONFIG['port']
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            logger.info(f"✅ MySQL port {port} is accessible on {host}")
            return True
        else:
            logger.error(f"❌ Cannot connect to MySQL on {host}:{port}")
            return False
    except Exception as e:
        logger.error(f"❌ Error checking MySQL port: {e}")
        return False


def check_mysql_service_windows():
    """Check if MySQL service is running on Windows"""
    try:
        result = subprocess.run(
            ['sc', 'query', 'MySQL80'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if 'RUNNING' in result.stdout:
            logger.info("✅ MySQL service (MySQL80) is RUNNING")
            return True
        elif 'MySQL80' in result.stdout:
            logger.warning("⚠️  MySQL service (MySQL80) is found but NOT RUNNING")
            logger.info("   To start MySQL service, run as Administrator:")
            logger.info("   net start MySQL80")
            return False
        else:
            logger.warning("⚠️  MySQL80 service not found")
            return False
    except Exception as e:
        logger.warning(f"⚠️  Could not check MySQL service: {e}")
        return False


def check_mysql_installed():
    """Check if MySQL client is installed"""
    try:
        result = subprocess.run(
            ['mysql', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            logger.info(f"✅ MySQL client is installed: {result.stdout.strip()}")
            return True
        else:
            logger.warning("⚠️  MySQL client not found in PATH")
            return False
    except FileNotFoundError:
        logger.warning("⚠️  MySQL client not found in PATH")
        return False
    except Exception as e:
        logger.warning(f"⚠️  Could not check MySQL installation: {e}")
        return False


def main():
    """Run all checks"""
    logger.info("=" * 60)
    logger.info("MySQL Connection Diagnostic")
    logger.info("=" * 60)
    logger.info(f"\nConfiguration:")
    logger.info(f"  Host: {MYSQL_CONFIG['host']}")
    logger.info(f"  Port: {MYSQL_CONFIG['port']}")
    logger.info(f"  User: {MYSQL_CONFIG['user']}")
    logger.info(f"  Database: {MYSQL_CONFIG['database']}")
    logger.info("")
    
    # Check MySQL installation
    logger.info("1. Checking MySQL installation...")
    mysql_installed = check_mysql_installed()
    logger.info("")
    
    # Check MySQL service (Windows)
    logger.info("2. Checking MySQL service...")
    service_running = check_mysql_service_windows()
    logger.info("")
    
    # Check MySQL port
    logger.info("3. Checking MySQL port connection...")
    port_accessible = check_mysql_port()
    logger.info("")
    
    # Summary
    logger.info("=" * 60)
    logger.info("Summary")
    logger.info("=" * 60)
    
    if port_accessible:
        logger.info("✅ MySQL server is accessible!")
        logger.info("   You can proceed with database setup.")
    else:
        logger.error("❌ MySQL server is NOT accessible")
        logger.info("")
        logger.info("Solutions:")
        logger.info("")
        logger.info("1. Install MySQL Server:")
        logger.info("   - Download from: https://dev.mysql.com/downloads/mysql/")
        logger.info("   - Or use XAMPP: https://www.apachefriends.org/")
        logger.info("   - Or use MySQL Installer for Windows")
        logger.info("")
        logger.info("2. Start MySQL Service (if installed):")
        logger.info("   - Open Command Prompt as Administrator")
        logger.info("   - Run: net start MySQL80")
        logger.info("   - Or check Services (services.msc) and start MySQL")
        logger.info("")
        logger.info("3. Check MySQL Configuration:")
        logger.info("   - Verify MySQL is running on port 3306")
        logger.info("   - Check if MySQL is bound to localhost")
        logger.info("   - Update config/config.py if using different host/port")
        logger.info("")
        logger.info("4. Alternative: Use SQLite for testing")
        logger.info("   (Would require code modifications)")
    
    logger.info("=" * 60)


if __name__ == "__main__":
    main()

