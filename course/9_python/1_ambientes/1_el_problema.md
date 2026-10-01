---
id: el-problema-de-los-ambientes
title: "El problema: un solo Python para todo"
nav_title: "El problema"
summary: "Sin ambientes, todos tus proyectos comparten los mismos paquetes, y el sistema operativo ya no te deja instalarlos encima de su Python."
status: ready
estimated_time: 5m
tags: [ambiente, site-packages, pep-668, pip]
prerequisites: [ambientes-python]
---

# El problema: un solo Python para todo

**Página 1 de 10 · Ambientes**

Meta: ver los dos errores que hacen necesarios los ambientes.

::: figure {#py-choque title="Dos proyectos, un solo Python"}
![Dos columnas. A la izquierda, sin ambientes: proyecto-a pide pandas 1.5 y proyecto-b pide pandas 2.2, y los dos apuntan al único site-packages del Python del sistema, donde sólo cabe una versión, la 2.2; la flecha de proyecto-a termina en rojo. A la derecha, con un .venv por proyecto: cada proyecto tiene su propio site-packages con su versión.](../_assets/py-choque.svg)
:::

## En corto

- Sin ambientes, **todos tus proyectos comparten un solo `site-packages/`**: instalar una versión borra la otra.
- En Ubuntu 24.04 y en macOS con Homebrew, **el sistema ya no te deja** hacer `pip install` sobre su Python (PEP 668).
- La salida: **un ambiente por proyecto**.

## Falla 1: una versión borra a la otra

`site-packages/` es la carpeta donde Python guarda los paquetes instalados. Sin ambientes hay **una sola**.

| Paso | Qué haces | Qué queda en `site-packages/` |
|---|---|---|
| Lunes | `pip install pandas==1.5` para `proyecto-a` | pandas 1.5 |
| Jueves | `pip install pandas==2.2` para `proyecto-b` | pandas 2.2 — **la 1.5 ya no está** |
| Lunes siguiente | corres `proyecto-a` | truena con una versión que no conoce |

Nadie tocó el código de `proyecto-a`. Lo rompió una instalación de otro proyecto.

## Falla 2: el sistema te lo prohíbe

En Ubuntu 24.04, `pip install` sobre el Python del sistema:

```bash
pip install rich
```

**Sale esto** (salida real, recortada):

```text
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.

    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
hint: See PEP 668 for the detailed specification.
```

Ese Python lo usa el propio sistema operativo para sus herramientas. Si le cambias paquetes, las puedes romper. Por eso, desde 2023, Debian, Ubuntu y Homebrew lo bloquean.

## Lo que vas a usar

| Problema | Lo resuelve |
|---|---|
| Versiones que chocan entre proyectos | Un `.venv/` por proyecto |
| «En mi máquina sí funciona» | `uv.lock`, con la versión exacta de cada paquete |
| El Python del sistema bloqueado | No lo tocas: uv instala y usa el suyo |

::: problem {#py-problema-pisa title="¿Quién se rompió?"}
Instalaste `pandas==1.5` para la tarea del lunes y el jueves `pandas==2.2` para otra, las dos con `pip install` sin ambiente. El lunes siguiente corres la primera y truena. ¿Qué pasó, si no tocaste su código?
:::

::: hint {of="py-problema-pisa"}
¿Cuántas carpetas `site-packages/` hay en tu máquina sin ambientes?
:::

::: answer {of="py-problema-pisa"}
- Una sola. El segundo `pip install` reemplazó la 1.5 por la 2.2.
- La tarea del lunes ahora corre con una versión que no conoce.
- Con un `.venv/` por proyecto, cada uno guarda la suya y no se tocan.
:::

Sigue con [[un-ambiente-por-dentro]]: qué hay en esa carpeta y cómo sabes cuál estás usando.

> [!NOTE]
> **Si sólo recuerdas una cosa:** sin ambientes, todos tus proyectos comparten los mismos paquetes, y el último que instala gana.
