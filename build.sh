# Remove the build and dist directories
# rm -rf build
# rm -rf dist

# Run pyinstaller to package the punch.py script
<<<<<<< HEAD
/Library/Frameworks/Python.framework/Versions/Current/bin/pyinstaller punch.py --onedir --noconfirm
=======
pyinstaller punch.py --onedir --noconfirm
>>>>>>> 4f40ad7 (Create build script for shell)

# Remove the generated punch.spec file
rm punch.spec
