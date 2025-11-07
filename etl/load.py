"""
Load transformed data into data warehouse (star schema)
"""
from utils.database_connector import MySQLConnector
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Loader:
    """Load data into data warehouse"""
    
    def __init__(self):
        self.mysql = MySQLConnector()
        self.mysql.connect()
    
    def upsert_customer(self, customer_data):
        """Insert or update customer dimension"""
        try:
            query = """
            INSERT INTO dim_customer 
            (customer_id, customer_name, email, age, gender, registration_date, customer_segment, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                customer_name = VALUES(customer_name),
                email = VALUES(email),
                age = VALUES(age),
                gender = VALUES(gender),
                customer_segment = VALUES(customer_segment),
                updated_at = CURRENT_TIMESTAMP
            """
            params = (
                customer_data['customer_id'],
                customer_data['customer_name'],
                customer_data['email'],
                customer_data.get('age'),
                customer_data.get('gender'),
                customer_data.get('registration_date'),
                customer_data.get('customer_segment', 'Standard'),
                customer_data.get('is_active', True)
            )
            self.mysql.execute_query(query, params)
            
            # Get customer_key
            get_key_query = "SELECT customer_key FROM dim_customer WHERE customer_id = %s"
            result = self.mysql.execute_query(get_key_query, (customer_data['customer_id'],))
            if result:
                return result[0]['customer_key']
            return None
        except Exception as e:
            logger.error(f"Failed to upsert customer: {e}")
            return None
    
    def upsert_product(self, product_data):
        """Insert or update product dimension"""
        try:
            query = """
            INSERT INTO dim_product 
            (product_id, product_name, category, subcategory, brand, price, stock_quantity, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                product_name = VALUES(product_name),
                category = VALUES(category),
                subcategory = VALUES(subcategory),
                brand = VALUES(brand),
                price = VALUES(price),
                stock_quantity = VALUES(stock_quantity),
                updated_at = CURRENT_TIMESTAMP
            """
            params = (
                product_data['product_id'],
                product_data['product_name'],
                product_data.get('category', 'Uncategorized'),
                product_data.get('subcategory', ''),
                product_data.get('brand', 'Unknown'),
                product_data.get('price', 0),
                product_data.get('stock_quantity', 0),
                product_data.get('is_active', True)
            )
            self.mysql.execute_query(query, params)
            
            # Get product_key
            get_key_query = "SELECT product_key FROM dim_product WHERE product_id = %s"
            result = self.mysql.execute_query(get_key_query, (product_data['product_id'],))
            if result:
                return result[0]['product_key']
            return None
        except Exception as e:
            logger.error(f"Failed to upsert product: {e}")
            return None
    
    def upsert_location(self, location_data):
        """Insert or update location dimension"""
        try:
            query = """
            INSERT INTO dim_location 
            (city, state, country, postal_code, region)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                region = VALUES(region)
            """
            params = (
                location_data['city'],
                location_data['state'],
                location_data['country'],
                location_data.get('postal_code', ''),
                location_data.get('region', '')
            )
            self.mysql.execute_query(query, params)
            
            # Get location_key
            get_key_query = """
            SELECT location_key FROM dim_location 
            WHERE city = %s AND state = %s AND country = %s 
            AND (postal_code = %s OR (%s = '' AND postal_code IS NULL))
            """
            result = self.mysql.execute_query(
                get_key_query, 
                (location_data['city'], location_data['state'], location_data['country'],
                 location_data.get('postal_code', ''), location_data.get('postal_code', ''))
            )
            if result:
                return result[0]['location_key']
            return None
        except Exception as e:
            logger.error(f"Failed to upsert location: {e}")
            return None
    
    def get_date_key(self, date):
        """Get date key for a given date"""
        try:
            if isinstance(date, str):
                date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            date_key = int(date.strftime('%Y%m%d'))
            
            # Verify date exists in dim_date
            query = "SELECT date_key FROM dim_date WHERE date_key = %s"
            result = self.mysql.execute_query(query, (date_key,))
            if result:
                return date_key
            return None
        except Exception as e:
            logger.error(f"Failed to get date key: {e}")
            return None
    
    def insert_fact_sales(self, sales_data):
        """Insert into fact_sales table"""
        try:
            query = """
            INSERT INTO fact_sales 
            (date_key, customer_key, product_key, location_key, order_id, order_date,
             quantity, unit_price, total_amount, discount_amount, shipping_cost,
             payment_method, delivery_date, delivery_time_hours, order_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                sales_data['date_key'],
                sales_data['customer_key'],
                sales_data['product_key'],
                sales_data['location_key'],
                sales_data['order_id'],
                sales_data['order_date'],
                sales_data['quantity'],
                sales_data['unit_price'],
                sales_data['total_amount'],
                sales_data.get('discount_amount', 0),
                sales_data.get('shipping_cost', 0),
                sales_data.get('payment_method', 'unknown'),
                sales_data.get('delivery_date'),
                sales_data.get('delivery_time_hours'),
                sales_data.get('order_status', 'pending')
            )
            self.mysql.execute_query(query, params)
            return True
        except Exception as e:
            logger.error(f"Failed to insert fact_sales: {e}")
            return False
    
    def insert_fact_cart_abandonment(self, abandonment_data):
        """Insert into fact_cart_abandonment table"""
        try:
            query = """
            INSERT INTO fact_cart_abandonment 
            (date_key, customer_key, product_key, session_id, add_to_cart_time,
             abandonment_time, time_to_abandonment_minutes, cart_value, items_count,
             device_type, browser)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                abandonment_data['date_key'],
                abandonment_data.get('customer_key'),
                abandonment_data['product_key'],
                abandonment_data.get('session_id'),
                abandonment_data['add_to_cart_time'],
                abandonment_data.get('abandonment_time'),
                abandonment_data.get('time_to_abandonment_minutes', 0),
                abandonment_data.get('cart_value', 0),
                abandonment_data.get('items_count', 0),
                abandonment_data.get('device_type', 'unknown'),
                abandonment_data.get('browser', 'unknown')
            )
            self.mysql.execute_query(query, params)
            return True
        except Exception as e:
            logger.error(f"Failed to insert fact_cart_abandonment: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        self.mysql.close()


