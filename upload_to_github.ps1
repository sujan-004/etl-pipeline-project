# PowerShell script to upload project to GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub Upload Helper" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path .git)) {
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
}

# Check current status
Write-Host "Checking git status..." -ForegroundColor Yellow
git status --short

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Ready to upload to GitHub!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Follow these steps:" -ForegroundColor White
Write-Host ""
Write-Host "1. Create repository on GitHub:" -ForegroundColor Yellow
Write-Host "   - Go to https://github.com" -ForegroundColor Gray
Write-Host "   - Click 'New repository'" -ForegroundColor Gray
Write-Host "   - Name: etl-pipeline-project" -ForegroundColor Gray
Write-Host "   - Choose Public (for portfolio)" -ForegroundColor Gray
Write-Host "   - DO NOT check 'Add README'" -ForegroundColor Gray
Write-Host ""

Write-Host "2. Run these commands:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   git add ." -ForegroundColor Green
Write-Host "   git commit -m 'Initial commit: ETL Pipeline Project'" -ForegroundColor Green
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/etl-pipeline-project.git" -ForegroundColor Green
Write-Host "   git branch -M main" -ForegroundColor Green
Write-Host "   git push -u origin main" -ForegroundColor Green
Write-Host ""

Write-Host "3. If authentication fails:" -ForegroundColor Yellow
Write-Host "   - Use Personal Access Token (not password)" -ForegroundColor Gray
Write-Host "   - GitHub Settings > Developer settings > Personal access tokens" -ForegroundColor Gray
Write-Host ""

$continue = Read-Host "Do you want to run 'git add .' now? (Y/N)"
if ($continue -eq 'Y' -or $continue -eq 'y') {
    Write-Host ""
    Write-Host "Adding all files..." -ForegroundColor Yellow
    git add .
    Write-Host "Files added!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next: Run 'git commit -m \"Initial commit\"'" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "For detailed instructions, see:" -ForegroundColor White
Write-Host "  - UPLOAD_TO_GITHUB.md (Quick guide)" -ForegroundColor Cyan
Write-Host "  - GITHUB_SETUP.md (Detailed guide)" -ForegroundColor Cyan
Write-Host ""

