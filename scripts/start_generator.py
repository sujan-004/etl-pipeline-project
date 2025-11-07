"""
Start Flask data generator
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_generator.flask_app import app
from config.config import FLASK_CONFIG

if __name__ == "__main__":
    print(f"Starting Flask server on http://{FLASK_CONFIG['host']}:{FLASK_CONFIG['port']}")
    app.run(host=FLASK_CONFIG['host'], port=FLASK_CONFIG['port'], debug=FLASK_CONFIG['debug'])
