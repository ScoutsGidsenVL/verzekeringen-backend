# Verzekeringen API

This is the Django API repository for the Scouts verzekeringen project. See https://gitlab.inuits.io/customers/scouts/verzekeringen/verzekeringen-common for general information.

## Local setup

The common repository contains information about how to easily run a local (developement) enviroment.

Requirements: Python

1. Create virtual env: `python -m venv ./venv`
2. Activate virtual env:
    - Windows:
    - Macos:
    - Linux: 
3. Directly install psycopg2: `pip install psycopg2-binary`
4. Install requirements: `pip install -r .\etc\requirements.txt`
5. Run the app: `python verzekeringen_api/manage.py runserver 0.0.0.0:8000`

## Problems
### Kan requirements niet installeren door python versie
Fix 1: Installeer python versie 3.9.x maar NIET 3.9.1
Fix 2: Ga in etc/requirements en verwijder overal 'and python_version < "3.10"'