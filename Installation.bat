@echo OFF

python -V 2>NUL ( GOTO PYTHON_DOES_NOT_EXIST )

cls
echo "Python has already installed" 


GOTO End

:PYTHON_DOES_NOT_EXIST
set pythonVersion=3.8.2
IF EXIST "%PROGRAMFILES(X86)%" (
	GOTO B_64
) ELSE (
	GOTO B_32
)

:B_64
curl https://www.python.org/ftp/python/%pythonVersion%/python-%pythonVersion%-amd64.exe --output python64bit.exe
%CD%/python64bit.exe
del /Q /F %CD%\python64bit.exe
GOTO End

:B_32
curl https://www.python.org/ftp/python/%pythonVersion%/python-%pythonVersion%.exe --output python32bit.exe
%CD%/python32bit.exe
del /Q /F %CD%\python32bit.exe
GOTO End

:END
pip install selenium
pause


