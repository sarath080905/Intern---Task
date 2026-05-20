$port = $env:PORT
if (-not $port) {
    $port = 8000
}
Write-Host "Starting backend on port $port"
python -m uvicorn main:app --host 0.0.0.0 --port $port
