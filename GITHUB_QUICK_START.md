# GitHub Quick Start Guide

## 🚀 Upload Your Project to GitHub in 5 Steps

### Step 1: Create GitHub Repository

1. Go to https://github.com
2. Click **"New repository"**
3. Name: `etl-pipeline-project`
4. Description: `Real-Time E-Commerce Data Pipeline - ETL with MySQL and Power BI`
5. Choose **Public** (for portfolio) or **Private**
6. **DO NOT** check "Add README" (we already have one)
7. Click **"Create repository"**

### Step 2: Prepare Project (Already Done!)

✅ Password removed from code
✅ .env.example created
✅ .gitignore configured
✅ All files ready

### Step 3: Initialize Git and Commit

```powershell
# In your project directory
git init
git add .
git commit -m "Initial commit: Real-Time ETL Pipeline for E-Commerce Analytics"
```

### Step 4: Connect to GitHub

```powershell
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/etl-pipeline-project.git
git branch -M main
```

### Step 5: Push to GitHub

```powershell
git push -u origin main
```

**If authentication fails:**
- Use Personal Access Token (GitHub Settings → Developer settings → Personal access tokens)
- Or use SSH keys

## ✅ Done!

Your project is now on GitHub at:
`https://github.com/YOUR_USERNAME/etl-pipeline-project`

## 📋 What's Included

✅ All source code
✅ Database schemas
✅ Documentation (README, LICENSE, CONTRIBUTING)
✅ Configuration templates
✅ Setup scripts

❌ Excluded (sensitive):
- .env files
- config/database_config.json (with real passwords)
- venv/ folder
- Generated files

## 🎯 Next Steps

1. Add repository topics (etl, data-pipeline, python, mysql)
2. Add repository description
3. Share on LinkedIn/portfolio
4. Star your own repo! ⭐

See [GITHUB_SETUP.md](GITHUB_SETUP.md) for detailed instructions.

