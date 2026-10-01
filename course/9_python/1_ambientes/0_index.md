---
id: ambientes-python
title: "Ambientes"
nav_title: "1. Ambientes"
summary: "Qué es un ambiente de Python, qué herramientas existen y por qué usamos uv."
status: ready
tags: [python, uv, venv, pip, pyproject, lockfile, ambiente]
---

# Ambientes

**Sección 1** · 12 páginas · unos 120 min · sesión del jueves 1 de octubre, 19:00–20:00

Meta: que sepas en qué Python y con qué paquetes corre tu código, y cómo hacer que corra igual en otra máquina.

::: figure {#py-mapa title="Qué produce qué en un proyecto uv"}
![Tres cajas en fila. Lo que pides, pyproject.toml, con rangos como rich>=15, que escribes tú o uv add. Una flecha uv lock lleva a lo que se resolvió, uv.lock, con versión exacta y hash de cada paquete, también las transitivas, que se bajan de PyPI. Una flecha uv sync lleva a lo que está instalado, la carpeta .venv con su python y su site-packages, desechable. De .venv sale uv run hacia tu programa, y uv python install pone el intérprete. Abajo: pyproject.toml y uv.lock van a git; .venv no va a git, se borra y se recrea con uv sync.](../_assets/py-mapa.svg)
:::

## En corto

- **Un ambiente es una carpeta (`.venv/`) con su propio `python` y sus propios paquetes.**
- **Usamos uv**: un solo programa crea el ambiente, instala, fija versiones y pone el intérprete.
- A git van `pyproject.toml` y `uv.lock`; **`.venv/` nunca**.

## Las páginas

| # | Página | Qué agrega | Min | Dónde |
|---:|---|---|---:|---|
| 1 | [[el-problema-de-los-ambientes]] | Los dos errores que hacen necesarios los ambientes | 5 | clase |
| 3 | [[un-ambiente-por-dentro]] | Tres comandos que muestran qué es un ambiente y qué hace «activar» | 15 | clase |
| 7 | [[lab-uv]] | Un proyecto uv de punta a punta: crear, usar, romper y recrear | 30 | clase |
| 9 | [[ambientes-en-vs-code]] | Que VS Code use el `.venv` de tu proyecto | 10 | clase |

## La clase de hoy, en 60 minutos

| Página | Min |
|---|---:|
| 1 · El problema | 5 |
| 3 · Un ambiente por dentro | 15 |
| 7 · Lab: uv | 30 |
| 9 · VS Code | 10 |

## Antes de clase

1. **uv instalado**: `uv --version` responde (instrucciones en [[python]]).
2. **Los archivos del lab, fuera del repo**:

```bash
mkdir -p ~/lab-ambientes
cp -r ~/fdd/fdd_o26/codigo/09_python/ambientes/. ~/lab-ambientes/
ls ~/lab-ambientes
```

**Deberías ver** `hola.py`, `quien_soy.py`, `requirements.txt` y `script_autonomo.py`.

Los labs trabajan en `~/lab-ambientes/`, **fuera** del repo del curso: crean `.venv/` y archivos que no deben acabar en un `git add`.
