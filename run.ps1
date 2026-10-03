$ErrorActionPreference = "Stop"

Write-Host "Starting CyberShield API and Dashboard..." -ForegroundColor Green

# Start FastAPI server in the background
Start-Process -FilePath ".\venv\Scripts\uvicorn.exe" -ArgumentList "backend.main:app", "--reload", "--port", "8000" -NoNewWindow

# Wait for API to start
Start-Sleep -Seconds 3

# Start Streamlit dashboard
.\venv\Scripts\streamlit.exe run dashboard\app.py
