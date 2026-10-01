---
id: python
title: "Python"
nav_title: "Python"
summary: "Python para trabajar con datos de forma profesional. Empieza por lo que todo proyecto necesita antes de su primera línea: un ambiente."
status: ready
estimated_time: 120m
tags: [python, uv, ambientes, venv, pip]
prerequisites: [contenedores]
---

# Python

**Una sección por ahora** · 12 páginas · unos 120 min

## En corto

- La unidad es Python para trabajar con datos de forma profesional: código que corre igual en tu máquina, en la de otra persona y en un contenedor.
- **Empieza por los ambientes**: dónde viven tus paquetes, qué versión de cada uno usa tu proyecto, y cómo se manejan con **uv**.
- Las demás secciones se agregan aquí cuando llega su clase.

## Las secciones

| # | Sección | Qué contesta | Sesión | Páginas | Min |
|---:|---|---|---|---:|---:|
| 1 | [[ambientes-python]] | Dónde viven tus paquetes, y cómo hacer que tu proyecto corra igual en otra máquina | jueves 1 de octubre, 19:00–20:00 | 12 | 120 |

## Antes de empezar

Necesitas **uv instalado antes de clase**, en la **misma terminal donde trabajas el repo**. En Windows eso es **WSL**, igual que Docker en la unidad 8: dentro de WSL usa el comando de Linux. El de PowerShell sólo sirve si trabajas fuera de WSL.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh      # Linux y macOS
```

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"   # Windows
```

Cierra la terminal, abre otra y comprueba:

```bash
uv --version
```

**Deberías ver** una línea `uv 0.12.…` o más nueva. Docker, de la unidad anterior, lo necesitas para una de las entregas.
