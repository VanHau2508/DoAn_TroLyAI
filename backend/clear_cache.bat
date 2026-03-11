@echo off
echo Clearing Python cache...
rmdir /s /q app\__pycache__ 2>nul
rmdir /s /q app\config\__pycache__ 2>nul
rmdir /s /q app\models\__pycache__ 2>nul
rmdir /s /q app\controllers\__pycache__ 2>nul
rmdir /s /q app\routes\__pycache__ 2>nul
rmdir /s /q app\utils\__pycache__ 2>nul
del /s /q *.pyc 2>nul
echo Cache cleared!