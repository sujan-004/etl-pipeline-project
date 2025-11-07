# PowerShell script to add MySQL to PATH temporarily or help with permanent setup

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "MySQL PATH Configuration Helper" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Common MySQL paths
$mysqlPaths = @(
    "C:\xampp\mysql\bin",
    "C:\Program Files\MySQL\MySQL Server 8.0\bin",
    "C:\Program Files\MySQL\MySQL Server 8.1\bin",
    "C:\Program Files\MySQL\MySQL Server 5.7\bin",
    "C:\wamp\bin\mysql\mysql8.0.xx\bin",
    "C:\wamp64\bin\mysql\mysql8.0.xx\bin"
)

Write-Host "Searching for MySQL installation..." -ForegroundColor Yellow

$foundPaths = @()
foreach ($path in $mysqlPaths) {
    if (Test-Path $path) {
        $mysqlExe = Join-Path $path "mysql.exe"
        if (Test-Path $mysqlExe) {
            $foundPaths += $path
            Write-Host "  [OK] Found MySQL at: $path" -ForegroundColor Green
        }
    }
}

# Check Program Files
$programFilesPaths = @(
    $env:ProgramFiles,
    ${env:ProgramFiles(x86)}
)

foreach ($pf in $programFilesPaths) {
    $mysqlBase = Join-Path $pf "MySQL"
    if (Test-Path $mysqlBase) {
        Write-Host "  [OK] Found MySQL directory at: $mysqlBase" -ForegroundColor Green
        $subdirs = Get-ChildItem $mysqlBase -Directory -ErrorAction SilentlyContinue
        foreach ($subdir in $subdirs) {
            $binPath = Join-Path $subdir.FullName "bin"
            if (Test-Path $binPath) {
                $mysqlExe = Join-Path $binPath "mysql.exe"
                if (Test-Path $mysqlExe) {
                    if ($binPath -notin $foundPaths) {
                        $foundPaths += $binPath
                        Write-Host "  [OK] Found MySQL at: $binPath" -ForegroundColor Green
                    }
                }
            }
        }
    }
}

if ($foundPaths.Count -eq 0) {
    Write-Host ""
    Write-Host "  [X] MySQL not found in common locations" -ForegroundColor Red
    Write-Host ""
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host "SOLUTION: Install MySQL" -ForegroundColor Yellow
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Option 1 - XAMPP (Easiest):" -ForegroundColor White
    Write-Host "  1. Download from: https://www.apachefriends.org/" -ForegroundColor Gray
    Write-Host "  2. Install XAMPP"
    Write-Host "  3. Open XAMPP Control Panel"
    Write-Host "  4. Click 'Start' next to MySQL"
    Write-Host ""
    Write-Host "Option 2 - MySQL Installer:" -ForegroundColor White
    Write-Host "  1. Download from: https://dev.mysql.com/downloads/installer/" -ForegroundColor Gray
    Write-Host "  2. Install MySQL Server"
    Write-Host ""
    exit
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "MySQL Found! Choose an option:" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Use first found path
$mysqlPath = $foundPaths[0]
Write-Host "Using MySQL path: $mysqlPath" -ForegroundColor Cyan
Write-Host ""

Write-Host "Option 1: Add to PATH for current PowerShell session" -ForegroundColor Yellow
Write-Host "  Run this command:" -ForegroundColor White
Write-Host "  `$env:Path += `";$mysqlPath`"" -ForegroundColor Green
Write-Host ""

Write-Host "Option 2: Use full path (no PATH modification needed)" -ForegroundColor Yellow
Write-Host "  Run this command:" -ForegroundColor White
Write-Host "  & `"$mysqlPath\mysql.exe`" -u root -p" -ForegroundColor Green
Write-Host ""

Write-Host "Option 3: Add to PATH permanently (requires Admin)" -ForegroundColor Yellow
Write-Host "  Run this command (as Administrator):" -ForegroundColor White
Write-Host "  [Environment]::SetEnvironmentVariable(`"Path`", `$env:Path + `";$mysqlPath`", [EnvironmentVariableTarget]::Machine)" -ForegroundColor Green
Write-Host ""

Write-Host "=" * 70 -ForegroundColor Cyan

# Ask if user wants to add to PATH for current session
Write-Host ""
$response = Read-Host "Add MySQL to PATH for current PowerShell session? (Y/N)"
if ($response -eq 'Y' -or $response -eq 'y') {
    $env:Path += ";$mysqlPath"
    Write-Host ""
    Write-Host "[OK] MySQL added to PATH for this session!" -ForegroundColor Green
    Write-Host "You can now use: mysql -u root -p" -ForegroundColor Green
    Write-Host ""
    
    # Test
    Write-Host "Testing MySQL command..." -ForegroundColor Yellow
    $mysqlExe = Join-Path $mysqlPath "mysql.exe"
    if (Test-Path $mysqlExe) {
        & $mysqlExe --version
        Write-Host ""
        Write-Host "[OK] MySQL is working!" -ForegroundColor Green
    }
}

