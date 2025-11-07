-- E-Commerce Data Pipeline Database Schemas
-- Staging Tables and Star Schema Data Warehouse

-- Drop existing tables if they exist (for fresh setup)
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS fact_cart_abandonment;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_location;
DROP TABLE IF EXISTS staging_orders;
DROP TABLE IF EXISTS staging_clicks;
DROP TABLE IF EXISTS staging_customer_events;

-- ============================================
-- STAGING TABLES (Raw data ingestion)
-- ============================================

-- Staging table for orders
CREATE TABLE staging_orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    order_date DATETIME NOT NULL,
    order_status VARCHAR(20) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    shipping_address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    delivery_date DATETIME,
    payment_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order_date (order_date),
    INDEX idx_customer_id (customer_id),
    INDEX idx_product_id (product_id)
);

-- Staging table for clicks/views
CREATE TABLE staging_clicks (
    click_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    product_id VARCHAR(50) NOT NULL,
    click_type VARCHAR(20) NOT NULL, -- 'view', 'add_to_cart', 'remove_from_cart', 'checkout'
    click_timestamp DATETIME NOT NULL,
    session_id VARCHAR(50),
    device_type VARCHAR(20),
    browser VARCHAR(50),
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_click_timestamp (click_timestamp),
    INDEX idx_customer_id (customer_id),
    INDEX idx_product_id (product_id),
    INDEX idx_click_type (click_type)
);

-- Staging table for customer events
CREATE TABLE staging_customer_events (
    event_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    event_type VARCHAR(50) NOT NULL, -- 'login', 'logout', 'signup', 'profile_update', etc.
    event_timestamp DATETIME NOT NULL,
    event_data JSON,
    session_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_event_timestamp (event_timestamp),
    INDEX idx_customer_id (customer_id),
    INDEX idx_event_type (event_type)
);

-- ============================================
-- DIMENSION TABLES (Star Schema)
-- ============================================

-- Dimension: Customer
CREATE TABLE dim_customer (
    customer_key INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(200),
    email VARCHAR(255),
    age INT,
    gender VARCHAR(20),
    registration_date DATE,
    customer_segment VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_customer_id (customer_id)
);

-- Dimension: Product
CREATE TABLE dim_product (
    product_key INT AUTO_INCREMENT PRIMARY KEY,
    product_id VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    price DECIMAL(10, 2),
    stock_quantity INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_product_id (product_id),
    INDEX idx_category (category)
);

-- Dimension: Date
CREATE TABLE dim_date (
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
);

-- Dimension: Location
CREATE TABLE dim_location (
    location_key INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20),
    region VARCHAR(100),
    UNIQUE KEY unique_location (city, state, country, postal_code),
    INDEX idx_country (country),
    INDEX idx_state (state)
);

-- ============================================
-- FACT TABLES (Star Schema)
-- ============================================

-- Fact: Sales
CREATE TABLE fact_sales (
    sale_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    date_key INT NOT NULL,
    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    location_key INT NOT NULL,
    order_id VARCHAR(50) NOT NULL,
    order_date DATETIME NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    shipping_cost DECIMAL(10, 2) DEFAULT 0,
    payment_method VARCHAR(50),
    delivery_date DATETIME,
    delivery_time_hours INT, -- Calculated: delivery_date - order_date
    order_status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (location_key) REFERENCES dim_location(location_key),
    INDEX idx_order_date (order_date),
    INDEX idx_date_key (date_key),
    INDEX idx_customer_key (customer_key),
    INDEX idx_product_key (product_key)
);

-- Fact: Cart Abandonment
CREATE TABLE fact_cart_abandonment (
    abandonment_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    date_key INT NOT NULL,
    customer_key INT,
    product_key INT NOT NULL,
    session_id VARCHAR(50),
    add_to_cart_time DATETIME NOT NULL,
    checkout_attempt_time DATETIME,
    abandonment_time DATETIME NOT NULL,
    time_to_abandonment_minutes INT, -- Calculated time
    cart_value DECIMAL(10, 2),
    items_count INT,
    device_type VARCHAR(20),
    browser VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    INDEX idx_date_key (date_key),
    INDEX idx_abandonment_time (abandonment_time)
);

-- ============================================
-- Populate Date Dimension (2020-2030)
-- Note: Date dimension is populated by Python script in mysql_setup.py
-- This ensures compatibility across all MySQL versions
-- ============================================

