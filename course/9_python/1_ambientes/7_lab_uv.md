---
id: lab-uv
title: "Lab: uv de punta a punta"
nav_title: "Lab: uv"
summary: "Crear, usar, romper y recrear un proyecto uv, viendo en cada paso qué archivo cambió: pyproject.toml, uv.lock o .venv."
status: ready
estimated_time: 30m
tags: [uv, pyproject, lockfile, venv, uvx, pep-723]
prerequisites: [un-ambiente-por-dentro]
---

# Lab: uv de punta a punta

**Página 7 de 10 · Ambientes**

Meta: crear, usar, romper y recrear un proyecto uv, y ver en cada paso qué archivo cambió.

![Tres cajas: pyproject.toml, uv.lock y .venv, unidas por uv lock y uv sync; uv add escribe la primera, uv run usa la última, y abajo: a git van pyproject.toml y uv.lock, .venv no.](../_assets/py-mapa.svg)

## En corto

- **`uv add` escribe `pyproject.toml`, resuelve `uv.lock` e instala en `.venv/`**, todo en un comando.
- **`uv run` nunca necesita activar**, y si falta `.venv/` lo recrea desde el lock.
- A git van `pyproject.toml` y `uv.lock`; `.venv/` se tira y se recrea.

## Antes: tu uv

**Haz:**

```bash
uv self update
uv --version
```

**Deberías ver:** `uv 0.12.21` o más nuevo. Las salidas de esta página se capturaron con **uv 0.12.21** y Python 3.13.15; tus números de versión pueden ser mayores. Si instalaste uv con otro gestor (Homebrew, pipx), `uv self update` te lo dice: actualiza con ese gestor.

### 1. El intérprete

**Haz:**

```bash
uv python install 3.13
```

**Deberías ver:**

```text
Installed Python 3.13.15 in 1.99s
 + cpython-3.13.15-linux-x86_64-gnu (python3.13)
```

**En el mapa:** uv pone el Python. No necesitas el del sistema, ni instalarlo aparte.

### 2. Un proyecto

**Haz:**

```bash
cd ~/fdd/fdd_o26/estudiantes/$GHUSER/09_python/ambientes
uv init --no-package demo && cd demo
ls -a && cat pyproject.toml
```

**Deberías ver:**

```text
.  ..  .python-version  README.md  main.py  pyproject.toml
[project]
name = "demo"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = []
```

**En el mapa:** existe `pyproject.toml`; todavía no hay `uv.lock` ni `.venv/`. `--no-package` es para un proyecto que sólo corre scripts; sin la bandera, uv 0.12 arma un paquete instalable con carpeta `src/`.

### 3. Un paquete

**Haz:**

```bash
uv add rich
ls -a && grep -A2 dependencies pyproject.toml
```

**Deberías ver:** (recortado)

```text
 + rich==15.0.0
.  ..  .python-version  .venv  README.md  main.py  pyproject.toml  uv.lock
dependencies = [
    "rich>=15.0.0",
]
```

**En el mapa:** un comando tocó las tres cajas. `pyproject.toml` ganó un **rango** (`>=15.0.0`); `uv.lock` y `.venv/` nacieron.

### 4. Correr

**Haz:**

```bash
cp ../hola.py .
uv run hola.py
```

**Deberías ver:** `Hola desde un Python que sí tiene rich instalado.`, con colores.

**En el mapa:** `uv run` usó `.venv/` sin activar nada.

### 5. Leer el lock

**Haz:**

```bash
grep -c '^\[\[package\]\]' uv.lock
uv tree
```

**Deberías ver:**

```text
5
demo v0.1.0
└── rich v15.0.0
    ├── markdown-it-py v4.2.0
    │   └── mdurl v0.1.2
    └── pygments v2.21.0
```

**En el mapa:** pediste un paquete y el lock fija cinco entradas: tu proyecto, `rich` y tres **transitivas** que `rich` necesita. Cada una con versión exacta y hash.

