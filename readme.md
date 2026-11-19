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

## Migraties

Om migraties te beheren of uit te voeren, kun je het volgende commando gebruiken:

```bash
docker exec -it verzekeringen_django python verzekeringen_api/manage.py migrate
```

### Lokale installatie

Vereisten: [uv](https://docs.astral.sh/uv/getting-started/installation/). Python hoef je niet zelf te installeren, uv haalt zelf Python 3.11, de versie van de server.

1. Installeer de dependencies uit `uv.lock` in `.venv`: `uv sync --python 3.11`
2. Voer de app uit: `uv run python verzekeringen_api/manage.py runserver 0.0.0.0:8000`

Met `just install` doe je stap 1 en maak je ook de mappen onder `var/` aan.

### Dependencies wijzigen

De dependencies staan in `pyproject.toml` onder `[project] dependencies`. Pas je die aan, werk dan `uv.lock` bij en commit beide files:

```bash
uv lock
```

Een pull request controleert of `uv.lock` overeenkomt met `pyproject.toml`.
