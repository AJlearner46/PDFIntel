# MongoDB Status Check Commands

## Quick Commands to Check MongoDB Status

### 1. Check if MongoDB is installed
```powershell
# Check if mongod.exe exists
Get-Command mongod -ErrorAction SilentlyContinue

# Or check common installation paths
Test-Path "C:\Program Files\MongoDB\Server\*\bin\mongod.exe"
```

### 2. Check if MongoDB service is running
```powershell
# Check MongoDB Windows service
Get-Service MongoDB -ErrorAction SilentlyContinue

# If service exists, check its status
$service = Get-Service MongoDB -ErrorAction SilentlyContinue
if ($service) { $service.Status }
```

### 3. Check if MongoDB is listening on port 27017
```powershell
# Check if port 27017 is in use
Get-NetTCPConnection -LocalPort 27017 -ErrorAction SilentlyContinue

# Or use netstat
netstat -an | findstr :27017
```

### 4. Test MongoDB connection
```powershell
# Try to connect to MongoDB
$tcpClient = New-Object System.Net.Sockets.TcpClient
try {
    $tcpClient.Connect("localhost", 27017)
    Write-Host "MongoDB is running!"
    $tcpClient.Close()
} catch {
    Write-Host "MongoDB is not running: $($_.Exception.Message)"
}
```

### 5. Check MongoDB in PATH
```powershell
# Check if MongoDB is in your PATH
$env:PATH -split ';' | Where-Object { $_ -like "*MongoDB*" }
```

## Solutions

### Option 1: Install MongoDB Community Edition
1. Download from: https://www.mongodb.com/try/download/community
2. Run the installer
3. Choose "Complete" installation
4. Install as a Windows Service (recommended)
5. MongoDB will start automatically after installation

### Option 2: Use MongoDB Atlas (Cloud - Recommended for Development)
1. Sign up at: https://www.mongodb.com/cloud/atlas
2. Create a free cluster
3. Get your connection string
4. Update your `.env` file with the connection string:
   ```
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/ragapp
   ```

### Option 3: Install MongoDB via Chocolatey (if you have it)
```powershell
choco install mongodb
```

### Option 4: Run MongoDB manually (if installed but not in PATH)
```powershell
# Find MongoDB installation
$mongoPath = Get-ChildItem "C:\Program Files\MongoDB" -Recurse -Filter "mongod.exe" | Select-Object -First 1

# Create data directory
New-Item -ItemType Directory -Force -Path "C:\data\db"

# Start MongoDB manually
& $mongoPath.FullName --dbpath "C:\data\db"
```

## After Installation

### Start MongoDB Service (if installed as service)
```powershell
Start-Service MongoDB
```

### Stop MongoDB Service
```powershell
Stop-Service MongoDB
```

### Check MongoDB Status
```powershell
Get-Service MongoDB
```

## For Your Project

Since your project uses `MONGO_URI` from environment variables, you can:

1. **Use MongoDB Atlas (Easiest)**: 
   - No local installation needed
   - Free tier available
   - Just update your `.env` file

2. **Install MongoDB Locally**:
   - Install MongoDB Community Edition
   - Default connection: `mongodb://localhost:27017`
   - Update `.env`: `MONGO_URI=mongodb://localhost:27017`

