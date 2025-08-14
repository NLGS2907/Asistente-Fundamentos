@echo off
set possible_ver= py python3.13 python3.12 python3.11 python3.10 python3 python
set pyupdate= -m pip install --upgrade -r requirements.txt
set pyargs= -m asistente

@REM debería de pararse en la carpeta raíz del proyecto
if %CD:~-3% == run (
    cd ..
)

for %%v in (%possible_ver%) do (
    echo: & echo: & echo Trying with '%%v'...& echo:
    %%v%pyupdate%%reqpath%
    %%v%pyargs%
    if not errorlevel 1 goto:EOF
)
