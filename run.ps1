param(
    [switch]$NoSimulator
)
$ErrorActionPreference = "Stop"

Write-Host "Starting CyberShield API and Dashboard..." -ForegroundColor Green
Set-Location $PSScriptRoot

# Start FastAPI server in the background
Start-Process -FilePath ".\venv\Scripts\uvicorn.exe" -ArgumentList "backend.main:app", "--reload", "--port", "8000" -NoNewWindow

# Wait for API to start
Start-Sleep -Seconds 3

if (-not $NoSimulator) {
    Write-Host "Starting security event simulator..." -ForegroundColor Green
    Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "simulator\event_generator.py" -WorkingDirectory $PSScriptRoot -NoNewWindow
}

# Start Streamlit dashboard
.\venv\Scripts\streamlit.exe run dashboard\app.py
