"""
Prepare project for GitHub upload
Checks for sensitive data and ensures all necessary files are ready
"""
import os
import sys

def check_sensitive_data():
    """Check for sensitive data in files"""
    issues = []
    
    # Check config.py for hardcoded passwords
    config_path = os.path.join('config', 'config.py')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            content = f.read()
            if 'Bossmom1986' in content or 'root' in content.lower():
                # Check if it's just in comments or example
                if "'password': os.getenv('MYSQL_PASSWORD', " in content:
                    # Check default value
                    if "'root')" in content or "'Bossmom" in content:
                        issues.append("⚠️  Hardcoded password found in config.py default value")
    
    # Check database_config.json
    db_config_path = os.path.join('config', 'database_config.json')
    if os.path.exists(db_config_path):
        with open(db_config_path, 'r') as f:
            content = f.read()
            if 'root' not in content or 'your_password' not in content:
                if 'Bossmom' in content or (len(content) > 0 and '"password": "root"' not in content and '"password": "your_password_here"' not in content):
                    issues.append("⚠️  Real password might be in database_config.json")
    
    # Check for .env file
    if os.path.exists('.env'):
        issues.append("⚠️  .env file exists (should be in .gitignore)")
    
    return issues

def check_required_files():
    """Check if all required files exist"""
    required = [
        'README.md',
        'requirements.txt',
        '.gitignore',
        '.env.example',
        'config/database_config.json.example',
        'LICENSE',
        'CONTRIBUTING.md'
    ]
    
    missing = []
    for file in required:
        if not os.path.exists(file):
            missing.append(file)
    
    return missing

def main():
    """Main function"""
    import sys
    import io
    
    # Fix encoding for Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 70)
    print("GitHub Preparation Checklist")
    print("=" * 70)
    print()
    
    # Check sensitive data
    print("1. Checking for sensitive data...")
    issues = check_sensitive_data()
    if issues:
        for issue in issues:
            print(f"   {issue}")
    else:
        print("   [OK] No sensitive data found in code")
    print()
    
    # Check required files
    print("2. Checking required files...")
    missing = check_required_files()
    if missing:
        print("   [X] Missing files:")
        for file in missing:
            print(f"      - {file}")
    else:
        print("   [OK] All required files present")
    print()
    
    # Check .gitignore
    print("3. Checking .gitignore...")
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r', encoding='utf-8') as f:
            content = f.read()
            if '.env' in content and 'database_config.json' in content:
                print("   [OK] .gitignore properly configured")
            else:
                print("   [WARNING] .gitignore might be missing some entries")
    else:
        print("   [X] .gitignore file not found!")
    print()
    
    # Summary
    print("=" * 70)
    if not issues and not missing:
        print("[OK] Project is ready for GitHub!")
        print()
        print("Next steps:")
        print("1. git add .")
        print("2. git commit -m 'Initial commit: ETL Pipeline Project'")
        print("3. git remote add origin https://github.com/YOUR_USERNAME/repo-name.git")
        print("4. git push -u origin main")
    else:
        print("[WARNING] Please fix the issues above before pushing to GitHub")
    print("=" * 70)

if __name__ == "__main__":
    main()

