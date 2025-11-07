"""
Real-time E-Commerce Event Generator
Generates orders, clicks, and customer events
"""
from faker import Faker
import random
import uuid
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = Faker()

# Sample data pools
PRODUCTS = [
    {"id": "PROD001", "name": "Wireless Headphones", "category": "Electronics", "subcategory": "Audio", "brand": "TechSound", "price": 99.99},
    {"id": "PROD002", "name": "Smartphone Case", "category": "Electronics", "subcategory": "Accessories", "brand": "ProtectPlus", "price": 24.99},
    {"id": "PROD003", "name": "Laptop Stand", "category": "Electronics", "subcategory": "Accessories", "brand": "ErgoDesk", "price": 49.99},
    {"id": "PROD004", "name": "Running Shoes", "category": "Fashion", "subcategory": "Footwear", "brand": "SportMax", "price": 79.99},
    {"id": "PROD005", "name": "Yoga Mat", "category": "Sports", "subcategory": "Fitness", "brand": "FlexFit", "price": 29.99},
    {"id": "PROD006", "name": "Coffee Maker", "category": "Home", "subcategory": "Appliances", "brand": "BrewMaster", "price": 89.99},
    {"id": "PROD007", "name": "Desk Lamp", "category": "Home", "subcategory": "Furniture", "brand": "BrightLight", "price": 34.99},
    {"id": "PROD008", "name": "Backpack", "category": "Fashion", "subcategory": "Bags", "brand": "TravelPro", "price": 59.99},
    {"id": "PROD009", "name": "Wireless Mouse", "category": "Electronics", "subcategory": "Computer", "brand": "ClickTech", "price": 19.99},
    {"id": "PROD010", "name": "Water Bottle", "category": "Sports", "subcategory": "Accessories", "brand": "Hydrate", "price": 14.99},
]

CLICK_TYPES = ['view', 'add_to_cart', 'remove_from_cart', 'checkout']
EVENT_TYPES = ['login', 'logout', 'signup', 'profile_update', 'password_reset']
ORDER_STATUSES = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
PAYMENT_METHODS = ['credit_card', 'debit_card', 'paypal', 'cash_on_delivery']
DEVICE_TYPES = ['desktop', 'mobile', 'tablet']
BROWSERS = ['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera']


class EventGenerator:
    """Generate realistic e-commerce events"""
    
    def __init__(self):
        self.customers = {}  # Store customer data
        self.sessions = {}  # Store session data
    
    def generate_customer_id(self):
        """Generate or retrieve customer ID"""
        if random.random() < 0.7 and len(self.customers) > 0:
            # 70% chance to use existing customer
            return random.choice(list(self.customers.keys()))
        else:
            # Generate new customer
            customer_id = f"CUST{random.randint(1000, 9999)}"
            self.customers[customer_id] = {
                'name': fake.name(),
                'email': fake.email(),
                'age': random.randint(18, 80),
                'gender': random.choice(['Male', 'Female', 'Other']),
                'registration_date': fake.date_between(start_date='-2y', end_date='today')
            }
            return customer_id
    
    def generate_session_id(self):
        """Generate session ID"""
        return f"SESSION{random.randint(100000, 999999)}"
    
    def generate_order(self):
        """Generate an order event"""
        order_id = f"ORD{random.randint(100000, 999999)}"
        customer_id = self.generate_customer_id()
        product = random.choice(PRODUCTS)
        quantity = random.randint(1, 5)
        unit_price = product['price']
        total_amount = unit_price * quantity
        
        # Calculate delivery date (1-7 days after order)
        order_date = datetime.now() - timedelta(hours=random.randint(0, 24))
        delivery_days = random.randint(1, 7)
        delivery_date = order_date + timedelta(days=delivery_days)
        
        order = {
            'order_id': order_id,
            'customer_id': customer_id,
            'product_id': product['id'],
            'order_date': order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'order_status': random.choice(ORDER_STATUSES),
            'quantity': quantity,
            'unit_price': float(unit_price),
            'total_amount': float(total_amount),
            'shipping_address': fake.address(),
            'city': fake.city(),
            'state': fake.state(),
            'country': fake.country(),
            'postal_code': fake.zipcode(),
            'delivery_date': delivery_date.strftime('%Y-%m-%d %H:%M:%S'),
            'payment_method': random.choice(PAYMENT_METHODS)
        }
        
        return order
    
    def generate_click(self):
        """Generate a click/view event"""
        click_id = f"CLICK{random.randint(100000, 999999)}"
        customer_id = self.generate_customer_id() if random.random() < 0.8 else None
        product = random.choice(PRODUCTS)
        click_type = random.choice(CLICK_TYPES)
        session_id = self.generate_session_id()
        
        click = {
            'click_id': click_id,
            'customer_id': customer_id,
            'product_id': product['id'],
            'click_type': click_type,
            'click_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'session_id': session_id,
            'device_type': random.choice(DEVICE_TYPES),
            'browser': random.choice(BROWSERS),
            'ip_address': fake.ipv4()
        }
        
        return click
    
    def generate_customer_event(self):
        """Generate a customer event"""
        event_id = f"EVT{random.randint(100000, 999999)}"
        customer_id = self.generate_customer_id()
        event_type = random.choice(EVENT_TYPES)
        session_id = self.generate_session_id()
        
        event_data = {}
        if event_type == 'profile_update':
            event_data = {'field_updated': random.choice(['email', 'address', 'phone', 'preferences'])}
        elif event_type == 'signup':
            event_data = {'source': random.choice(['web', 'mobile_app', 'referral'])}
        
        event = {
            'event_id': event_id,
            'customer_id': customer_id,
            'event_type': event_type,
            'event_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'event_data': event_data,
            'session_id': session_id
        }
        
        return event
    
    def generate_cart_abandonment(self):
        """Generate cart abandonment data"""
        customer_id = self.generate_customer_id()
        product = random.choice(PRODUCTS)
        session_id = self.generate_session_id()
        
        add_to_cart_time = datetime.now() - timedelta(minutes=random.randint(5, 60))
        abandonment_time = datetime.now()
        time_to_abandonment = int((abandonment_time - add_to_cart_time).total_seconds() / 60)
        
        abandonment = {
            'session_id': session_id,
            'customer_id': customer_id,
            'product_id': product['id'],
            'add_to_cart_time': add_to_cart_time.strftime('%Y-%m-%d %H:%M:%S'),
            'abandonment_time': abandonment_time.strftime('%Y-%m-%d %H:%M:%S'),
            'time_to_abandonment_minutes': time_to_abandonment,
            'cart_value': float(product['price'] * random.randint(1, 3)),
            'items_count': random.randint(1, 3),
            'device_type': random.choice(DEVICE_TYPES),
            'browser': random.choice(BROWSERS)
        }
        
        return abandonment


