---
id: contenedores
title: "Contenedores"
nav_title: "Contenedores"
summary: "Tres clases. Qué es un contenedor, cómo se usa en tu máquina, y cómo se reparte un sistema en servicios."
status: ready
estimated_time: 399m
tags: [docker, podman, contenedor, imagen, volumen, namespace, cgroup, kata, seguridad, diseno]
prerequisites: [git-y-github]
---

# Contenedores

![Muelle de carga nocturno visto desde una pasarela elevada: una hilera de bloques sellados e idénticos entre sí desciende por un haz de luz vertical y se acomoda, sin abrirse, sobre un camión, un vagón de tren y la cubierta de un barco alineados abajo; al fondo se recorta la silueta de una grúa portuaria, y en primer plano una figura de espaldas observa el descenso a contraluz contra el resplandor del muelle.](_assets/ilus-contenedores-portada.jpg)

**Tres clases** · 35 páginas · unos 399 min

## En corto

- **Un contenedor no es una máquina pequeña: es un proceso de Linux con la vista recortada y la despensa medida.** Comparte el kernel del host; los namespaces deciden qué puede ver, los cgroups deciden cuánto puede usar.
- Vas a instalar Docker y Podman en tu propia máquina, construir una imagen, montarle un volumen y publicarla en un registro público.
- La unidad termina en diseño: cómo se reparte una aplicación en varios contenedores, y por dónde se rompe el aislamiento cuando algo sale mal.

## Las tres secciones

| # | Sección | Qué contesta | Sesión | Páginas | Min |
|---:|---|---|---|---:|---:|
| 1 | La idea | Qué es un contenedor, y qué pasa exactamente cuando escribes `docker run` | jueves 17 de septiembre, 19:00–20:00 | 9 | 106 |
| 2 | Manos a la obra | Instalar, construir, montar y limpiar. Dónde vive cada byte de tu contenedor | martes 22 de septiembre, 19:00–20:30 | 13 | 180 |
| 3 | Diseño y seguridad | Cómo se reparte una aplicación en servicios, y por dónde se rompe el aislamiento | jueves 24 de septiembre, 19:00–20:30 | 5 | 69 |

La primera sesión es **corta y sin computadora**: 60 minutos, no 90. Las páginas se proyectan y no se teclea nada; el teclado empieza en la sesión 2.

## Cuánto trabajo hay fuera de clase

Además de las tres clases, la unidad pide ≈ 236 minutos de lectura —las páginas marcadas «lectura» o «previa» dentro de cada sección, más los cuatro anexos de referencia— más **8 h 27 de DataCamp**, repartidas entre *Introduction to Docker* e *Intermediate Docker*. En total son **unas 12 horas y media en doce días**. Es el número con el que decides, desde el jueves 17, cómo repartes el resto de tu semana.

## Los benchmarks de la unidad

Los cinco scripts que miden lo que de verdad cuesta un contenedor —arranque, escala, ejecución y anidamiento— viven en `_assets/benchmarks/`, junto con los CSV ya medidos. [`code/analyze.py`](code/analyze.py) los lee y genera las cuatro gráficas que usa la unidad; es opcional, no es una entrega, y sigue el mismo patrón que el notebook publicado en la unidad de arquitectura de computadoras.

## Antes de empezar

Necesitas Git y GitHub: la primera entrega de esta unidad ya se hace por pull request, igual que el resto del curso desde la unidad anterior. Nada más hace falta todavía — instalar Docker y Podman es la primera página de la segunda sección.
