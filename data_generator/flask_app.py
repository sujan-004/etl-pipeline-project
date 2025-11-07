"""
Flask API for Real-time Data Generation
Streams e-commerce events to MySQL
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time
from data_generator.event_generator import EventGenerator
from utils.database_connector import MySQLConnector
import json

app = Flask(__name__)
CORS(app)

generator = EventGenerator()
mysql_connector = MySQLConnector()

# Global flag for streaming
streaming_active = False
stream_thread = None


def insert_order_mysql(order):
    """Insert order into MySQL staging table"""
    try:
        if not mysql_connector.connection:
            mysql_connector.connect()
        query = """
        INSERT INTO staging_orders 
        (order_id, customer_id, product_id, order_date, order_status, quantity, 
         unit_price, total_amount, shipping_address, city, state, country, 
         postal_code, delivery_date, payment_method)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            order['order_id'], order['customer_id'], order['product_id'],
            order['order_date'], order['order_status'], order['quantity'],
            order['unit_price'], order['total_amount'], order['shipping_address'],
            order['city'], order['state'], order['country'],
            order['postal_code'], order['delivery_date'], order['payment_method']
        )
        mysql_connector.execute_query(query, params)
    except Exception as e:
        print(f"Failed to insert order: {e}")


def insert_click_mysql(click):
    """Insert click into MySQL staging table"""
    try:
        if not mysql_connector.connection:
            mysql_connector.connect()
        query = """
        INSERT INTO staging_clicks 
        (click_id, customer_id, product_id, click_type, click_timestamp, 
         session_id, device_type, browser, ip_address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            click['click_id'], click.get('customer_id'), click['product_id'],
            click['click_type'], click['click_timestamp'], click['session_id'],
            click['device_type'], click['browser'], click['ip_address']
        )
        mysql_connector.execute_query(query, params)
    except Exception as e:
        print(f"Failed to insert click: {e}")


def insert_event_mysql(event):
    """Insert customer event into MySQL staging table"""
    try:
        if not mysql_connector.connection:
            mysql_connector.connect()
        query = """
        INSERT INTO staging_customer_events 
        (event_id, customer_id, event_type, event_timestamp, event_data, session_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        event_data_str = json.dumps(event.get('event_data', {})) if event.get('event_data') else '{}'
        params = (
            event['event_id'], event['customer_id'], event['event_type'],
            event['event_timestamp'], event_data_str, event['session_id']
        )
        mysql_connector.execute_query(query, params)
    except Exception as e:
        print(f"Failed to insert event: {e}")


def stream_events():
    """Stream events continuously"""
    global streaming_active
    event_count = 0
    
    while streaming_active:
        try:
            # Generate events
            order = generator.generate_order()
            click = generator.generate_click()
            event = generator.generate_customer_event()
            
            # Insert to MySQL
            insert_order_mysql(order)
            insert_click_mysql(click)
            insert_event_mysql(event)
            
            event_count += 3
            if event_count % 30 == 0:
                print(f"Streamed {event_count} events...")
            time.sleep(2)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)


@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'E-Commerce Real-Time Data Pipeline API',
        'endpoints': {
            '/start': 'Start data streaming',
            '/stop': 'Stop data streaming',
            '/status': 'Get streaming status',
            '/generate/order': 'Generate single order',
            '/generate/click': 'Generate single click',
            '/generate/event': 'Generate single customer event'
        }
    })


@app.route('/start', methods=['POST'])
def start_streaming():
    """Start real-time data streaming"""
    global streaming_active, stream_thread
    
    if streaming_active:
        return jsonify({'status': 'error', 'message': 'Streaming already active'}), 400
    
    streaming_active = True
    stream_thread = threading.Thread(target=stream_events, daemon=True)
    stream_thread.start()
    
    return jsonify({
        'status': 'success',
        'message': 'Data streaming started'
    })


@app.route('/stop', methods=['POST'])
def stop_streaming():
    """Stop real-time data streaming"""
    global streaming_active
    
    if not streaming_active:
        return jsonify({'status': 'error', 'message': 'Streaming not active'}), 400
    
    streaming_active = False
    return jsonify({
        'status': 'success',
        'message': 'Data streaming stopped'
    })


@app.route('/status', methods=['GET'])
def get_status():
    """Get streaming status"""
    return jsonify({
        'streaming': streaming_active,
        'message': 'Streaming active' if streaming_active else 'Streaming inactive'
    })


@app.route('/generate/order', methods=['POST'])
def generate_order():
    """Generate a single order"""
    order = generator.generate_order()
    insert_order_mysql(order)
    return jsonify({'status': 'success', 'data': order})


@app.route('/generate/click', methods=['POST'])
def generate_click():
    """Generate a single click"""
    click = generator.generate_click()
    insert_click_mysql(click)
    return jsonify({'status': 'success', 'data': click})


@app.route('/generate/event', methods=['POST'])
def generate_event():
    """Generate a single customer event"""
    event = generator.generate_customer_event()
    insert_event_mysql(event)
    return jsonify({'status': 'success', 'data': event})


if __name__ == '__main__':
    from config.config import FLASK_CONFIG
    print(f"Starting server on http://{FLASK_CONFIG['host']}:{FLASK_CONFIG['port']}")
    app.run(host=FLASK_CONFIG['host'], port=FLASK_CONFIG['port'], debug=FLASK_CONFIG['debug'])

