---
id: cheatsheet-ambientes
title: "Cheatsheet de ambientes"
nav_title: "A. Cheatsheet"
summary: "La misma tarea en uv, venv + pip, poetry y conda, en una sola tabla. uv es la columna que se usa en este curso; las otras son para leer repos ajenos."
status: ready
estimated_time: 5m
tags: [cheatsheet, uv, pip, venv, poetry, conda]
prerequisites: [trampas-de-ambientes]
---

# Cheatsheet de ambientes

**Anexo A** · para tener abierto

La columna **uv** es la del curso. Las otras tres sirven para traducir el README de un repo ajeno. Todos los comandos se probaron con uv 0.12.21, poetry 2.5.1 y conda 26.7.2.

::: table {#py-cheatsheet title="La misma tarea en cada herramienta"}

| Tarea | uv | venv + pip | poetry | conda |
|---|---|---|---|---|
| Instalar Python | `uv python install 3.13` | el instalador de tu sistema | `poetry python install 3.13` (experimental desde 2.1) | `conda create -n x python=3.13` |
| Nuevo proyecto | `uv init --no-package x` | `mkdir x && cd x` | `poetry new x` | — |
| Crear el ambiente | automático; o `uv venv` | `python3 -m venv .venv` | automático | `conda create -n x` |
| Activar | no hace falta: `uv run` | `source .venv/bin/activate` · Windows: `.venv\Scripts\activate` | `eval $(poetry env activate)` | `conda activate x` |
| Agregar un paquete | `uv add rich` | `pip install rich` | `poetry add rich` | `conda install rich` |
| Quitarlo | `uv remove rich` | `pip uninstall rich` | `poetry remove rich` | `conda remove rich` |
| Dependencia de desarrollo | `uv add --dev pytest` | un segundo `requirements-dev.txt` | `poetry add --group dev pytest` | — |
| Instalar desde el lock | `uv sync` | `pip install -r requirements.txt` | `poetry install` | `conda env create -f environment.yml` |
| Correr | `uv run x.py` | `python x.py`, activado | `poetry run python x.py` | `python x.py`, activado |
| Ver qué hay | `uv tree` | `pip list` | `poetry show --tree` | `conda list` |
| Exportar a requirements | `uv export --no-dev > requirements.txt` | `pip freeze > requirements.txt` | requiere el plugin `poetry-plugin-export` | `conda env export > environment.yml` |
| Una herramienta suelta | `uvx ruff` | `pipx run ruff` | — | — |
| Borrar el ambiente | `rm -rf .venv` | `deactivate && rm -rf .venv` | `poetry env remove --all` | `conda env remove -n x` |

:::

## Los cinco que más vas a usar

```bash
uv add rich              # agregar
uv run hola.py           # correr
uv sync                  # recrear desde el lock
uv tree                  # qué hay
rm -rf .venv             # borrar (uv sync lo recrea)
```

## Diagnóstico

```bash
which python3            # qué python encuentra tu shell
python3 -m pip --version # a qué Python instala pip
uv run quien_soy.py      # qué Python usa tu proyecto
```

Los errores frecuentes, con su causa, están en [[trampas-de-ambientes]].
