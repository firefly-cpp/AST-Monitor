@echo off

pyuic6 "-o" "mainwindow.py" "uis\GUI2.ui"
move "mainwindow.py" "%CD%\..\ast_monitor"