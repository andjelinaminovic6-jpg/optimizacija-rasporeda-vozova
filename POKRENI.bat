@echo off
rem =====================================================================
rem  POKRENI.bat  —  DUPLI-KLIK ZA POKRETANJE (ne treba nijedan program)
rem  Ovaj fajl nadje Python na racunaru i pokrene POKRENI.py.
rem =====================================================================
chcp 65001 >nul
title Seminarski rad - pokretanje
rem Predji u folder u kome se ovaj .bat nalazi (radi i sa fleshke i sa Desktopa)
cd /d "%~dp0"

echo ============================================================
echo   Pokrecem seminarski rad. Sacekajte...
echo ============================================================
echo.

rem 1) Probaj Python preko "py" pokretaca (dolazi uz zvanicni Python sa python.org)
where py >nul 2>nul
if %errorlevel%==0 (
    py POKRENI.py
    goto kraj
)

rem 2) Ako nema "py", probaj komandu "python"
where python >nul 2>nul
if %errorlevel%==0 (
    python POKRENI.py
    goto kraj
)

rem 3) Python nije pronadjen — objasni sta da se uradi
echo.
echo ------------------------------------------------------------
echo   PYTHON NIJE PRONADJEN NA OVOM RACUNARU.
echo.
echo   1. Otvoricu ti stranicu za preuzimanje Python-a.
echo   2. Skini ga i instaliraj (VAZNO: u prvom prozoru instalacije
echo      cekiraj kvadratic "Add python.exe to PATH").
echo   3. Kada zavrsis, ponovo dupli-klik na ovaj fajl (POKRENI.bat).
echo.
echo   Detaljno uputstvo sa slikama je u PDF fajlu uz projekat.
echo ------------------------------------------------------------
echo.
start https://www.python.org/downloads/
goto kraj

:kraj
echo.
echo ============================================================
echo   Prozor mozes da zatvoris. Slike su u folderu "slike".
echo ============================================================
pause
