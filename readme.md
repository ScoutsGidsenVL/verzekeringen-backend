# Verzekeringen API

Dit is de Django API-repository voor het Scouts verzekeringen-project. Zie https://gitlab.inuits.io/customers/scouts/verzekeringen/verzekeringen-common voor algemene informatie.

## Lokale setup

De gemeenschappelijke repository bevat informatie over hoe je eenvoudig een lokale (ontwikkelings)omgeving kunt uitvoeren.

### Automatische setup met Docker

Navigeer naar de /docker map en voer het volgende commando uit in de terminal:

```bash
docker compose up -d --build
```

Om logs weer te geven:
```bash
docker logs -f verzekeringen_django
```

### Handmatige setup

Vereisten: Python

1. Maak virtual env aan: `python -m venv ./venv`
2. Activeer virtual env:

    - Windows: `venv\Scripts\Activate.ps1`
    - Linux & MacOS: `source venv/bin/activate`

3. Wijzig python versie: `pyenv local 3.9.9` // indien niet geïnstalleerd = `yay -S pyenv` en daarna `pyenv install 3.9.9`
4. Gebruik python versie 3.9.9: `poetry env use python3.9`
5. Installeer packages (poetry): `poetry install`
6. Activeer de poetry shell: `poetry shell`
7. Voer de app uit: `python verzekeringen_api/manage.py runserver 0.0.0.0:8000`

## Problemen

### Kan requirements niet installeren door python versie

Fix 1: Installeer python versie 3.9.x maar NIET 3.9.1
Fix 2: Ga in etc/requirements en verwijder overal 'and python_version < "3.10"'

## Poetry

### Installeren

Project gebruikt poetry voor het onderhouden van de packages.
Installeer:

-   Linux (yay): `yay -S python-poetry`

### Packages toevoegen

Als je een package wilt toevoegen: `poetry add requests`
Of voor dev dependencies: `poetry add --dev pytest`
