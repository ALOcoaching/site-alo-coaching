@echo off
REM ============================================================
REM  Tests ALO Coaching - Non-régression & IHM
REM  Usage :
REM    test-site.bat                   (teste la prod Netlify)
REM    test-site.bat http://localhost:8000  (teste en local)
REM ============================================================

set BASE_URL=%1
if "%BASE_URL%"=="" set BASE_URL=https://aloformationcoaching.netlify.app

echo.
echo ====================================
echo  ALO Coaching - Tests automatises
echo  URL : %BASE_URL%
echo ====================================
echo.

cd /d "%~dp0"
call "%~dp0..\.venv\Scripts\activate.bat" 2>nul

pytest tests/ --base-url=%BASE_URL% -v --tb=short %2 %3 %4

echo.
if %ERRORLEVEL%==0 (
    echo [OK] Tous les tests sont passes !
) else (
    echo [ECHEC] Des tests ont echoue - voir ci-dessus
)
pause
