# Remove the build and dist directories
# rm -rf build
# rm -rf dist

# Run pyinstaller to package the punch.py script
/Library/Frameworks/Python.framework/Versions/Current/bin/pyinstaller punch.py --onedir --noconfirm

# Remove the generated punch.spec file
rm punch.spec
