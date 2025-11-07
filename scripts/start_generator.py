"""
Script to start the Flask data generator
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_generator.flask_app import app
from config.config import FLASK_CONFIG
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("Starting Flask data generator server...")
    logger.info(f"Server will run on http://{FLASK_CONFIG['host']}:{FLASK_CONFIG['port']}")
    app.run(host=FLASK_CONFIG['host'], port=FLASK_CONFIG['port'], debug=FLASK_CONFIG['debug'])


