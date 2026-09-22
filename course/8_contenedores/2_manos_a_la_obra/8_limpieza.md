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

**Página 13 de 13 · sección 2 de 3**

Meta: recuperar el disco sin borrar lo que no querías borrar.

::: figure {#cont-prune title="Qué se lleva exactamente cada prune"}
![El disco dibujado como cinco montones —imágenes con un contenedor encima, imágenes que nadie usa, contenedores detenidos, capas huérfanas o dangling, y volúmenes sin dueño— cada uno con su tamaño. Debajo, una fila por comando con una marca en la columna que se lleva: docker container prune sólo los contenedores detenidos; docker image prune sólo las capas huérfanas; docker image prune -a además las imágenes que nadie usa; y docker system prune -a las tres del medio. La columna de volúmenes no queda marcada en ninguna de las cuatro filas, con una nota que dice que se piden aparte a propósito, con docker volume prune o con system prune --volumes, porque es la única columna donde borrar es perder un dato y no rehacer un build. Arriba, la salida de docker system df como el comando que mide antes de borrar. Al pie, la advertencia de que nada de esto toca lo que está en uso](../_assets/cont-prune.svg)
:::

## En corto

- **Mide antes de borrar**: `docker system df` te dice cuánto vas a recuperar y de dónde.
- Cada `prune` tiene su columna. Ninguno toca lo que está **en uso**, y ninguno toca los **volúmenes** salvo que se lo pidas aparte.
- Borrar una imagen es rehacer un build; borrar un volumen es perder un dato. No son la misma operación aunque se parezcan los comandos.

## Cuánto está ocupando esto

Después de una sesión como la de hoy —seis imágenes, una docena de contenedores, un par de volúmenes— hay varios gigabytes en tu disco que no aparecen en ninguna carpeta que puedas listar.

**Haz:**

```bash
docker system df
```

**Deberías ver:** cuatro renglones —`Images`, `Containers`, `Local Volumes`, `Build Cache`— con su tamaño total y su columna `RECLAIMABLE`, que es lo que un `prune` podría llevarse. Esa segunda columna es la que decide si vale la pena hacer algo.

## Los cuatro montones

Lo que se acumula no es una sola cosa, y por eso no hay un solo comando.

::: table {#cont-tabla-prune title="Qué se lleva cada uno"}

| Comando | Qué borra | Qué respeta |
|---|---|---|
| `docker container prune` | los contenedores **detenidos** | los que están corriendo |
| `docker image prune` | las **capas huérfanas** (*dangling*) | toda imagen con etiqueta |
| `docker image prune -a` | además, las imágenes **que ningún contenedor usa** | las que sí tienen un contenedor encima |
| `docker system prune` | contenedores detenidos, capas huérfanas, redes sin uso y caché de build | las imágenes etiquetadas y **los volúmenes** |
| `docker system prune -a` | todo lo anterior **más** las imágenes que nadie usa | **los volúmenes**, igual |
| `docker volume prune` | los volúmenes **sin dueño** | los montados por algún contenedor |

:::

Los volúmenes están fuera de los `system prune` a propósito: es la única fila donde borrar es **perder un dato** y no rehacer un build. Para incluirlos hay que escribirlo: `docker system prune --volumes`.

## Las capas huérfanas aparecen solas

No hace falta hacer nada raro para generarlas: basta reconstruir.

**Haz:**

```bash
cd ~/fdd/docker-lab/ocho
docker build -t ocho:1 . >/dev/null
printf '# un comentario\n' >> app.py
docker build -t ocho:1 . >/dev/null
docker images -f dangling=true
```

**Deberías ver:** al menos un renglón con `<none>` en repositorio y etiqueta. Es la imagen anterior: la etiqueta `ocho:1` se movió a la nueva —igual que una rama de Git se mueve al commit nuevo— y la vieja quedó sin nombre, ocupando disco y sin manera de invocarla. Eso es una capa huérfana, y `docker image prune` existe para eso.

## Y los contenedores detenidos, también

**Haz:**

```bash
docker ps -a --format '{{.Names}} {{.Status}}' | head
docker container prune -f
docker ps -a --format '{{.Names}} {{.Status}}'
```

**Deberías ver:** la primera lista con varios `Exited (0)` —todo lo que corriste sin `--rm` durante la sección—, y la tercera con sólo lo que sigue vivo. El `-f` salta la confirmación; la primera vez conviene correrlo sin él y leer lo que propone.

## La advertencia del salón

`docker image prune -a` y `docker system prune -a` se llevan **todas** las imágenes que en ese momento no tengan un contenedor encima. Eso incluye `python:3.12-slim`, `postgres:16` y `alpine:3.20`, que tardaste en bajar y que el prepull de [[instalar-docker-y-podman]] bajó a propósito antes de clase.

Volver a bajarlas desde la red del ITAM, treinta personas a la vez detrás de una sola IP, cuesta bastante más que los gigabytes que recuperaste. **En el salón, `prune` sin `-a`.** En tu casa, con calma, el que quieras.

::: problem {#cont-p13-cinco-imagenes title="Cinco imágenes, un solo pipeline"}
Crea cinco imágenes de juguete y bórralas **con una sola línea**, sin escribir sus nombres uno por uno.

```bash
for i in 1 2 3 4 5; do
  printf 'FROM alpine:3.20\n' | docker build -t "lab-$i" - >/dev/null
done
docker images | grep -E '^lab-'
```

Ahora la línea que las borra. Tiene que seleccionar **exactamente** `lab-1` a `lab-5` y nada más: si en tu máquina hay una imagen llamada `laboratorio` o `lab-6`, no se toca. Las piezas son `docker images --format`, un `grep -E` y `xargs`.
:::

::: hint {of="cont-p13-cinco-imagenes"}
`docker images --format` acepta la misma plantilla que `docker ps`: `--format '{{.Repository}}:{{.Tag}}'` te devuelve una línea por imagen, sin encabezado y sin columnas que estorben. A partir de ahí es [[grep-awk-en-serio]]: un patrón anclado en los dos extremos y una clase de caracteres.
:::

::: answer {of="cont-p13-cinco-imagenes"}

```bash
docker images --format '{{.Repository}}:{{.Tag}}' \
  | grep -E '^lab-[1-5]:latest$' \
  | xargs -r docker rmi
```

Los dos anclajes son el ejercicio entero. Sin el `^`, `mi-lab-3` casaría. Sin el `$` final, `lab-1:latest-viejo` también. `[1-5]` es una clase de caracteres, no un rango numérico: `lab-12` no casa porque después del `1` viene un `2` donde el patrón exige `:`. Y `--format` está ahí para que `grep` reciba una columna, no una tabla: filtrar la salida por defecto de `docker images` te obliga a pelearte con el encabezado y con los espacios.

`xargs` convierte esas líneas en argumentos de un solo `docker rmi`, que acepta varias imágenes de una vez. El `-r` es lo que evita que, si el filtro no encuentra nada, `docker rmi` se ejecute sin argumentos y devuelva un error. En algunas versiones de `xargs` de macOS esa bandera no existe; ahí se quita, porque ese `xargs` ya no corre nada cuando la entrada está vacía.

Comprueba con `docker images | grep -E '^lab-'` que no queda ninguna. Éste es el patrón que vas a repetir con contenedores, con volúmenes y con cualquier cosa que el CLI sepa listar: **listar en una columna, filtrar con una regex anclada, pasar a `xargs`.**
:::

Con esto cierra la sección: los dos runtimes instalados, una imagen propia publicada, y un modelo de dónde vive cada byte que un contenedor escribe. Sigue con [[disenar-con-contenedores]], donde la pregunta deja de ser *cómo corro este contenedor* y pasa a ser *cuántos contenedores son, y cómo se hablan entre ellos*.

> [!NOTE]
> **Si sólo recuerdas una cosa:** `docker system df` antes de cualquier `prune`, y los volúmenes se borran aparte porque son la única cosa que no se puede reconstruir.
