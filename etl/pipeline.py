"""
Main ETL Pipeline
Orchestrates Extract, Transform, Load operations
"""
from etl.extract import Extractor
from etl.transform import Transformer
from etl.load import Loader
import logging
from datetime import datetime, timedelta
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ETLPipeline:
    """Main ETL Pipeline"""
    
    def __init__(self):
        self.extractor = Extractor()
        self.transformer = Transformer()
        self.loader = Loader()
        self.last_run_time = None
    
    def get_product_info(self, product_id):
        """Get product information - in real scenario, this would come from a product catalog"""
        # Sample product data - in production, fetch from product database
        products = {
            "PROD001": {"product_name": "Wireless Headphones", "category": "Electronics", "subcategory": "Audio", "brand": "TechSound", "price": 99.99},
            "PROD002": {"product_name": "Smartphone Case", "category": "Electronics", "subcategory": "Accessories", "brand": "ProtectPlus", "price": 24.99},
            "PROD003": {"product_name": "Laptop Stand", "category": "Electronics", "subcategory": "Accessories", "brand": "ErgoDesk", "price": 49.99},
            "PROD004": {"product_name": "Running Shoes", "category": "Fashion", "subcategory": "Footwear", "brand": "SportMax", "price": 79.99},
            "PROD005": {"product_name": "Yoga Mat", "category": "Sports", "subcategory": "Fitness", "brand": "FlexFit", "price": 29.99},
            "PROD006": {"product_name": "Coffee Maker", "category": "Home", "subcategory": "Appliances", "brand": "BrewMaster", "price": 89.99},
            "PROD007": {"product_name": "Desk Lamp", "category": "Home", "subcategory": "Furniture", "brand": "BrightLight", "price": 34.99},
            "PROD008": {"product_name": "Backpack", "category": "Fashion", "subcategory": "Bags", "brand": "TravelPro", "price": 59.99},
            "PROD009": {"product_name": "Wireless Mouse", "category": "Electronics", "subcategory": "Computer", "brand": "ClickTech", "price": 19.99},
            "PROD010": {"product_name": "Water Bottle", "category": "Sports", "subcategory": "Accessories", "brand": "Hydrate", "price": 14.99},
        }
        return products.get(product_id, {"product_name": f"Product {product_id}", "category": "Uncategorized", "subcategory": "", "brand": "Unknown", "price": 0})
    
    def get_customer_info(self, customer_id):
        """Get customer information - in real scenario, this would come from customer database"""
        # In production, fetch from customer database
        # For now, return basic structure
        return {
            "customer_id": customer_id,
            "customer_name": f"Customer {customer_id}",
            "email": f"{customer_id}@example.com",
            "age": None,
            "gender": None,
            "registration_date": None,
            "customer_segment": "Standard"
        }
    
    def process_orders(self):
        """Process orders through ETL pipeline"""
        logger.info("Starting order processing...")
        
        # Extract
        orders = self.extractor.extract_orders(self.last_run_time, limit=1000)
        if not orders:
            logger.info("No new orders to process")
            return
        
        processed_count = 0
        
        for order in orders:
            try:
                # Transform
                cleaned_order = self.transformer.clean_order(order)
                if not cleaned_order:
                    continue
                
                # Get dimension keys
                # Customer dimension
                customer_info = self.get_customer_info(cleaned_order['customer_id'])
                customer_key = self.loader.upsert_customer(customer_info)
                
                # Product dimension
                product_info = self.get_product_info(cleaned_order['product_id'])
                product_info['product_id'] = cleaned_order['product_id']
                product_key = self.loader.upsert_product(product_info)
                
                # Location dimension
                location_data = self.transformer.transform_for_dim_location(cleaned_order)
                location_key = self.loader.upsert_location(location_data)
                
                # Date dimension
                date_key = self.loader.get_date_key(cleaned_order['order_date'])
                
                if not all([customer_key, product_key, location_key, date_key]):
                    logger.warning(f"Missing dimension keys for order {cleaned_order['order_id']}")
                    continue
                
                # Transform for fact table
                sales_data = self.transformer.transform_for_fact_sales(
                    cleaned_order, customer_key, product_key, location_key, date_key
                )
                
                # Load
                if sales_data:
                    self.loader.insert_fact_sales(sales_data)
                    processed_count += 1
                    
            except Exception as e:
                logger.error(f"Error processing order {order.get('order_id')}: {e}")
                continue
        
        logger.info(f"Processed {processed_count} orders successfully")
    
    def process_cart_abandonment(self):
        """Process cart abandonment data"""
        logger.info("Starting cart abandonment processing...")
        
        # Extract clicks with add_to_cart type
        clicks = self.extractor.extract_clicks(self.last_run_time, limit=1000)
        if not clicks:
            logger.info("No new clicks to process")
            return
        
        processed_count = 0
        
        for click in clicks:
            try:
                if click.get('click_type') != 'add_to_cart':
                    continue
                
                # Get dimension keys
                customer_key = None
                if click.get('customer_id'):
                    customer_info = self.get_customer_info(click['customer_id'])
                    customer_key = self.loader.upsert_customer(customer_info)
                
                product_info = self.get_product_info(click['product_id'])
                product_info['product_id'] = click['product_id']
                product_key = self.loader.upsert_product(product_info)
                
                date_key = self.loader.get_date_key(click['click_timestamp'])
                
                if not all([product_key, date_key]):
                    continue
                
                # Transform for fact table
                abandonment_data = self.transformer.transform_cart_abandonment(
                    click, customer_key, product_key, date_key
                )
                
                if abandonment_data:
                    self.loader.insert_fact_cart_abandonment(abandonment_data)
                    processed_count += 1
                    
            except Exception as e:
                logger.error(f"Error processing click {click.get('click_id')}: {e}")
                continue
        
        logger.info(f"Processed {processed_count} cart abandonment records")
    
    def run(self):
        """Run the complete ETL pipeline"""
        logger.info("=" * 50)
        logger.info("Starting ETL Pipeline Run")
        logger.info("=" * 50)
        
        start_time = datetime.now()
        
        try:
            # Process orders
            self.process_orders()
            
            # Process cart abandonment
            self.process_cart_abandonment()
            
            # Update last run time
            self.last_run_time = start_time
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info("=" * 50)
            logger.info(f"ETL Pipeline completed in {duration:.2f} seconds")
            logger.info("=" * 50)
            
        except Exception as e:
            logger.error(f"ETL Pipeline failed: {e}")
            raise
        finally:
            self.extractor.close()
            self.loader.close()
    
    def run_continuous(self, interval_seconds=30):
        """Run ETL pipeline continuously"""
        logger.info(f"Starting continuous ETL pipeline (interval: {interval_seconds}s)")
        
        while True:
            try:
                self.run()
                time.sleep(interval_seconds)
            except KeyboardInterrupt:
                logger.info("ETL pipeline stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in continuous ETL: {e}")
                time.sleep(interval_seconds)


if __name__ == "__main__":
    from config.config import ETL_CONFIG
    
    pipeline = ETLPipeline()
    
    # Run once
    # pipeline.run()
    
    # Or run continuously
    pipeline.run_continuous(interval_seconds=ETL_CONFIG['sleep_interval'])


