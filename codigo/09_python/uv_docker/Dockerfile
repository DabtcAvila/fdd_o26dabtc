FROM python:3.13-slim

# uv no viene en la imagen de Python: se copia su binario de la imagen oficial.
COPY --from=ghcr.io/astral-sh/uv:0.12 /uv /usr/local/bin/uv

WORKDIR /app

# HUECO 1: copia aquí los dos archivos que describen el ambiente.
# HUECO 2: crea el ambiente desde el lock, sin dejar que cambie.
# HUECO 3: copia el programa.

CMD ["uv", "run", "--no-sync", "reporte.py"]
