# Verzekeringen API

This is the Django API repository for the Scouts verzekeringen project. See https://gitlab.inuits.io/customers/scouts/verzekeringen/verzekeringen-common for general information.

## Local setup

The common repository contains information about how to easily run a local (developement) enviroment.

Requirements: Python

1. Create virtual env: `python -m venv ./venv`
2. Activate virtual env:

    - Windows: `venv\Scripts\Activate.ps1`
    - Linux & MacOS: `source venv/bin/activate`

3. Install packages (poetry): `poetry install`
4. Activeer de poetry shell: `poetry shell`
5. Run the app: `python verzekeringen_api/manage.py runserver 0.0.0.0:8000`

## Problems

Fix 1: Installeer python versie 3.11
Fix 2: Ga in etc/requirements en pas python_version aan

## Poetry

### Installeren

Project gebruikt poetry voor het onderhouden van de packages.
Installeer:

-   Linux (yay): `yay -S python-poetry`

### Packages toevoegen

If you want to add a package: `poetry add requests`
Or for dev dependencies: `poetry add --dev pytest`
