"""
MySQL Database Setup Script
"""
import pymysql
from config.config import MYSQL_CONFIG
import logging
import os
from datetime import datetime, timedelta
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def populate_date_dimension(connection):
    """Populate date dimension table"""
    try:
        logger.info("Populating date dimension...")
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2030, 12, 31)
        current_date = start_date
        
        insert_query = """
        INSERT INTO dim_date 
        (date_key, full_date, year, quarter, month, month_name,
         week, day_of_month, day_of_week, day_name, is_weekend, is_holiday)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE full_date = VALUES(full_date)
        """
        
        month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        batch = []
        batch_size = 1000
        
        with connection.cursor() as cursor:
            while current_date <= end_date:
                date_key = int(current_date.strftime('%Y%m%d'))
                year = current_date.year
                quarter = (current_date.month - 1) // 3 + 1
                month = current_date.month
                month_name = month_names[month]
                
                # Calculate week number (ISO week)
                week = current_date.isocalendar()[1]
                day_of_month = current_date.day
                day_of_week = current_date.weekday() + 1  # 1=Monday, 7=Sunday
                day_name = day_names[current_date.weekday()]
                is_weekend = day_of_week in [6, 7]  # Saturday or Sunday
                
                batch.append((
                    date_key, current_date.date(), year, quarter, month, month_name,
                    week, day_of_month, day_of_week, day_name, is_weekend, False
                ))
                
                if len(batch) >= batch_size:
                    cursor.executemany(insert_query, batch)
                    connection.commit()
                    logger.info(f"Inserted {len(batch)} date records...")
                    batch = []
                
                current_date += timedelta(days=1)
            
            # Insert remaining records
            if batch:
                cursor.executemany(insert_query, batch)
                connection.commit()
                logger.info(f"Inserted {len(batch)} date records...")
        
        logger.info("Date dimension populated successfully")
    except Exception as e:
        logger.error(f"Failed to populate date dimension: {e}")
        raise


def execute_sql_file(connection, file_path):
    """Execute SQL file statement by statement"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove stored procedure section
    if 'Populate Date Dimension' in content:
        content = content.split('Populate Date Dimension')[0]
    
    # Remove DELIMITER commands
    content = re.sub(r'DELIMITER\s+\$\$.*?\$\$', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'DELIMITER\s*;', '', content, flags=re.IGNORECASE)
    
    # Split by semicolon, but handle it more carefully
    # First, normalize line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Split into statements
    statements = []
    current = []
    in_string = False
    string_char = None
    
    i = 0
    while i < len(content):
        char = content[i]
        
        # Track string literals
        if char in ("'", '"') and (i == 0 or content[i-1] != '\\'):
            if not in_string:
                in_string = True
                string_char = char
            elif char == string_char:
                in_string = False
                string_char = None
        
        current.append(char)
        
        # If semicolon and not in string, end of statement
        if char == ';' and not in_string:
            stmt = ''.join(current).strip()
            # Remove trailing semicolon
            stmt = stmt.rstrip(';').strip()
            # Remove comments
            stmt = re.sub(r'--.*$', '', stmt, flags=re.MULTILINE)
            stmt = stmt.strip()
            
            if stmt and not stmt.upper().startswith('DELIMITER'):
                statements.append(stmt)
            current = []
        
        i += 1
    
    # Execute statements
    logger.info(f"Found {len(statements)} SQL statements to execute")
    executed = 0
    errors = 0
    
    with connection.cursor() as cursor:
        for i, statement in enumerate(statements, 1):
            if not statement or len(statement) < 10:  # Skip very short statements
                continue
            
            try:
                cursor.execute(statement)
                connection.commit()
                executed += 1
                
                # Log CREATE TABLE statements
                if 'CREATE TABLE' in statement.upper():
                    # Extract table name
                    match = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?(\w+)`?', statement, re.IGNORECASE)
                    if match:
                        table_name = match.group(1)
                        logger.info(f"  ✅ Created table: {table_name}")
                    
            except pymysql.err.ProgrammingError as e:
                error_msg = str(e).lower()
                # Ignore "table doesn't exist" for DROP TABLE IF EXISTS
                if 'drop table' in statement.lower() and ('doesn\'t exist' in error_msg or 'unknown table' in error_msg):
                    continue
                # Ignore "already exists" for CREATE TABLE IF NOT EXISTS
                elif 'already exists' in error_msg:
                    match = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?(\w+)`?', statement, re.IGNORECASE)
                    if match:
                        logger.info(f"  ℹ️  Table {match.group(1)} already exists")
                    continue
                else:
                    logger.error(f"  ❌ Error in statement {i}: {e}")
                    logger.error(f"  Statement: {statement[:150]}...")
                    errors += 1
                    # Don't raise - continue with other statements
            except Exception as e:
                error_msg = str(e).lower()
                if 'drop table' in statement.lower():
                    continue  # Ignore DROP errors
                logger.warning(f"  ⚠️  Warning in statement {i}: {e}")
                logger.debug(f"  Statement: {statement[:150]}...")
    
    logger.info(f"Executed {executed} statements successfully")
    if errors > 0:
        logger.warning(f"Encountered {errors} errors (non-critical)")
    
    return executed, errors


def setup_database():
    """Create database and tables"""
    try:
        # Connect without database to create it
        connection = pymysql.connect(
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            logger.info(f"✅ Database '{MYSQL_CONFIG['database']}' created or already exists")
        
        connection.close()
        
        # Connect to the database
        connection = pymysql.connect(
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            database=MYSQL_CONFIG['database'],
            charset='utf8mb4'
        )
        
        # Execute SQL schema file
        schema_path = os.path.join(os.path.dirname(__file__), 'schemas.sql')
        logger.info(f"Reading schema file: {schema_path}")
        execute_sql_file(connection, schema_path)
        
        # Verify dim_date table exists
        logger.info("Verifying tables were created...")
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES LIKE 'dim_date'")
            result = cursor.fetchone()
            if not result:
                logger.error("❌ ERROR: dim_date table was not created!")
                logger.error("This might be due to SQL parsing issues.")
                logger.error("Trying to create dim_date table manually...")
                
                # Create dim_date table manually as fallback
                create_dim_date = """
                CREATE TABLE IF NOT EXISTS dim_date (
                    date_key INT PRIMARY KEY,
                    full_date DATE NOT NULL,
                    year INT NOT NULL,
                    quarter INT NOT NULL,
                    month INT NOT NULL,
                    month_name VARCHAR(20) NOT NULL,
                    week INT NOT NULL,
                    day_of_month INT NOT NULL,
                    day_of_week INT NOT NULL,
                    day_name VARCHAR(20) NOT NULL,
                    is_weekend BOOLEAN NOT NULL,
                    is_holiday BOOLEAN DEFAULT FALSE,
                    UNIQUE KEY unique_date (full_date)
                )
                """
                cursor.execute(create_dim_date)
                connection.commit()
                logger.info("✅ dim_date table created manually")
            else:
                logger.info("✅ dim_date table exists")
        
        # Populate date dimension
        populate_date_dimension(connection)
        
        logger.info("")
        logger.info("=" * 70)
        logger.info("✅ Database schema created successfully!")
        logger.info("=" * 70)
        connection.close()
        
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        raise


if __name__ == "__main__":
    setup_database()
