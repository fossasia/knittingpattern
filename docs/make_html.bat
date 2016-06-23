@echo off

REM 
REM This is a shortcut for notepad++
REM You can press F5 and use this as command to update the html of the docs. 
REM 

cd "%~dp0"

REM call make html
call make coverage

py -c "print(open('../build/coverage/Python.txt').read())"

pause