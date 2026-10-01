---
id: los-archivos-del-ambiente
title: "Los archivos de un proyecto"
nav_title: "Los archivos"
summary: "requirements.txt, pyproject.toml, uv.lock, pylock.toml y environment.yml: qué dice cada uno, quién lo escribe y cuáles van a git."
status: ready
estimated_time: 8m
tags: [pyproject, requirements, lockfile, pylock, toml, pep-621, pep-751]
prerequisites: [un-ambiente-por-dentro]
---

# Los archivos de un proyecto

**Página 4 de 10 · Ambientes**

Meta: reconocer cada archivo de ambiente que vas a encontrar en un repo, y saber cuál manda.

## En corto

- **`pyproject.toml` es el estándar** (PEP 621): lo leen uv, poetry, pdm y hatch.
- **El lock lo escribe la herramienta, nunca tú.**
- `requirements.txt` es el formato viejo de pip, y sigue en todos lados.

## Los seis

::: table {#py-tabla-archivos title="Los archivos de un proyecto de Python"}

| Archivo | Qué es | Lo escribe | ¿Versiones exactas? | ¿A git? |
|---|---|---|---|---|
| `requirements.txt` | Lista de paquetes, uno por línea; formato de pip | tú, o `pip freeze` | sólo si usas `==` | ✅ |
| `pyproject.toml` | Nombre, versión de Python y dependencias del proyecto (PEP 621) | tú, o `uv add` | ❌ rangos | ✅ |
| `uv.lock` · `poetry.lock` · `pdm.lock` | El lock de cada herramienta | la herramienta | ✅ con hash | ✅ |
| `pylock.toml` | El lock **estándar** (PEP 751, aceptado en 2025); uv lo exporta | la herramienta | ✅ con hash | ✅ |
| `environment.yml` | Lo mismo para conda | tú, o `conda env export` | depende | ✅ |
| `.python-version` | Qué versión de Python usa el proyecto | `uv init` o `uv python pin` | ✅ | ✅ |

:::

## Un pyproject.toml, línea por línea

Éste sale de `uv init --no-package demo`, `uv add rich` y `uv add --dev pytest`:

```toml
[project]
name = "demo"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "rich>=15.0.0",
]

[dependency-groups]
dev = [
    "pytest>=9.1.1",
]
```

| Línea | Qué dice |
|---|---|
| `[project]` | Empieza la sección estándar: la entienden todas las herramientas |
| `requires-python = ">=3.13"` | Con qué Python corre; uv lo usa para escoger intérprete |
| `dependencies` | Lo que el programa necesita para correr, como **rangos** |
| `[dependency-groups]` · `dev` | Lo que sólo necesitas tú para desarrollar (pruebas, formateo) |

Un rango (`>=15.0.0`) acepta versiones futuras. Por eso hace falta el lock: el rango dice qué aceptas, el lock dice qué se instaló.

## [tool.*]: lo que no es estándar

`[project]` y `[dependency-groups]` son estándar. Las secciones `[tool.uv]`, `[tool.poetry]` o `[tool.ruff]` son configuración propia de cada herramienta: las otras las ignoran.

El mismo proyecto hecho con **poetry 2.5** (salida real de `poetry init` + `poetry add rich`, sin las líneas de descripción y autor):

```toml
[project]
name = "demo"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "rich (>=15.0.0,<16.0.0)"
]

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

La sección `[project]` es la misma; cambian el formato del rango y el lock (`poetry.lock`). En proyectos de antes de 2025 vas a ver `[tool.poetry.dependencies]` en lugar de `[project]`: es el formato propio que poetry usaba antes de su versión 2.

## requirements.txt, ida y vuelta

| Quieres | Comando |
|---|---|
| De tu proyecto uv a un `requirements.txt` | `uv export --no-hashes > requirements.txt` |
| De un `requirements.txt` ajeno a tu proyecto uv | `uv add -r requirements.txt` |

::: problem {#py-archivos-lock title="El rango no basta"}
Tu `pyproject.toml` dice `rich>=15.0.0`. Tu compañera clona el repo dentro de seis meses, **sin** `uv.lock`, y corre `uv sync`. ¿Instala lo mismo que tú?
:::

::: hint {of="py-archivos-lock"}
¿Qué versiones acepta `>=15.0.0`?
:::

::: answer {of="py-archivos-lock"}
- No necesariamente: sin lock, uv resuelve otra vez y escoge la versión más nueva que cumpla el rango, por ejemplo una 15.4.
- Con `uv.lock` en el repo, instala exactamente la 15.0.0 que tú probaste.
:::

Sigue con [[las-herramientas-de-ambientes]]: quién escribe cada uno de estos archivos.

> [!NOTE]
> **Si sólo recuerdas una cosa:** pyproject.toml pide rangos, el lock fija versiones exactas, y a git van los dos.
