---
id: las-herramientas-de-ambientes
title: "Las herramientas, con pros y contras"
nav_title: "Las herramientas"
summary: "pip, venv, pip-tools, pipenv, poetry, pdm, hatch, conda, pixi, pyenv, pipx y uv: qué trabajo hace cada una, sus pros y contras, y por qué en este curso usamos uv."
status: ready
estimated_time: 12m
tags: [uv, pip, poetry, conda, pixi, pdm, hatch, pyenv, pipx, pipenv]
prerequisites: [los-archivos-del-ambiente]
---

# Las herramientas, con pros y contras

**Página 5 de 10 · Ambientes**

Meta: reconocer cada herramienta cuando la veas en un repo ajeno, y saber por qué aquí usamos uv.

::: figure {#py-trabajos title="Cinco trabajos, doce herramientas"}
![Matriz de doce herramientas contra cinco trabajos: instalar paquetes, aislar, proyecto + lock, versiones de Python y herramientas de terminal. pip sólo instala; venv sólo aísla; pip-tools sólo fija versiones; pipenv y poetry instalan, aíslan y manejan proyecto con lock; pdm y hatch además instalan versiones de Python; conda hace casi todo y su lock es a medias; pixi y uv hacen los cinco; pyenv sólo versiones de Python; pipx instala herramientas de terminal aisladas. La fila de uv está resaltada.](../_assets/py-trabajos.svg)
:::

## En corto

- Cada herramienta resuelve **uno o varios de cinco trabajos**: instalar paquetes, aislar, proyecto + lock, versiones de Python, herramientas de terminal.
- **uv hace los cinco, y rápido.** No instala paquetes que no son de Python.
- Las vas a encontrar todas en proyectos ajenos: hay que reconocerlas, no dominarlas.

## La tabla

::: table {#py-tabla-herramientas title="Las herramientas, con pros y contras"}

| Herramienta | Desde | Qué hace | 👍 | 👎 | Dónde la vas a ver |
|---|---|---|---|---|---|
| **pip** | 2008 | Instala paquetes de PyPI | Viene con Python | No aísla; no fija las transitivas | Todos los tutoriales |
| **venv** | 2012 (Python 3.3) | Crea ambientes | Viene con Python | Sólo aísla; lo demás lo haces tú | READMEs, Dockerfiles |
| pip-tools | 2012 | `requirements.in` → `requirements.txt` con todo fijado | Simple, encima de pip | Sólo hace eso | Proyectos maduros |
| pipenv | 2017 | pip + venv + lock (`Pipfile`, `Pipfile.lock`) | Fue el primer todo-en-uno | Lento; perdió impulso | Proyectos de 2018 a 2020 |
| **poetry** | 2018 | Proyecto, lock, publicar paquetes | Maduro, muy usado | Más lento; formato propio hasta su versión 2 (2025) | Muchas empresas |
| pdm | 2019 | Proyecto + lock, apegado al estándar | Muy estándar | Comunidad chica | Librerías |
| hatch | 2017 | Proyecto, ambientes de prueba, publicar | El más cómodo para publicar librerías | Menos pensado para aplicaciones | Librerías open source |
| **conda** / mamba | 2012 | Paquetes de Python **y de fuera de Python**, con su propio Python | CUDA, GDAL, R | Pesado; otro registro de paquetes; la distribución Anaconda cobra licencia a organizaciones grandes (términos de 2024) | Ciencia, academia |
| pixi | 2023 | Paquetes de conda, rápido, con lockfile | Lo de conda con un flujo moderno | Joven | GPU, geoespacial |
| pyenv | 2012 | Instala versiones de Python | Hace bien una sola cosa | uv ya lo hace | Máquinas de desarrolladores |
| pipx | 2017 | Instala programas de terminal, cada uno aislado | Sencillo | uv tiene `uvx` | `pipx install ruff` |
| **uv** | 2024 | **Los cinco trabajos** | 10 a 100 veces más rápido que pip; un solo binario; sigue los estándares | Es de una empresa (Astral), cuya compra anunció OpenAI el 2026-03-19; no instala paquetes de fuera de Python | **Este curso** |

:::

## Por qué uv

- **Velocidad**: resuelve e instala en segundos lo que con pip o poetry tarda minutos. En clase se nota.
- **Un solo programa**: hace el trabajo de pip, venv, pip-tools, pyenv y pipx. Menos cosas que instalar y que se contradigan.
- **Archivos estándar**: escribe `pyproject.toml` (PEP 621) y exporta `pylock.toml` (PEP 751). Si mañana cambias de herramienta, tu `pyproject.toml` sirve igual.

## Lo que uv no te da

- **Paquetes de fuera de Python** (CUDA, GDAL, compiladores): para eso, pixi o conda.
- **Independencia de una empresa**: uv es open source (licencias MIT y Apache), pero lo desarrolla una sola compañía. El seguro es el mismo: los archivos son estándar.

Una que ya no vas a ver en proyectos nuevos: **rye** (2023). Astral la tomó en 2024 y hoy recomienda uv en su lugar.

## ¿Cuál uso?

::: figure {#py-cual-uso title="¿Cuál uso?"}
![Árbol de decisión de tres preguntas. ¿Necesitas paquetes que no son de Python, como CUDA o GDAL? Sí: pixi, o conda. No: ¿el proyecto ya usa poetry, pdm o hatch? Sí: usa esa y lee su pyproject.toml. No: ¿es un script suelto? Sí: uv run script.py con sus dependencias dentro, PEP 723. No: uv init y uv add, que es el caso de este curso.](../_assets/py-cual-uso.svg)
:::

**Regla práctica**: en un repo ajeno, **usa la herramienta que ya usa el repo**. Su lock (`poetry.lock`, `uv.lock`, `pixi.lock`) te lo dice.

::: problem {#py-herramientas-elige title="Tres repos, tres herramientas"}
Te pasan tres repos: (a) un notebook que entrena un modelo con CUDA y trae `environment.yml`; (b) una API que trae `pyproject.toml` y `poetry.lock`; (c) tu tarea de este curso. ¿Con qué herramienta trabajas cada uno?
:::

::: hint {of="py-herramientas-elige"}
Mira qué archivo de lock o de ambiente trae cada repo, y la figura «¿Cuál uso?».
:::

::: answer {of="py-herramientas-elige"}
- (a) conda o pixi: necesita CUDA, que no es un paquete de Python, y ya trae `environment.yml`.
- (b) poetry: el lock es suyo. Mezclar herramientas en un mismo repo produce dos locks que se contradicen.
- (c) uv.
:::

Fuentes: [Which Python package manager should I use? (pydevtools, 2026)](https://pydevtools.com/handbook/explanation/which-python-package-manager-should-i-use/) · [OpenAI to acquire Astral (2026-03-19)](https://openai.com/index/openai-to-acquire-astral/) · [Documentación de uv](https://docs.astral.sh/uv/).

Sigue con [[ambiente-conda-docker]]: qué aísla cada una, comparado con un contenedor.

> [!NOTE]
> **Si sólo recuerdas una cosa:** las herramientas cambian; pyproject.toml se queda.
