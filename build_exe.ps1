Write-Host "Installing required Python packages..." -ForegroundColor Cyan
pip install -r requirements.txt

Write-Host "Building executable using PyInstaller..." -ForegroundColor Cyan
# --noconsole prevents the black command prompt from showing when opening the GUI app
# --onefile packages everything into a single .exe file
pyinstaller --noconsole --onefile --name "AIBugFixer" gui_bugfixer.py

Write-Host "Done! The executable is located in the 'dist' folder." -ForegroundColor Green
