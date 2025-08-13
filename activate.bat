@echo off
echo Activating Personal Website Development Environment...
call "G:\apps\personal-website\venv\Scripts\activate.bat"
echo.
echo Available commands:
echo   python dev_server.py     - Start development server
echo   python deploy.py --help  - Deploy to AWS
echo   python build.py          - Build for production
echo   pytest                   - Run tests
echo.
