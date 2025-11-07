"""
Script to run ETL pipeline
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.pipeline import ETLPipeline
from config.config import ETL_CONFIG
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    pipeline = ETLPipeline()
    pipeline.run_continuous(interval_seconds=ETL_CONFIG['sleep_interval'])


