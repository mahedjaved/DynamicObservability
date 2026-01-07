# Check if podman is installed
if (-not (Get-Command podman -ErrorAction SilentlyContinue)) {
    Write-Host "Podman not found. Please ensure Podman is installed and in your PATH." -ForegroundColor Red
    exit 1
}

Write-Host "Starting Demo Containers..." -ForegroundColor Cyan

# Start Nginx
Write-Host "Starting Nginx..."
podman run -d --name dynobs-nginx -p 8081:80 nginx:alpine

# Start Redis
Write-Host "Starting Redis..."
podman run -d --name dynobs-redis -p 6379:6379 redis:alpine

# Start a loop container
Write-Host "Starting Alpine Loop..."
podman run -d --name dynobs-alpine alpine /bin/sh -c "while true; do echo 'DynObs Log Entry: ' $(date); sleep 5; done"

Write-Host "------------------------------------------------"
Write-Host "Containers started!" -ForegroundColor Green
Write-Host "1. dynobs-nginx"
Write-Host "2. dynobs-redis"
Write-Host "3. dynobs-alpine"
Write-Host "------------------------------------------------"
Write-Host "IMPORTANT: Configure Backend Connection" -ForegroundColor Yellow
Write-Host "For the Java backend to see these containers, run this in your PowerShell before starting the app:"
Write-Host '$env:DOCKER_HOST="npipe:////./pipe/podman-machine-default"' -ForegroundColor Green
Write-Host "Then run:"
Write-Host "cd app"
Write-Host "mvn spring-boot:run"
