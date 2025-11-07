# Where to Execute Commands

## 📍 Command Execution Locations

### For Installing Dependencies (Local Setup)

**Location:** PowerShell in your project folder

```powershell
# 1. Open PowerShell
# 2. Navigate to project directory
cd "C:\Users\ACER\OneDrive\Desktop\etl pipeline project"

# 3. Activate virtual environment (if you have one)
.venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**Where:** On your local computer, in the project folder

---

### For GitHub Upload (Local Computer)

**Location:** PowerShell in your project folder

```powershell
# 1. Open PowerShell
# 2. Navigate to project directory
cd "C:\Users\ACER\OneDrive\Desktop\etl pipeline project"

# 3. Run git commands
git add .
git commit -m "Initial commit: ETL Pipeline Project"
git remote add origin https://github.com/YOUR_USERNAME/etl-pipeline-project.git
git branch -M main
git push -u origin main
```

**Where:** On your local computer, in the project folder

---

### For Running the Project (Local Computer)

**Terminal 1 - Data Generator:**
```powershell
cd "C:\Users\ACER\OneDrive\Desktop\etl pipeline project"
.venv\Scripts\Activate.ps1
python scripts/start_generator.py
```

**Terminal 2 - Start Streaming:**
```powershell
cd "C:\Users\ACER\OneDrive\Desktop\etl pipeline project"
curl -X POST http://localhost:5000/start
```

**Terminal 3 - ETL Pipeline:**
```powershell
cd "C:\Users\ACER\OneDrive\Desktop\etl pipeline project"
.venv\Scripts\Activate.ps1
python scripts/run_pipeline.py
```

**Where:** On your local computer, in separate PowerShell windows

---

## 🖥️ Step-by-Step: Where to Run Each Command

### Step 1: Install Dependencies (LOCAL)

**Open:** PowerShell on your Windows computer

**Navigate to:**
```
C:\Users\ACER\OneDrive\Desktop\etl pipeline project
```

**Run:**
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 2: Upload to GitHub (LOCAL)

**Open:** PowerShell on your Windows computer

**Navigate to:**
```
C:\Users\ACER\OneDrive\Desktop\etl pipeline project
```

**Run:**
```powershell
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/etl-pipeline-project.git
git push -u origin main
```

---

### Step 3: After GitHub Upload (GitHub will auto-install)

**GitHub Actions** will automatically:
- Install dependencies when you push code
- Run tests (if configured)
- You don't need to do anything on GitHub!

**For others cloning your repo:**
They will run commands on THEIR local computer:
```bash
git clone https://github.com/YOUR_USERNAME/etl-pipeline-project.git
cd etl-pipeline-project
pip install -r requirements.txt
```

---

## 🎯 Quick Reference

| Task | Where to Run | Command |
|------|--------------|---------|
| Install dependencies | **Local PowerShell** (project folder) | `pip install -r requirements.txt` |
| Upload to GitHub | **Local PowerShell** (project folder) | `git push -u origin main` |
| Run data generator | **Local PowerShell** (project folder) | `python scripts/start_generator.py` |
| Run ETL pipeline | **Local PowerShell** (project folder) | `python scripts/run_pipeline.py` |
| Clone repository | **Any computer** (where you want to clone) | `git clone https://github.com/...` |

---

## 💡 Visual Guide

```
YOUR COMPUTER (Local)
├── PowerShell Terminal
│   ├── Install dependencies: pip install -r requirements.txt
│   ├── Run project: python scripts/start_generator.py
│   └── Upload to GitHub: git push
│
└── Project Folder
    └── etl-pipeline-project/
        ├── requirements.txt
        ├── scripts/
        └── ...


GITHUB (Remote)
└── Your Repository
    ├── GitHub automatically runs CI/CD
    └── Others can clone and run locally
```

---

## 🚀 Most Common: Install Dependencies

**Right now, you need to:**

1. **Open PowerShell**
2. **Navigate to project:**
   ```powershell
   cd "C:\Users\ACER\OneDrive\Desktop\etl pipeline project"
   ```

3. **Activate virtual environment (if exists):**
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. **Install:**
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

That's it! All commands run in PowerShell on your local computer. 🎯

