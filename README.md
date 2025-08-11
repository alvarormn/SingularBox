# AimHarder Selenium (Docker)

Automatiza la reserva de **CrossFit a las 07:00** para el **día objetivo = hoy + 3 días**, saltando sábados y domingos.

## Configuración

1. Crea un `.env` (no se sube a Git):
```
AIMHARDER_URL=https://aimharder.com
USUARIO=tu_usuario
CONTRASENA=tu_contrasena
```

2. Construye la imagen:
```
docker build -t aimharder-bot .
```

3. Ejecuta el contenedor (leyendo variables desde `.env`):
```
docker run --rm --env-file .env aimharder-bot
```

> El proyecto usa `Europe/Madrid` para el cálculo de fechas.

## Estructura
- `main.py` – Orquestación del flujo.
- `cookies.py` – Rechazo de cookies (JS `denyAllBtn()` + fallback clic).
- `aimharder.py` – Funciones específicas del sitio (login, seleccionar día, clase y reservar).
- `config.py` – Carga de variables de entorno con `python-dotenv`.
- `Dockerfile` – Entorno reproducible con Chromium + Chromedriver.
- `requirements.txt` – Dependencias Python.

## Scheduler
La imagen está lista para ejecutarse bajo cualquier planificador externo (cron del host, GitHub Actions, Azure Pipelines). Por ejemplo, cron L-V 07:00:
```
0 7 * * 1-5 docker run --rm --env-file /ruta/.env aimharder-bot
```
