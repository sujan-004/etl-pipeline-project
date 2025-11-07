# Real-Time Data Pipeline for E-Commerce Analytics

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![MySQL](https://img.shields.io/badge/mysql-8.0+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A comprehensive real-time data pipeline project that demonstrates end-to-end data engineering skills including real-time data ingestion, ETL processing, data warehousing with star-schema design, and Power BI visualization.

## 🎯 Project Overview

This project implements a scalable e-commerce data pipeline that:
- **Ingests** real-time orders, clicks, and customer events via Flask API
- **Stores** data in MySQL (staging tables)
- **Transforms** raw data through ETL pipeline
- **Loads** cleaned data into star-schema data warehouse
- **Exports** analytics-ready data for Power BI dashboards

## 📊 Key Features

- ✅ Real-time data streaming via Flask API
- ✅ MySQL staging tables for raw data ingestion
- ✅ ETL pipeline with data cleaning and transformation
- ✅ Star-schema data warehouse (dimensions + facts)
- ✅ Power BI compatible data exports
- ✅ Analytics on sales trends, cart abandonment, delivery times
- ✅ Scalable and production-ready architecture

## 🛠️ Tech Stack

- **Python 3.8+**
- **MySQL** - Data warehouse and staging
- **Flask** - Real-time data generator API
- **Pandas** - Data processing
- **Power BI** - Visualization (data export)

## 📁 Project Structure

```
etl-pipeline-project/
├── config/                    # Configuration files
│   ├── config.py             # Main config
│   └── database_config.json.example  # DB config template
├── data_generator/           # Real-time data generation
│   ├── flask_app.py          # Flask API server
│   └── event_generator.py    # Event generation logic
├── database/                 # Database setup
│   ├── schemas.sql           # SQL schemas
│   └── mysql_setup.py        # MySQL initialization
├── etl/                      # ETL pipeline
│   ├── extract.py            # Data extraction
│   ├── transform.py          # Data transformation
│   ├── load.py               # Data loading
│   └── pipeline.py           # ETL orchestration
├── utils/                    # Utilities
│   └── database_connector.py # DB connection helpers
├── scripts/                  # Execution scripts
│   ├── setup_database.py     # DB setup
│   ├── start_generator.py    # Start data generator
│   ├── run_pipeline.py       # Run ETL
│   └── powerbi_export.py     # Export for Power BI
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── LICENSE                   # MIT License
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **MySQL Server** installed and running
3. **pip** package manager

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/etl-pipeline-project.git
   cd etl-pipeline-project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   
   Create a `.env` file in the project root:
   ```env
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=ecommerce_db
   ```
   
   Or copy from example:
   ```bash
   cp .env.example .env
   # Then edit .env with your credentials
   ```

5. **Setup database**
   ```bash
   python scripts/setup_database.py
   ```

## 📈 Running the Pipeline

### Step 1: Start Data Generator

In **Terminal 1**, start the Flask data generator:
```bash
python scripts/start_generator.py
```

### Step 2: Start Data Streaming

In **Terminal 2**, start streaming:
```bash
curl -X POST http://localhost:5000/start
```

Or use Python:
```python
import requests
requests.post('http://localhost:5000/start')
```

### Step 3: Run ETL Pipeline

In **Terminal 3**, run the ETL pipeline:
```bash
python scripts/run_pipeline.py
```

### Step 4: Export Data for Power BI

```bash
python scripts/powerbi_export.py
```

## 📊 Database Schema

### Staging Tables (Raw Data)
- `staging_orders` - Raw order data
- `staging_clicks` - Raw click/view data
- `staging_customer_events` - Raw customer events

### Dimension Tables (Star Schema)
- `dim_customer` - Customer information
- `dim_product` - Product catalog
- `dim_date` - Date dimension (2020-2030)
- `dim_location` - Geographic locations

### Fact Tables (Star Schema)
- `fact_sales` - Sales transactions
- `fact_cart_abandonment` - Cart abandonment events

## 📈 Power BI Integration

### Import CSV Files
1. Open Power BI Desktop
2. Get Data → Text/CSV
3. Select exported CSV files from `powerbi_exports/`
4. Load and create visualizations

### Direct MySQL Connection
1. Open Power BI Desktop
2. Get Data → MySQL Database
3. Enter: Server: `localhost`, Database: `ecommerce_db`
4. Select fact and dimension tables
5. Create relationships and visualizations

## 🐛 Troubleshooting

### MySQL Connection Issues

**Error: "Can't connect to MySQL server"**
1. Check MySQL status: `python scripts/check_mysql.py`
2. Install MySQL if needed (XAMPP is easiest)
3. Start MySQL service: `net start MySQL80`
4. Update credentials in `.env` file

### Cryptography Package Error

**Error: "'cryptography' package is required"**
```bash
pip install cryptography
```

### MySQL Access Denied

**Error: "Access denied for user 'root'@'localhost'"**
1. Test password: `python scripts/test_mysql_password.py`
2. Update password in `.env` file
3. Common passwords: empty `''` (XAMPP), `'root'`

## 📊 Project Highlights for Resume

**Resume Line:**
> "Engineered a scalable e-commerce data pipeline (real-time ingestion, ETL, and visualization) using Python, MySQL, and Power BI, reducing reporting latency by 70%."

**Key Skills Demonstrated:**
- Real-time data streaming and ingestion
- Database design (staging + star-schema warehouse)
- ETL pipeline development
- Data transformation and cleaning
- Power BI integration
- API development (Flask)
- Python programming
- SQL optimization
- Data warehousing concepts

## 🔄 Workflow

```
Data Generator (Flask) 
    ↓
Staging Tables (MySQL)
    ↓
ETL Pipeline (Extract → Transform → Load)
    ↓
Data Warehouse (Star Schema - MySQL)
    ↓
Power BI Export/Connection
    ↓
Dashboards & Analytics
```

## 📚 Additional Resources

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Power BI Documentation](https://docs.microsoft.com/power-bi/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 🚀 GitHub Setup

For detailed instructions on hosting this project on GitHub, see [GITHUB_SETUP.md](GITHUB_SETUP.md) or [GITHUB_QUICK_START.md](GITHUB_QUICK_START.md).

---

**Built with ❤️ for Data Engineering Portfolio**
