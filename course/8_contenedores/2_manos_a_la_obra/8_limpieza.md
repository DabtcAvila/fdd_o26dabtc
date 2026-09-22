---
id: limpieza-de-docker
title: "Limpieza"
nav_title: "Limpieza"
summary: "Recuperar el disco y entender qué se lleva exactamente cada prune, con la advertencia de la única columna donde borrar es perder."
status: ready
estimated_time: 12m
tags: [prune, disco, imagenes, volumenes, dangling, xargs, regex]
prerequisites: [named-volumes-y-postgres]
---

# Limpieza

**Página 8 de 16 · sección 2 de 3**

Meta: recuperar el disco sin borrar lo que no querías borrar.

::: figure {#cont-prune title="Qué se lleva exactamente cada prune"}
![El disco dibujado como cuatro montones —las imágenes, partidas en las que tienen un contenedor corriendo y las que nadie usa; los contenedores detenidos; las capas huérfanas o dangling; y los volúmenes sin dueño— cada uno con su tamaño. Debajo, una fila por comando con una marca en la columna que se lleva: docker container prune sólo los contenedores detenidos; docker image prune sólo las capas huérfanas; docker image prune -a además las imágenes que nadie usa; y docker system prune -a las tres del medio. La columna de volúmenes no queda marcada en ninguna de las cuatro filas, con una nota que dice que se piden aparte a propósito, porque es la única columna donde borrar es perder un dato y no rehacer un build: sin -a, docker volume prune y system prune --volumes sólo se llevan los volúmenes anónimos, y los que tienen nombre piden docker volume prune -a. Arriba, la salida de docker system df como el comando que mide antes de borrar. Al pie, la advertencia de que nada de esto toca lo que está en uso](../_assets/cont-prune.svg)
:::

## En corto

- **Mide antes de borrar**: `docker system df` te dice cuánto vas a recuperar y de dónde.
- Cada `prune` tiene su columna. Ninguno toca lo que está **en uso**, y los volúmenes se piden aparte.
- Borrar una imagen es rehacer un build; borrar un volumen es perder un dato.

## Cuánto está ocupando esto

Una sesión como la de hoy deja gigabytes que no aparecen en ninguna carpeta que puedas listar.

**Haz:**

```bash
docker system df
```

**Deberías ver:**
- cuatro renglones: `Images`, `Containers`, `Local Volumes`, `Build Cache`;
- columnas `TOTAL`, `ACTIVE`, `SIZE` y `RECLAIMABLE`.

**Por qué:** `RECLAIMABLE` es lo que un `prune` podría llevarse. Es la columna que decide si vale la pena.

## Los montones, y quién se lleva cada uno

::: table {#cont-tabla-prune title="Qué se lleva cada uno"}

| Comando | Qué borra | Qué respeta |
|---|---|---|
| `docker container prune` | los contenedores **detenidos** | los que están corriendo |
| `docker image prune` | las **capas huérfanas** (*dangling*) | toda imagen con etiqueta |
| `docker image prune -a` | además, las imágenes **que ningún contenedor usa** | las que tienen un contenedor encima |
| `docker system prune` | contenedores detenidos, capas huérfanas, redes sin uso, caché de build | imágenes etiquetadas y **volúmenes** |
| `docker system prune -a` | todo lo anterior **más** las imágenes que nadie usa | **los volúmenes**, igual |
| `docker volume prune` | los volúmenes **anónimos** sin uso; con `-a`, también los named | los que usa algún contenedor, aunque esté detenido |

:::

- Los volúmenes quedan fuera de `system prune` a propósito: es la única fila donde borrar es **perder un dato**.
- Hay que pedirlo: `docker system prune --volumes`, y aun así sólo se lleva los **anónimos** (lo dice su `--help`).
- Un named volume como `pgdata` de [[named-volumes-y-postgres|2/7]] sólo muere con `docker volume rm` o `docker volume prune -a`.
- **Podman es distinto:** en Podman 4.6, `volume prune` y `system prune --volumes` **sí** se llevan los volúmenes con nombre sin dueño.

## Las capas huérfanas aparecen solas

Basta reconstruir. Usa la carpeta del [[lab-sin-volumen|laboratorio A (2/5)]].

**Haz:**

```bash
cd ~/fdd/docker-lab/lab-a
docker build -q -t app:1 .
docker images app
printf '# un comentario\n' >> app.py
docker build -q -t app:1 .
docker images app
docker images -f dangling=true
```

**Deberías ver:**
- cada `build -q` imprime el `sha256:` de su imagen;
- `docker images app` muestra `app:1` las dos veces, pero con otro `ID`;
- el último comando: al menos un renglón `<untagged>` (según la versión de Docker, `<none>` en repositorio y etiqueta);
- ojo: en Docker 29, `docker images` **sin filtro** ya no muestra la huérfana `<untagged>`. Por eso el `-f dangling=true`.

**Por qué:** la etiqueta `app:1` se movió a la imagen nueva —como una rama de Git al commit nuevo— y la vieja quedó sin nombre, ocupando disco. Para eso existe `docker image prune`.

## Y los contenedores detenidos, también

**Haz:**

```bash
docker run --name detenido alpine:3.20 true
docker ps -a --filter status=exited --format '{{.Names}} {{.Status}}'
```

**Deberías ver:**
- `detenido Exited (0) ...`, junto a todo lo que corriste sin `--rm` en la sección.

**Por qué:** esa lista es exactamente lo que `docker container prune` («Remove all stopped containers») se llevaría. Córrelo **sin** `-f` la primera vez: sin `-f` te pide confirmación, y lees antes de borrar.

## La advertencia del salón

- `docker image prune -a` y `docker system prune -a` se llevan **toda** imagen sin un contenedor encima.
- Eso incluye `python:3.12-slim`, `postgres:16` y `alpine:3.20`, que el prepull de [[instalar-docker-y-podman|2/10]] bajó a propósito.
- Rebajarlas desde la red del ITAM, treinta personas detrás de una sola IP, cuesta más que el disco que recuperaste.

**En el salón, `prune` sin `-a`.** En tu casa, con calma, el que quieras.

::: problem {#cont-p13-cinco-imagenes title="Cinco imágenes, un solo pipeline"}
Crea cinco imágenes de juguete y bórralas **con una sola línea**, sin escribir sus nombres uno por uno.

```bash
for i in 1 2 3 4 5; do
  printf 'FROM alpine:3.20\n' | docker build -q -t "lab-$i" - >/dev/null
done
docker images | grep -E '^lab-'
```

La línea tiene que seleccionar **exactamente** `lab-1` a `lab-5`: si hay una `laboratorio` o una `lab-6`, no se toca. Las piezas: `docker images --format`, un `grep -E` y `xargs`.
:::

::: hint {of="cont-p13-cinco-imagenes"}
`docker images --format '{{.Repository}}:{{.Tag}}'` da una línea por imagen, sin encabezado. A partir de ahí es [[grep-awk-en-serio]]: un patrón anclado en los dos extremos y una clase de caracteres.
:::

::: answer {of="cont-p13-cinco-imagenes"}

```bash
docker images --format '{{.Repository}}:{{.Tag}}' \
  | grep -E '^lab-[1-5]:latest$' \
  | xargs -r docker rmi
```

- **Los dos anclajes son el ejercicio.** Sin `^`, `mi-lab-3` casaría; sin `$`, `lab-1:latest-viejo` también.
- `[1-5]` es una clase de caracteres, no un rango numérico: `lab-12` no casa porque tras el `1` viene un `2` donde el patrón exige `:`.
- `--format` le da a `grep` una columna, no una tabla con encabezado y espacios.
- `xargs` junta las líneas en un solo `docker rmi`. El `-r` evita correrlo sin argumentos si el filtro no encuentra nada. Si tu `xargs` no acepta `-r`, quítalo: el de macOS no corre nada con la entrada vacía.
- Como las cinco comparten el `ID` de `alpine:3.20`, la salida dice `Untagged: lab-1:latest`…: se quitan las etiquetas, la imagen base se queda.
- **En Podman** los builds locales se llaman `localhost/lab-1`: el patrón pasa a ser `^(localhost/)?lab-[1-5]:latest$`.

Comprueba con `docker images | grep -E '^lab-'`. El patrón se repite con contenedores, volúmenes y todo lo que el CLI liste: **una columna, una regex anclada, `xargs`.**
:::

La clase termina aquí; las páginas 2/10 a 2/16 son referencia. Sigue con [[arreglar-un-dockerfile]], la entrega de hoy, que vencía antes de clase.

> [!NOTE]
> **Si sólo recuerdas una cosa:** `docker system df` antes de cualquier `prune`, y los volúmenes se borran aparte porque son la única cosa que no se puede reconstruir.
