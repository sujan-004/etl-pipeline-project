"""
Transform and clean data
"""
import logging
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Transformer:
    """Transform and clean extracted data"""
    
    @staticmethod
    def clean_order(order):
        """Clean and validate order data"""
        try:
            # Ensure required fields exist
            if not all(key in order for key in ['order_id', 'customer_id', 'product_id', 'order_date']):
                return None
            
            # Clean numeric fields
            order['quantity'] = max(1, int(order.get('quantity', 1)))
            order['unit_price'] = max(0, float(order.get('unit_price', 0)))
            order['total_amount'] = max(0, float(order.get('total_amount', 0)))
            
            # Ensure order_date is datetime
            if isinstance(order['order_date'], str):
                order['order_date'] = datetime.strptime(order['order_date'], '%Y-%m-%d %H:%M:%S')
            
            # Clean delivery_date
            if order.get('delivery_date'):
                if isinstance(order['delivery_date'], str):
                    order['delivery_date'] = datetime.strptime(order['delivery_date'], '%Y-%m-%d %H:%M:%S')
            else:
                order['delivery_date'] = None
            
            # Calculate delivery time in hours
            if order['delivery_date'] and order['order_date']:
                delta = order['delivery_date'] - order['order_date']
                order['delivery_time_hours'] = int(delta.total_seconds() / 3600)
            else:
                order['delivery_time_hours'] = None
            
            # Clean string fields
            order['order_status'] = order.get('order_status', 'pending').lower()
            order['city'] = order.get('city', '').strip()
            order['state'] = order.get('state', '').strip()
            order['country'] = order.get('country', '').strip()
            
            return order
        except Exception as e:
            logger.error(f"Failed to clean order {order.get('order_id')}: {e}")
            return None
    
    @staticmethod
    def transform_for_dim_customer(customer_data):
        """Transform data for customer dimension"""
        try:
            return {
                'customer_id': customer_data.get('customer_id'),
                'customer_name': customer_data.get('customer_name', 'Unknown'),
                'email': customer_data.get('email', ''),
                'age': customer_data.get('age'),
                'gender': customer_data.get('gender', 'Unknown'),
                'registration_date': customer_data.get('registration_date'),
                'customer_segment': customer_data.get('customer_segment', 'Standard'),
                'is_active': True
            }
        except Exception as e:
            logger.error(f"Failed to transform customer data: {e}")
            return None
    
    @staticmethod
    def transform_for_dim_product(product_data):
        """Transform data for product dimension"""
        try:
            return {
                'product_id': product_data.get('product_id'),
                'product_name': product_data.get('product_name', 'Unknown Product'),
                'category': product_data.get('category', 'Uncategorized'),
                'subcategory': product_data.get('subcategory', ''),
                'brand': product_data.get('brand', 'Unknown'),
                'price': float(product_data.get('price', 0)),
                'stock_quantity': product_data.get('stock_quantity', 0),
                'is_active': True
            }
        except Exception as e:
            logger.error(f"Failed to transform product data: {e}")
            return None
    
    @staticmethod
    def transform_for_dim_location(order):
        """Transform data for location dimension"""
        try:
            return {
                'city': order.get('city', 'Unknown'),
                'state': order.get('state', 'Unknown'),
                'country': order.get('country', 'Unknown'),
                'postal_code': order.get('postal_code', ''),
                'region': order.get('region', '')
            }
        except Exception as e:
            logger.error(f"Failed to transform location data: {e}")
            return None
    
    @staticmethod
    def transform_for_fact_sales(order, customer_key, product_key, location_key, date_key):
        """Transform order for fact_sales table"""
        try:
            order_date = order['order_date']
            if isinstance(order_date, str):
                order_date = datetime.strptime(order_date, '%Y-%m-%d %H:%M:%S')
            
            delivery_date = order.get('delivery_date')
            if delivery_date and isinstance(delivery_date, str):
                delivery_date = datetime.strptime(delivery_date, '%Y-%m-%d %H:%M:%S')
            
            return {
                'date_key': date_key,
                'customer_key': customer_key,
                'product_key': product_key,
                'location_key': location_key,
                'order_id': order['order_id'],
                'order_date': order_date,
                'quantity': int(order['quantity']),
                'unit_price': float(order['unit_price']),
                'total_amount': float(order['total_amount']),
                'discount_amount': float(order.get('discount_amount', 0)),
                'shipping_cost': float(order.get('shipping_cost', 0)),
                'payment_method': order.get('payment_method', 'unknown'),
                'delivery_date': delivery_date,
                'delivery_time_hours': order.get('delivery_time_hours'),
                'order_status': order.get('order_status', 'pending')
            }
        except Exception as e:
            logger.error(f"Failed to transform order for fact_sales: {e}")
            return None
    
    @staticmethod
    def transform_cart_abandonment(click, customer_key, product_key, date_key):
        """Transform click data for cart abandonment fact table"""
        try:
            if click.get('click_type') != 'add_to_cart':
                return None
            
            # Find related checkout attempts or abandonment
            add_to_cart_time = click['click_timestamp']
            if isinstance(add_to_cart_time, str):
                add_to_cart_time = datetime.strptime(add_to_cart_time, '%Y-%m-%d %H:%M:%S')
            
            return {
                'date_key': date_key,
                'customer_key': customer_key,
                'product_key': product_key,
                'session_id': click.get('session_id'),
                'add_to_cart_time': add_to_cart_time,
                'abandonment_time': add_to_cart_time,  # Simplified - would need more logic
                'time_to_abandonment_minutes': 30,  # Default value
                'cart_value': 0,  # Would need to calculate from session
                'items_count': 1,
                'device_type': click.get('device_type', 'unknown'),
                'browser': click.get('browser', 'unknown')
            }
        except Exception as e:
            logger.error(f"Failed to transform cart abandonment: {e}")
            return None
    
    @staticmethod
    def get_date_key(date):
        """Get date key from date (YYYYMMDD format)"""
        try:
            if isinstance(date, str):
                date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            elif isinstance(date, datetime):
                pass
            else:
                return None
            
            return int(date.strftime('%Y%m%d'))
        except Exception as e:
            logger.error(f"Failed to get date key: {e}")
            return None


