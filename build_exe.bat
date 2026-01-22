@echo off
REM Script para empaquetar la app en Windows usando PyInstaller
REM Ejecutar desde la carpeta del proyecto: build_exe.bat

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Empaqueta en un único ejecutable sin consola (quitar --noconsole si quieres ver la consola)
python -m PyInstaller --onefile --noconsole main.py

echo Empaquetado finalizado. Revisa la carpeta dist\
pause
