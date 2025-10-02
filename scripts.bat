@echo off
REM Scripts para SoportePlus Backend

if "%1"=="dev" (
    echo 🚀 Iniciando servidor de desarrollo...
    call .\venv\Scripts\Activate.ps1
    flask run --debug
) else if "%1"=="start" (
    echo 🚀 Iniciando servidor...
    call .\venv\Scripts\Activate.ps1
    python run.py
) else if "%1"=="test" (
    echo 🧪 Ejecutando tests...
    call .\venv\Scripts\Activate.ps1
    pytest
) else if "%1"=="format" (
    echo 🎨 Formateando código...
    call .\venv\Scripts\Activate.ps1
    black .
) else (
    echo ❌ Comando no reconocido
    echo 💡 Comandos disponibles:
    echo    scripts dev     - Servidor de desarrollo
    echo    scripts start   - Servidor normal
    echo    scripts test    - Ejecutar tests
    echo    scripts format  - Formatear código
)