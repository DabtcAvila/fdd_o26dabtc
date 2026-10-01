---
id: ambientes-en-vs-code
title: "Ambientes en VS Code"
nav_title: "VS Code"
summary: "Que VS Code use el .venv de tu proyecto: elegirlo con Ctrl+Shift+P, verlo en la barra de estado y en la terminal integrada."
status: ready
estimated_time: 10m
tags: [vs-code, interprete, venv, jupyter, kernel]
prerequisites: [lab-uv]
---

# Ambientes en VS Code

**Página 9 de 10 · Ambientes**

Meta: que VS Code use el `.venv/` de tu proyecto, y saber comprobarlo.

## En corto

- **Ctrl+Shift+P** (macOS: **Cmd+Shift+P**) → *Python: Select Interpreter* → el `.venv` del proyecto.
- **El intérprete activo se ve abajo a la derecha**, en la barra de estado.
- La terminal integrada que abras después **se activa sola** con ese intérprete.

## Requisito

La extensión **Python** de Microsoft (`ms-python.python`). Si no la tienes: panel de extensiones (Ctrl+Shift+X), busca «Python», instala.

## Elegir el ambiente que hizo uv

1. Abre **la carpeta del proyecto**, no un archivo suelto: `code ~/lab-ambientes/demo`.
2. **Ctrl+Shift+P** abre la paleta de comandos.
3. Escribe `Python: Select Interpreter` y presiona Enter.
4. Elige la opción que dice `./.venv/bin/python` (Windows: `.\.venv\Scripts\python.exe`). Suele salir marcada como recomendada.
5. Mira la barra de estado, abajo a la derecha: ahora dice la versión y el nombre del ambiente.

Si el `.venv` no aparece en la lista: `uv sync` en la terminal para crearlo, y repite desde el paso 2.

## Crear uno desde VS Code

**Ctrl+Shift+P** → `Python: Create Environment` → *Venv* → la versión de Python → (opcional) marca `requirements.txt` para instalarlo.

Ese comando crea un `.venv` **con venv y pip, no con uv**: no escribe `pyproject.toml` ni `uv.lock`. En este curso el proyecto lo crea uv y VS Code **sólo lo elige**.

## Comprobar que está bien

| Dónde | Qué ves si está bien |
|---|---|
| Barra de estado, abajo a la derecha | La versión de Python y `.venv`, por ejemplo `3.13.15 (.venv)` |
| Una terminal integrada nueva (Ctrl+ñ o Ctrl+\`) | El prompt empieza con `(demo)` |
| `quien_soy.py` corrido con el botón ▶ | `¿en un ambiente?  : sí` |
| Un notebook `.ipynb` → *Select Kernel* | El mismo `.venv`. Necesita `uv add --dev ipykernel` antes |

La terminal integrada sólo se activa sola si la abres **después** de elegir el intérprete. Una que ya estaba abierta sigue como estaba: ciérrala y abre otra.

::: problem {#py-vscode-rojo title="Subrayado en rojo"}
`from rich import print` sale subrayado en amarillo o rojo en VS Code, con el aviso «Import "rich" could not be resolved». Pero `uv run hola.py` en la terminal funciona. ¿Qué está mal?
:::

::: hint {of="py-vscode-rojo"}
¿Qué intérprete dice la barra de estado?
:::

::: answer {of="py-vscode-rojo"}
- VS Code está analizando tu código con otro Python, normalmente el del sistema, que no tiene `rich`.
- `uv run` usa el `.venv`; VS Code no lo sabe hasta que se lo dices.
- Arreglo: Ctrl+Shift+P → *Python: Select Interpreter* → `.venv`. El código estaba bien.
:::

Sigue con [[trampas-de-ambientes]]: los errores de ambientes y dónde mirar.

> [!NOTE]
> **Si sólo recuerdas una cosa:** VS Code no adivina tu ambiente: se lo dices con Select Interpreter y lo compruebas en la barra de estado.
