@REM RMDIR /S /Q build
@REM RMDIR /S /Q dist
pyinstaller punch.py --onedir --noconfirm
RM punch.spec