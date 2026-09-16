---
id: la-idea-del-contenedor
title: "La idea"
nav_title: "1. La idea"
summary: "Qué es un contenedor, qué pasa cuando escribes docker run, y por qué el mundo se movió a esto."
status: ready
tags: [contenedor, namespace, cgroup, imagen, orquestacion]
---

# La idea

**Sección 1 de 3** · 9 páginas · unos 106 min · sesión del jueves 17 de septiembre, 19:00–20:00

Meta: que "proceso aislado" deje de ser una frase hecha, y que `docker run` deje de ser magia.

## En corto

- Sesión **sin computadora**: las páginas se proyectan y no se teclea nada.
- **Un contenedor es un proceso de Linux con la vista recortada y la despensa medida**: comparte el kernel del host y tiene su propia vista de archivos, procesos, red, usuarios y recursos.
- Cuatro páginas se ven en clase; las otras cinco son lectura para completar antes de la sesión 2.

## Las nueve páginas

| # | Página | Qué agrega | Min | Dónde |
|---:|---|---|---:|---|
| 1 | En mi máquina sí funciona | Qué problema resolvieron los contenedores, y la comparación con `venv`/conda | 8 | clase |
| 2 | Qué es un contenedor | Namespaces y cgroups: qué ve un proceso contra cuánto puede usar | 12 | clase |
| 3 | Receta, congelado, servido | Dockerfile, imagen y contenedor: las tres cosas que todo el mundo confunde | 10 | clase |
| 4 | Qué pasa cuando escribes `docker run` | La cadena completa y medida: CLI, daemon, containerd, shim y runc | 12 | clase |
| 5 | De uno a mil: escalamiento y orquestación | Por qué el mundo se movió a esto, más allá de la reproducibilidad | 10 | lectura |
| 6 | VM contra contenedor | Dónde ocurre el aislamiento, y cuándo el contenedor no es la respuesta | 10 | lectura |
| 7 | Docker y Podman | La diferencia es arquitectónica, y qué compra exactamente correr sin daemon | 14 | lectura |
| 8 | Capas y caché | Por qué un `build` a veces tarda tres segundos y a veces tres minutos | 15 | lectura |
| 9 | Lo que cuesta | Números propios de arranque y ejecución, y cómo leerlos sin engañarte | 15 | lectura |

## Antes de empezar

Nada que instalar. Esta sección corre entera sin terminal: instalar Docker y Podman es la primera página de la sección siguiente.

## Qué te llevas

- Un modelo mental de qué es un contenedor, no una definición de memoria.
- La cadena completa de lo que pasa al escribir `docker run`, y qué queda vivo cuando matas cada pieza.
- Números propios de cuánto cuesta arrancar y correr dentro de un contenedor.
</content>
