@echo off

setlocal
cd /d "%~dp0"

rem - find python
where python >nul 2>&1
if errorlevel 1 (
  echo Python nie znaleziony w PATH. Zainstaluj Pythona lub uruchom z poprawnego środowiska.
  pause
  exit /b 1
)

rem - if venv does not exist, create it
if not exist "%~dp0venv\Scripts\activate.bat" (
  echo Tworzenie virtualenv w `venv`...
  python -m venv "%~dp0venv"
  if errorlevel 1 (
    echo Nie udało sie utworzyc virtualenv.
    pause
    exit /b 1
  )
)

rem - activate venv
call "%~dp0venv\Scripts\activate.bat"

rem - install dependencies from requirements.txt
if exist "%~dp0requirements.txt" (
  echo Instalacja zaleznosci z `requirements.txt`...
  pip install --upgrade pip
  pip install -r "%~dp0requirements.txt"
  if errorlevel 1 (
    echo Instalacja zaleznosci nie powiodla sie.
    pause
    exit /b 1
  )
) else (
  echo Brak pliku `requirements.txt` w katalogu.
)

rem - start API and Streamlit in separate cmd windows
echo Uruchamianie API...
start "API" cmd /k "%~dp0venv\Scripts\python.exe -m uvicorn app.api:app --host 127.0.0.1 --port 8008 --reload"

echo Uruchamianie Streamlit...
start "Streamlit" cmd /k ""%~dp0venv\Scripts\python.exe" -m streamlit run "%~dp0app\streamlit_app.py""

echo Aplikacje uruchomione. Zamknij okna `API` i `Streamlit` aby zatrzymac procesy.
pause


endlocal