### 6. Romperlo

**Haz:**

```bash
rm -rf .venv
uv run hola.py
```

**Deberías ver:**

```text
Creating virtual environment at: .venv
Installed 4 packages in 12ms
Hola desde un Python que sí tiene rich instalado.
```

**En el mapa:** `.venv/` se recreó desde `uv.lock`, con las mismas versiones. Por eso `.venv/` no va a git: se recrea en segundos.

### 7. Dependencias de desarrollo

**Haz:**

```bash
uv add --dev pytest
tail -4 pyproject.toml
```

**Deberías ver:**

```text
[dependency-groups]
dev = [
    "pytest>=9.1.1",
]
```

**En el mapa:** `pytest` lo necesitas tú para probar, no el programa para correr. Va en otro grupo.

### 8. Quitar

**Haz:**

```bash
uv remove rich
uv run hola.py
```

**Deberías ver:**

```text
 - rich==15.0.0
ModuleNotFoundError: No module named 'rich'
```

**En el mapa:** se fue de las tres cajas. Vuelve a ponerlo: `uv add rich`.

### 9. Una herramienta sin instalarla

**Haz:**

```bash
uvx cowsay -t hola
```

**Deberías ver:** una vaca que dice `hola`.

**En el mapa:** ninguna caja cambió. `uvx` corre un programa en un ambiente temporal, fuera de tu proyecto.

### 10. Un script con sus dependencias dentro

**Haz:**

```bash
cd ..
head -4 script_autonomo.py
uv run script_autonomo.py
```

**Deberías ver:** el bloque `# /// script` con `dependencies = ["rich"]`, y una tabla cuya fila «Ambiente» apunta a `~/.cache/uv/environments-v2/…`.

**En el mapa:** el bloque del archivo hace de `pyproject.toml` (PEP 723). Sirve para scripts sueltos: no hay proyecto ni `.venv/` en tu carpeta.

## Puente al mundo de pip

| Comando | Para qué |
|---|---|
| `uv pip install rich` | La interfaz de pip, más rápida, sobre el ambiente activo o `.venv/` |
| `uv export --no-hashes --no-dev > requirements.txt` | Para quien sólo tiene pip; `--no-dev` deja fuera `pytest` y lo demás de desarrollo |

La salida (recortada) lista cada paquete con su versión exacta y, debajo, quién lo pidió:

```text
markdown-it-py==4.2.0
    # via rich
rich==15.0.0
    # via demo
```

## Qué subes a git

| Archivo | ¿A git? | Por qué |
|---|---|---|
| `pyproject.toml` | ✅ | Lo que pides |
| `uv.lock` | ✅ | Las versiones exactas: sin él, otra máquina resuelve otras |
| `.python-version` | ✅ | Qué Python usa el proyecto |
| `.venv/` | ❌ | Se recrea con `uv sync`; el `.gitignore` del curso lo excluye y la revisión de entregas lo rechaza |

::: problem {#py-lab-uv-clon title="Lo clonaste en otra máquina"}
Tu compañero clona tu repo: trae `pyproject.toml` y `uv.lock`, sin `.venv/`. ¿Qué comando corre para tener exactamente tus versiones, y por qué no `uv add rich`?
:::

::: hint {of="py-lab-uv-clon"}
¿Cuál de los dos archivos tiene las versiones exactas?
:::

::: answer {of="py-lab-uv-clon"}
- `uv sync`, o directo `uv run hola.py`: instalan lo que dice `uv.lock`.
- `uv add rich` volvería a resolver y podría escoger una versión más nueva que la tuya.
:::

Sigue con [[lab-venv-y-pip]]: la forma clásica, para reconocerla en un README.

> [!NOTE]
> **Si sólo recuerdas una cosa:** pyproject.toml dice lo que pides, uv.lock lo que exactamente se instaló, y .venv/ se tira y se recrea con uv sync.
