@echo off
ECHO Starting your CliQ Django project...

REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Run the Django development server
python manage.py runserver

REM Keep the window open after the server stops
pause