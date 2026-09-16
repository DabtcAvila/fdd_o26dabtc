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
- Tres páginas se ven en clase; las otras seis son lectura para completar antes de la sesión 2.

## Las nueve páginas

| # | Página | Qué agrega | Min | Dónde |
|---:|---|---|---:|---|
| 1 | En mi máquina sí funciona | Qué problema resolvieron los contenedores, y la comparación con `venv`/conda | 8 | clase |
| 2 | Qué es un contenedor | Namespaces y cgroups: qué ve un proceso contra cuánto puede usar | 12 | clase |
| 3 | Receta, congelado, servido | Dockerfile, imagen y contenedor: las tres cosas que todo el mundo confunde | 10 | lectura |
| 4 | Qué pasa cuando escribes `docker run` | La cadena completa y medida: CLI, daemon, containerd, shim y runc | 12 | clase |
| 5 | De uno a mil: escalamiento y orquestación | Por qué el mundo se movió a esto, más allá de la reproducibilidad | 10 | lectura |
| 6 | VM contra contenedor | Dónde ocurre el aislamiento, y cuándo el contenedor no es la respuesta | 10 | lectura |
| 7 | Docker y Podman | La diferencia es arquitectónica, y qué compra exactamente correr sin daemon | 14 | lectura |
| 8 | Capas y caché | Por qué un `build` a veces tarda tres segundos y a veces tres minutos | 15 | lectura |
| 9 | Lo que cuesta | Números propios de arranque y ejecución, y cómo leerlos sin engañarte | 15 | lectura |

Los 60 minutos de la sesión, repartidos:

- **3 min** — llegada y encuadre.
- **8 min** — página 1, *En mi máquina sí funciona*.
- **18 min** — página 2, *Qué es un contenedor*, con el ejercicio de las hojas de `ls -l /proc/1/ns/`.
- **22 min** — página 4, *Qué pasa cuando escribes `docker run`*, con el ejercicio de la cadena de pie.
- **5 min** — cierre y qué queda de tarea.

Suman **56**, no 60. Los cuatro minutos de diferencia son colchón a propósito: los dos ejercicios son de pie y con papel en las manos, y eso siempre se desborda.

Los números de esta sección vienen de tres tandas de medición distintas —los benchmarks de arranque, escala, ejecución y anidamiento son del semestre pasado; la comparación de runtimes OCI de la página 7 se midió aparte, en otra máquina; los inodos de namespaces se midieron ahora—, y cada una lleva su propio pie con la máquina y las versiones con que se obtuvo. No es un descuido: es la regla que la página 9 enseña con nombre y apellido.

## Antes de empezar

Nada que instalar. Esta sección corre entera sin terminal: instalar Docker y Podman es la primera página de la sección siguiente.

## Lo que se reparte en clase

Nada que instalar no quiere decir nada que preparar: dos de los tres bloques de clase se hacen con papel en las manos, y el papel hay que llevarlo impreso. Esto es a la vez el aviso al grupo y la lista de quien imprime.

- **Unas 15 hojas** con la salida de `ls -l /proc/1/ns/` del host y la del contenedor, una junto a la otra, para compararlas a mano. Es el ejercicio de la página 2.
- **Seis hojas rotuladas**: una por eslabón —`docker CLI`, `dockerd`, `containerd`, `shim`, `runc`— y una sexta que dice `proceso del contenedor`. Es el ejercicio de la página 4.

Eso es todo. El ejercicio de las tijeras no entra: se fue con la página 3 a lectura.

## Qué te llevas

- Un modelo mental de qué es un contenedor, no una definición de memoria.
- La cadena completa de lo que pasa al escribir `docker run`, y qué queda vivo cuando matas cada pieza.
- Números propios de cuánto cuesta arrancar y correr dentro de un contenedor.
