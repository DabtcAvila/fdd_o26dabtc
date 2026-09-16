---
id: contenedores-con-las-manos
title: "Manos a la obra"
nav_title: "2. Manos a la obra"
summary: "Instalar, construir, montar y limpiar. Dónde vive cada byte de tu contenedor."
status: ready
tags: [docker, podman, volumen, bind-mount, dockerfile, registro]
---

# Manos a la obra

**Sección 2 de 3** · 13 páginas · unos 180 min · sesión del martes 22 de septiembre, 19:00–20:30

Meta: instalar los dos runtimes, construir una imagen, publicarla, y saber exactamente dónde vive cada byte que escribe un contenedor.

## Dónde vive cada cosa

Todo el trabajo de práctica —construir, romper, montar volúmenes— ocurre en `~/fdd/docker-lab`: una carpeta **local y desechable**, que **no es un repositorio** de Git. Se puede borrar y rehacer sin ninguna consecuencia. Nada de lo que hagas ahí se sube a ningún lado por sí solo.

Lo que sí se entrega llega a tu fork por pull request, igual que todo desde la unidad de Git y GitHub, y cae en **dos** carpetas distintas. Son dos porque las entregas del martes 22 nacen las dos de `main`: si escribieran en la misma carpeta, cada pull request agregaría su propia versión de los mismos archivos y el merge acabaría en conflicto. Separadas, los conjuntos no se tocan.

- `estudiantes/<tu-login>/docker/` **acumula tus certificaciones de DataCamp** a lo largo del mes: un solo `certificaciones.md`, que llenas una sección por entrega, más las capturas. Es espejo de `codigo/docker/`, exactamente como la unidad 7 hizo con `github/certificaciones.md`. Ahí van las tres entregas de DataCamp de esta unidad.
- `estudiantes/<tu-login>/08_contenedores/` **guarda el trabajo de la unidad**: tu imagen publicada, el `Dockerfile` arreglado y la bitácora. Es la carpeta de una sola entrega, la del `tarea-08-imagen`.

De ahí sale una regla que la revisión automática comprueba y que no tiene periodo de gracia: **cada pull request toca una sola de las dos**, nunca las dos a la vez.

## Léelas antes del martes

Las tres primeras páginas de la tabla son **lectura previa**, no de clase, y por eso van primero: hay que leerlas **antes del martes**, porque sus entregas vencen ese mismo día, antes de que empiece la sesión.

## Las trece páginas

| # | Página | Qué agrega | Min | Dónde |
|---:|---|---|---:|---|
| 1 | [[instalar-docker-y-podman]] | Los dos runtimes corriendo sin `sudo`, en las tres plataformas | 25 | previa |
| 2 | [[planes-b-de-instalacion]] | Qué hacer si la instalación no salió, con las trampas más comunes y su síntoma | 12 | previa |
| 3 | [[a-docker-hub]] | Publicar una imagen propia y comprobar que existe para los demás | 12 | previa |
| 4 | [[ciclo-de-vida-de-un-contenedor]] | La única idea que explica todo el ciclo: un contenedor vive lo que vive su proceso | 12 | clase |
| 5 | [[el-dockerfile-por-dentro]] | Construir una imagen y ver de qué está hecha: capas, contexto, `CMD` contra `ENTRYPOINT` | 15 | lectura |
| 6 | [[arreglar-un-dockerfile]] | Reconocer y corregir los tres defectos de un Dockerfile real | 12 | lectura |
| 7 | [[donde-vive-cada-byte]] | La tabla que ordena toda la clase: capas de imagen, capa de escritura, bind mount, named volume | 10 | clase |
| 8 | [[rutas-en-docker]] | Relativa contra absoluta, y por qué un `./` olvidado crea un volumen vacío en silencio | 10 | lectura |
| 9 | [[el-archivo-compartido]] | El bind mount en las dos direcciones, y de quién queda el archivo según tu plataforma | 15 | clase |
| 10 | [[los-ocho-casos]] | Código en la imagen o en volumen, editado dentro o fuera, con o sin rebuild: predecir antes de ejecutar | 15 | clase |
| 11 | [[las-cuatro-trampas]] | Los filos que cortan la primera vez, incluida la del volumen que copia en vez de tapar | 15 | lectura |
| 12 | [[named-volumes-y-postgres]] | Ver el estado sobrevivir a su contenedor | 15 | lectura |
| 13 | [[limpieza-de-docker]] | Recuperar el disco y entender qué se borra con cada `prune` | 12 | lectura |

## Antes de empezar

Necesitas haber resuelto la instalación (página 1) antes del martes: Docker o Podman corriendo sin `sudo`, y las imágenes del prepull ya descargadas.

## Qué te llevas

- Docker y Podman corriendo en tu máquina, sin `sudo`.
- Una imagen propia, publicada en un registro público.
- Un modelo de dónde vive cada byte que escribe un contenedor, y por qué eso decide si sobrevive a un `docker rm`.
