# Setup Instructions for GitHub Repository

## 🚀 Quick Setup (After Cloning from GitHub)

### Step 1: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/etl-pipeline-project.git
cd etl-pipeline-project
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy example file
cp .env.example .env

# Edit .env file with your MySQL credentials
# Or edit config/config.py directly
```

### Step 5: Setup Database
```bash
python scripts/setup_database.py
```

### Step 6: Run the Project
```bash
# Terminal 1: Start data generator
python scripts/start_generator.py

# Terminal 2: Start streaming
curl -X POST http://localhost:5000/start

# Terminal 3: Run ETL pipeline
python scripts/run_pipeline.py
```

## 📋 Configuration Files

- `.env.example` - Template for environment variables (copy to `.env`)
- `config/database_config.json.example` - Template for database config
- `config/config.py` - Main configuration (uses environment variables)

## 🔒 Security Notes

- Never commit `.env` file (already in .gitignore)
- Never commit `config/database_config.json` with real password (already in .gitignore)
- Use environment variables for sensitive data
- Update `.env.example` with placeholder values

## ✅ Verification

Run the preparation script to verify everything is ready:
```bash
python scripts/prepare_for_github.py
```

