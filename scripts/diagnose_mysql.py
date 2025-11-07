"""
Comprehensive MySQL Diagnosis Tool
Checks installation, service status, and provides solutions
"""
import sys
import os
import subprocess
import socket
import platform
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Common MySQL installation paths on Windows
MYSQL_PATHS = [
    r"C:\Program Files\MySQL\MySQL Server 8.0\bin",
    r"C:\Program Files\MySQL\MySQL Server 8.1\bin",
    r"C:\Program Files\MySQL\MySQL Server 5.7\bin",
    r"C:\xampp\mysql\bin",
    r"C:\wamp\bin\mysql\mysql8.0.xx\bin",
    r"C:\wamp64\bin\mysql\mysql8.0.xx\bin",
]


def check_mysql_in_path():
    """Check if MySQL is in system PATH"""
    try:
        result = subprocess.run(
            ['mysql', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            logger.info(f"✅ MySQL client found in PATH: {result.stdout.strip()}")
            return True, result.stdout.strip()
    except FileNotFoundError:
        pass
    except Exception as e:
        logger.debug(f"Error checking PATH: {e}")
    
    logger.warning("❌ MySQL client NOT found in system PATH")
    return False, None


def find_mysql_installation():
    """Search for MySQL installation on common paths"""
    logger.info("\n🔍 Searching for MySQL installation...")
    found_paths = []
    
    for path in MYSQL_PATHS:
        mysql_exe = os.path.join(path, 'mysql.exe')
        if os.path.exists(mysql_exe):
            found_paths.append(path)
            logger.info(f"   ✅ Found MySQL at: {path}")
    
    # Also check in Program Files (recursive search would be too slow, so we check common locations)
    program_files = [
        os.environ.get('ProgramFiles', 'C:\\Program Files'),
        os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')
    ]
    
    for pf in program_files:
        mysql_base = os.path.join(pf, 'MySQL')
        if os.path.exists(mysql_base):
            logger.info(f"   ✅ Found MySQL directory at: {mysql_base}")
            # Try to find bin directory
            for item in os.listdir(mysql_base):
                bin_path = os.path.join(mysql_base, item, 'bin')
                if os.path.exists(bin_path) and 'mysql.exe' in os.listdir(bin_path):
                    if bin_path not in found_paths:
                        found_paths.append(bin_path)
                        logger.info(f"   ✅ Found MySQL at: {bin_path}")
    
    if not found_paths:
        logger.warning("   ❌ MySQL installation not found in common locations")
    
    return found_paths


def check_mysql_service():
    """Check MySQL Windows service status"""
    logger.info("\n🔍 Checking MySQL service status...")
    
    service_names = ['MySQL80', 'MySQL', 'MySQL57', 'mysql']
    
    for service_name in service_names:
        try:
            result = subprocess.run(
                ['sc', 'query', service_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if 'RUNNING' in result.stdout:
                logger.info(f"   ✅ MySQL service '{service_name}' is RUNNING")
                return True, service_name
            elif service_name in result.stdout or 'SERVICE_NAME' in result.stdout:
                logger.warning(f"   ⚠️  MySQL service '{service_name}' found but NOT RUNNING")
                return False, service_name
        except Exception:
            continue
    
    logger.warning("   ❌ MySQL service not found")
    return False, None


def check_mysql_port():
    """Check if MySQL port 3306 is accessible"""
    logger.info("\n🔍 Checking MySQL port 3306...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(('localhost', 3306))
        sock.close()
        
        if result == 0:
            logger.info("   ✅ Port 3306 is accessible (MySQL might be running)")
            return True
        else:
            logger.warning("   ❌ Port 3306 is not accessible")
            return False
    except Exception as e:
        logger.warning(f"   ⚠️  Could not check port: {e}")
        return False


def check_xampp():
    """Check if XAMPP is installed"""
    logger.info("\n🔍 Checking for XAMPP...")
    
    xampp_paths = [
        r"C:\xampp",
        r"C:\xampp\mysql",
        os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), 'xampp'),
    ]
    
    for path in xampp_paths:
        if os.path.exists(path):
            mysql_bin = os.path.join(path, 'mysql', 'bin')
            if os.path.exists(mysql_bin):
                logger.info(f"   ✅ XAMPP found at: {path}")
                return True, mysql_bin
    
    logger.info("   ℹ️  XAMPP not found")
    return False, None


def provide_solutions(mysql_in_path, mysql_paths, service_running, service_name, port_accessible):
    """Provide solutions based on diagnosis"""
    logger.info("\n" + "=" * 70)
    logger.info("SOLUTIONS")
    logger.info("=" * 70)
    
    if mysql_in_path and service_running and port_accessible:
        logger.info("\n✅ Everything looks good! MySQL should be working.")
        logger.info("   Try running: mysql -u root -p")
        return
    
    # Case 1: MySQL not installed
    if not mysql_paths and not service_name:
        logger.info("\n📦 SOLUTION 1: Install MySQL")
        logger.info("   Option A - XAMPP (Easiest):")
        logger.info("   1. Download from: https://www.apachefriends.org/")
        logger.info("   2. Install XAMPP")
        logger.info("   3. Open XAMPP Control Panel")
        logger.info("   4. Click 'Start' next to MySQL")
        logger.info("   5. MySQL will be available at: C:\\xampp\\mysql\\bin")
        
        logger.info("\n   Option B - MySQL Installer:")
        logger.info("   1. Download from: https://dev.mysql.com/downloads/installer/")
        logger.info("   2. Choose 'MySQL Installer - Community'")
        logger.info("   3. Install MySQL Server")
        logger.info("   4. Set root password during installation")
        logger.info("   5. Choose 'Start MySQL Server as Windows Service'")
        
        logger.info("\n   Option C - Docker:")
        logger.info("   docker run --name mysql-ecommerce -e MYSQL_ROOT_PASSWORD=root")
        logger.info("              -e MYSQL_DATABASE=ecommerce_db -p 3306:3306 -d mysql:8.0")
    
    # Case 2: MySQL installed but not in PATH
    elif mysql_paths and not mysql_in_path:
        logger.info("\n🔧 SOLUTION 2: Add MySQL to System PATH")
        logger.info(f"   MySQL found at: {mysql_paths[0]}")
        logger.info("\n   Method 1 - Temporary (Current Session):")
        logger.info(f"   set PATH=%PATH%;{mysql_paths[0]}")
        
        logger.info("\n   Method 2 - Permanent (Recommended):")
        logger.info("   1. Press Win + X, select 'System'")
        logger.info("   2. Click 'Advanced system settings'")
        logger.info("   3. Click 'Environment Variables'")
        logger.info("   4. Under 'System variables', find 'Path' and click 'Edit'")
        logger.info("   5. Click 'New' and add:")
        logger.info(f"      {mysql_paths[0]}")
        logger.info("   6. Click OK on all windows")
        logger.info("   7. Close and reopen Command Prompt")
        
        logger.info("\n   Or use full path to MySQL:")
        logger.info(f"   \"{os.path.join(mysql_paths[0], 'mysql.exe')}\" -u root -p")
    
    # Case 3: MySQL service not running
    if mysql_paths and not service_running and service_name:
        logger.info("\n🚀 SOLUTION 3: Start MySQL Service")
        logger.info(f"   Service name: {service_name}")
        logger.info("\n   Method 1 - Command Prompt (as Administrator):")
        logger.info(f"   net start {service_name}")
        
        logger.info("\n   Method 2 - Services GUI:")
        logger.info("   1. Press Win + R")
        logger.info("   2. Type 'services.msc' and press Enter")
        logger.info(f"   3. Find '{service_name}' service")
        logger.info("   4. Right-click → Start")
        
        logger.info("\n   Method 3 - XAMPP:")
        logger.info("   1. Open XAMPP Control Panel")
        logger.info("   2. Click 'Start' next to MySQL")
    
    # Case 4: MySQL running but port not accessible
    if service_running and not port_accessible:
        logger.info("\n🔌 SOLUTION 4: Check MySQL Configuration")
        logger.info("   MySQL service is running but port is not accessible.")
        logger.info("   - Check MySQL configuration file (my.ini)")
        logger.info("   - Verify MySQL is bound to localhost")
        logger.info("   - Check firewall settings")
    
    logger.info("\n" + "=" * 70)


def main():
    """Run complete diagnosis"""
    logger.info("=" * 70)
    logger.info("MySQL DIAGNOSIS TOOL")
    logger.info("=" * 70)
    logger.info(f"\nSystem: {platform.system()} {platform.release()}")
    logger.info(f"Python: {sys.version.split()[0]}")
    
    # Run all checks
    mysql_in_path, mysql_version = check_mysql_in_path()
    mysql_paths = find_mysql_installation()
    service_running, service_name = check_mysql_service()
    port_accessible = check_mysql_port()
    xampp_found, xampp_path = check_xampp()
    
    if xampp_found and xampp_path not in mysql_paths:
        mysql_paths.append(xampp_path)
    
    # Provide solutions
    provide_solutions(mysql_in_path, mysql_paths, service_running, service_name, port_accessible)
    
    logger.info("\n💡 Quick Test:")
    if mysql_paths:
        mysql_exe = os.path.join(mysql_paths[0], 'mysql.exe')
        logger.info(f"   Try: \"{mysql_exe}\" -u root -p")
    else:
        logger.info("   Install MySQL first, then try: mysql -u root -p")
    
    logger.info("\n" + "=" * 70)


if __name__ == "__main__":
    main()

