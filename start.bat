@echo off
echo Starting ATS Checker V2...

start "ATS Backend" cmd /k "cd backend && ..\venv\Scripts\python.exe app.py"

timeout /t 3 >nul

start "ATS Frontend" cmd /k "cd frontend && npm run dev"

echo Done! Both backend and frontend servers are launching.
pause