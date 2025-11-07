"""
Power BI Data Export Script
Exports data from data warehouse in Power BI compatible format
"""
import sys
import os
import pandas as pd
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database_connector import MySQLConnector
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PowerBIExporter:
    """Export data for Power BI"""
    
    def __init__(self):
        self.mysql = MySQLConnector()
        self.mysql.connect()
        self.export_dir = "powerbi_exports"
        os.makedirs(self.export_dir, exist_ok=True)
    
    def export_sales_trends(self):
        """Export sales trends data"""
        logger.info("Exporting sales trends data...")
        
        query = """
        SELECT 
            d.full_date,
            d.year,
            d.quarter,
            d.month,
            d.month_name,
            d.day_name,
            p.category,
            p.subcategory,
            p.brand,
            SUM(fs.quantity) as total_quantity,
            SUM(fs.total_amount) as total_sales,
            AVG(fs.total_amount) as avg_order_value,
            COUNT(DISTINCT fs.order_id) as total_orders,
            COUNT(DISTINCT fs.customer_key) as unique_customers
        FROM fact_sales fs
        JOIN dim_date d ON fs.date_key = d.date_key
        JOIN dim_product p ON fs.product_key = p.product_key
        GROUP BY d.full_date, d.year, d.quarter, d.month, d.month_name, d.day_name,
                 p.category, p.subcategory, p.brand
        ORDER BY d.full_date DESC, p.category
        """
        
        results = self.mysql.execute_query(query)
        df = pd.DataFrame(results)
        
        filename = f"{self.export_dir}/sales_trends_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        logger.info(f"Exported {len(df)} records to {filename}")
        return filename
    
    def export_cart_abandonment(self):
        """Export cart abandonment data"""
        logger.info("Exporting cart abandonment data...")
        
        query = """
        SELECT 
            d.full_date,
            d.year,
            d.month,
            d.month_name,
            p.category,
            p.product_name,
            AVG(fca.time_to_abandonment_minutes) as avg_abandonment_time,
            SUM(fca.cart_value) as total_abandoned_value,
            COUNT(*) as abandonment_count,
            AVG(fca.items_count) as avg_items_per_abandoned_cart,
            fca.device_type,
            fca.browser
        FROM fact_cart_abandonment fca
        JOIN dim_date d ON fca.date_key = d.date_key
        JOIN dim_product p ON fca.product_key = p.product_key
        GROUP BY d.full_date, d.year, d.month, d.month_name, p.category, p.product_name,
                 fca.device_type, fca.browser
        ORDER BY d.full_date DESC, abandonment_count DESC
        """
        
        results = self.mysql.execute_query(query)
        df = pd.DataFrame(results)
        
        filename = f"{self.export_dir}/cart_abandonment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        logger.info(f"Exported {len(df)} records to {filename}")
        return filename
    
    def export_delivery_times(self):
        """Export delivery time analytics"""
        logger.info("Exporting delivery time data...")
        
        query = """
        SELECT 
            d.full_date,
            d.year,
            d.month,
            d.month_name,
            l.country,
            l.state,
            l.city,
            p.category,
            AVG(fs.delivery_time_hours) as avg_delivery_time_hours,
            MIN(fs.delivery_time_hours) as min_delivery_time_hours,
            MAX(fs.delivery_time_hours) as max_delivery_time_hours,
            COUNT(*) as delivery_count,
            fs.order_status
        FROM fact_sales fs
        JOIN dim_date d ON fs.date_key = d.date_key
        JOIN dim_location l ON fs.location_key = l.location_key
        JOIN dim_product p ON fs.product_key = p.product_key
        WHERE fs.delivery_time_hours IS NOT NULL
        GROUP BY d.full_date, d.year, d.month, d.month_name, l.country, l.state, l.city,
                 p.category, fs.order_status
        ORDER BY d.full_date DESC, avg_delivery_time_hours DESC
        """
        
        results = self.mysql.execute_query(query)
        df = pd.DataFrame(results)
        
        filename = f"{self.export_dir}/delivery_times_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        logger.info(f"Exported {len(df)} records to {filename}")
        return filename
    
    def export_customer_analytics(self):
        """Export customer analytics"""
        logger.info("Exporting customer analytics data...")
        
        query = """
        SELECT 
            c.customer_id,
            c.customer_name,
            c.email,
            c.age,
            c.gender,
            c.customer_segment,
            l.country,
            l.state,
            COUNT(DISTINCT fs.order_id) as total_orders,
            SUM(fs.total_amount) as total_spent,
            AVG(fs.total_amount) as avg_order_value,
            MIN(fs.order_date) as first_order_date,
            MAX(fs.order_date) as last_order_date,
            DATEDIFF(MAX(fs.order_date), MIN(fs.order_date)) as customer_lifetime_days
        FROM dim_customer c
        LEFT JOIN fact_sales fs ON c.customer_key = fs.customer_key
        LEFT JOIN dim_location l ON fs.location_key = l.location_key
        GROUP BY c.customer_key, c.customer_id, c.customer_name, c.email, c.age, c.gender,
                 c.customer_segment, l.country, l.state
        HAVING total_orders > 0
        ORDER BY total_spent DESC
        """
        
        results = self.mysql.execute_query(query)
        df = pd.DataFrame(results)
        
        filename = f"{self.export_dir}/customer_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        logger.info(f"Exported {len(df)} records to {filename}")
        return filename
    
    def export_all(self):
        """Export all datasets"""
        logger.info("Exporting all datasets for Power BI...")
        files = []
        files.append(self.export_sales_trends())
        files.append(self.export_cart_abandonment())
        files.append(self.export_delivery_times())
        files.append(self.export_customer_analytics())
        logger.info(f"All exports completed. Files saved to {self.export_dir}/")
        return files
    
    def create_powerbi_query_file(self):
        """Create a Power BI M query file for direct connection"""
        from config.config import MYSQL_CONFIG
        query_template = f"""
let
    Source = MySQL.Database("{MYSQL_CONFIG['host']}", "{MYSQL_CONFIG['database']}", [
        Query="
        SELECT 
            d.full_date,
            d.year,
            d.month,
            d.month_name,
            p.category,
            p.product_name,
            SUM(fs.total_amount) as total_sales,
            COUNT(fs.order_id) as order_count
        FROM fact_sales fs
        JOIN dim_date d ON fs.date_key = d.date_key
        JOIN dim_product p ON fs.product_key = p.product_key
        GROUP BY d.full_date, d.year, d.month, d.month_name, p.category, p.product_name
        "
    ])
in
    Source
        """
        
        filename = f"{self.export_dir}/powerbi_query.m"
        with open(filename, 'w') as f:
            f.write(query_template)
        logger.info(f"Power BI query file created: {filename}")
        return filename
    
    def close(self):
        """Close database connection"""
        self.mysql.close()


if __name__ == "__main__":
    exporter = PowerBIExporter()
    try:
        # Export all datasets
        exporter.export_all()
        
        # Create Power BI query file
        exporter.create_powerbi_query_file()
        
        logger.info("Power BI export completed successfully!")
    except Exception as e:
        logger.error(f"Export failed: {e}")
    finally:
        exporter.close()

