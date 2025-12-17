# MongoDB Status Checker Script
Write-Host "=== MongoDB Status Checker ===" -ForegroundColor Cyan
Write-Host ""

# 1. Check if mongod.exe exists in common installation paths
Write-Host "1. Checking if MongoDB is installed..." -ForegroundColor Yellow
$mongodPaths = @(
    "C:\Program Files\MongoDB\Server\*\bin\mongod.exe",
    "C:\mongodb\bin\mongod.exe",
    "$env:ProgramFiles\MongoDB\Server\*\bin\mongod.exe",
    "$env:LOCALAPPDATA\Programs\MongoDB\*\bin\mongod.exe"
)

$mongodFound = $false
$mongodPath = $null

foreach ($path in $mongodPaths) {
    $found = Get-ChildItem -Path $path -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($found) {
        $mongodPath = $found.FullName
        $mongodFound = $true
        Write-Host "   ✓ MongoDB found at: $mongodPath" -ForegroundColor Green
        break
    }
}

if (-not $mongodFound) {
    Write-Host "   ✗ MongoDB not found in common installation paths" -ForegroundColor Red
    Write-Host "   You may need to install MongoDB or add it to your PATH" -ForegroundColor Yellow
}

Write-Host ""

# 2. Check if MongoDB service is running
Write-Host "2. Checking if MongoDB service is running..." -ForegroundColor Yellow
$mongoService = Get-Service -Name "MongoDB" -ErrorAction SilentlyContinue

if ($mongoService) {
    if ($mongoService.Status -eq "Running") {
        Write-Host "   ✓ MongoDB service is RUNNING" -ForegroundColor Green
        Write-Host "   Service Status: $($mongoService.Status)" -ForegroundColor Green
    } else {
        Write-Host "   ✗ MongoDB service is NOT running" -ForegroundColor Red
        Write-Host "   Service Status: $($mongoService.Status)" -ForegroundColor Yellow
        Write-Host "   To start it, run: Start-Service MongoDB" -ForegroundColor Cyan
    }
} else {
    Write-Host "   ⚠ MongoDB service not found (may be running as a standalone process)" -ForegroundColor Yellow
}

Write-Host ""

# 3. Check if MongoDB is listening on port 27017
Write-Host "3. Checking if MongoDB is listening on port 27017..." -ForegroundColor Yellow
$port27017 = Get-NetTCPConnection -LocalPort 27017 -ErrorAction SilentlyContinue

if ($port27017) {
    Write-Host "   ✓ Port 27017 is in use (MongoDB may be running)" -ForegroundColor Green
    Write-Host "   Process ID: $($port27017.OwningProcess)" -ForegroundColor Cyan
    $process = Get-Process -Id $port27017.OwningProcess -ErrorAction SilentlyContinue
    if ($process) {
        Write-Host "   Process Name: $($process.ProcessName)" -ForegroundColor Cyan
    }
} else {
    Write-Host "   ✗ Port 27017 is not in use (MongoDB is likely not running)" -ForegroundColor Red
}

Write-Host ""

# 4. Try to connect to MongoDB using mongo shell (if available)
Write-Host "4. Testing MongoDB connection..." -ForegroundColor Yellow
try {
    $mongoClient = New-Object System.Net.Sockets.TcpClient
    $mongoClient.Connect("localhost", 27017)
    $mongoClient.Close()
    Write-Host "   ✓ Successfully connected to MongoDB on localhost:27017" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Cannot connect to MongoDB on localhost:27017" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""

# 5. Check PATH environment variable
Write-Host "5. Checking if MongoDB is in PATH..." -ForegroundColor Yellow
$pathEnv = $env:PATH -split ';'
$mongoInPath = $pathEnv | Where-Object { $_ -like "*MongoDB*" -or $_ -like "*mongodb*" }

if ($mongoInPath) {
    Write-Host "   ✓ MongoDB found in PATH:" -ForegroundColor Green
    $mongoInPath | ForEach-Object { Write-Host "     $_" -ForegroundColor Cyan }
} else {
    Write-Host "   ✗ MongoDB not found in PATH" -ForegroundColor Red
    if ($mongodPath) {
        Write-Host "   To add MongoDB to PATH, run:" -ForegroundColor Yellow
        $mongoBinPath = Split-Path -Parent $mongodPath
        Write-Host "   `$env:PATH += `";$mongoBinPath`"" -ForegroundColor Cyan
    }
}

Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Cyan
Write-Host ""

# Provide recommendations
if ($mongodFound -and $mongoService -and $mongoService.Status -eq "Running") {
    Write-Host "✓ MongoDB appears to be installed and running!" -ForegroundColor Green
} elseif ($mongodFound -and -not $mongoService) {
    Write-Host "⚠ MongoDB is installed but service is not configured." -ForegroundColor Yellow
    Write-Host "  You can start MongoDB manually using:" -ForegroundColor Cyan
    Write-Host "  & `"$mongodPath`" --dbpath `"C:\data\db`"" -ForegroundColor White
} elseif ($mongodFound -and $mongoService -and $mongoService.Status -ne "Running") {
    Write-Host "⚠ MongoDB is installed but not running." -ForegroundColor Yellow
    Write-Host "  Start it with: Start-Service MongoDB" -ForegroundColor Cyan
} else {
    Write-Host "✗ MongoDB may not be installed or not found." -ForegroundColor Red
    Write-Host "  Install from: https://www.mongodb.com/try/download/community" -ForegroundColor Cyan
    Write-Host "  Or use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas" -ForegroundColor Cyan
}

