---
id: named-volumes-y-postgres
title: "Named volumes y Postgres"
nav_title: "Named volumes y Postgres"
summary: "Bind mount para tu código, named volume para datos de servicios. Ver el estado sobrevivir a su contenedor, y después morir con su volumen."
status: ready
estimated_time: 15m
tags: [named-volume, postgres, psql, estado, persistencia, uid]
prerequisites: [las-cuatro-trampas]
---

# Named volumes y Postgres

**Página 12 de 13 · sección 2 de 3**

Meta: ver con los ojos que el estado no vive en el contenedor, sino al lado.

::: figure {#cont-estado-postgres title="El estado sobrevive a su contenedor"}
![Cuatro tiempos de la misma línea, de izquierda a derecha. Primero, un contenedor postgres:16 con un named volume llamado pgdata montado en /var/lib/postgresql/data y una tabla con su fila recién insertada. Segundo, el contenedor destruido con docker rm -f: se va su capa de escritura y su nombre, y el volumen queda solo en el dibujo con la fila adentro. Tercero, un contenedor nuevo que monta el mismo volumen y devuelve la misma fila, sin inicializar nada. Cuarto, docker volume rm, el único de los cuatro comandos que se lleva el dato, sin deshacer. Al pie, dos recuadros: uno explica que aquí no se publica ningún puerto y que se entra con docker exec, y el otro por qué el volumen es named y no bind mount, por el uid 999 de Postgres y por la portabilidad entre sistemas operativos](../_assets/cont-estado-postgres.svg)
:::

## En corto

- **Bind mount para tu código; named volume para datos de servicios.** Es la regla que decide casi siempre.
- El named volume es un directorio que administra el runtime: no eliges dónde vive, y por eso funciona igual en Linux, macOS y Windows.
- Un contenedor es desechable **porque el dato no vive en él**. Cuál de los dos borras no es un detalle: es la diferencia entre rehacer y perder.

## Los dos montajes, y cuándo cada uno

Ya usaste bind mounts toda la sección: un path de tu disco, montado adentro. Un **named volume** es lo otro: le das un nombre, y el runtime decide dónde guardarlo.

::: table {#cont-tabla-dos-montajes title="Bind mount y named volume, lado a lado"}

| | Bind mount | Named volume |
|---|---|---|
| Se escribe | `-v "$(pwd)":/app` | `-v pgdata:/var/lib/postgresql/data` |
| Quién decide dónde vive | tú | el runtime |
| Portable entre sistemas operativos | no: la ruta cambia | sí: el comando es idéntico |
| Sobre un path con contenido | tapa | copia la primera vez |
| Muere con | `rm` de tu carpeta | `docker volume rm` |
| Para qué | **tu código, mientras lo editas** | **los datos de un servicio** |

:::

El CLI que vas a usar es corto —`docker volume create`, `ls`, `inspect` y `rm`—; la lista completa, con su equivalente de Podman, vive en la chuleta.

## Por qué una base de datos quiere un named volume

Dos razones, y ninguna es de gusto.

**El uid.** La imagen oficial de Postgres corre como el usuario `postgres`, que adentro es el **uid 999**. Si le montas un bind mount a una carpeta tuya, ese 999 no tiene permiso de escribir ahí —los permisos son números, como en [[las-cuatro-trampas]]— y el contenedor muere al arrancar. El named volume lo crea el runtime con el dueño correcto.

**La portabilidad.** `-v pgdata:/var/lib/postgresql/data` es la misma línea en Linux, en macOS y en Windows. Un bind mount no: la ruta cambia, y en macOS y Windows además cruza la frontera de una VM.

::: definition {#cont-def-psql title="`psql`"}
**`psql`** es el cliente de línea de comandos de PostgreSQL: se conecta a una base y ejecuta SQL. Con `-c 'SELECT …'` corre una sola sentencia y sale; sin `-c` abre una sesión interactiva.
:::

## Tiempo 1: la base, con su volumen

**Haz:**

```bash
docker volume create pgdata
docker run -d --name pg -e POSTGRES_PASSWORD=fdd \
  -v pgdata:/var/lib/postgresql/data postgres:16
until docker exec pg pg_isready -q; do sleep 1; done
docker exec pg psql -U postgres -c 'CREATE TABLE notas (id serial PRIMARY KEY, nombre text);'
docker exec pg psql -U postgres -c "INSERT INTO notas (nombre) VALUES ('ada');"
docker exec pg psql -U postgres -c 'SELECT * FROM notas;'
```

**Deberías ver:** `CREATE TABLE`, después `INSERT 0 1`, y por último la tabla con su única fila, `1 | ada`.

**Aquí no publicamos ningún puerto.** No hay `-p` en ese `docker run`, y sin embargo entraste: por `docker exec`, que es la puerta que ya existía. Publicar un puerto habría puesto esta base en tu red local sin que nadie lo necesitara. Que eso sea una decisión y no un atajo se explica en [[la-red-y-el-nombre]].

## Tiempo 2: destruir el contenedor, resucitar los datos

**Haz:**

```bash
docker rm -f pg
docker volume ls | grep pgdata
docker run -d --name pg2 -e POSTGRES_PASSWORD=fdd \
  -v pgdata:/var/lib/postgresql/data postgres:16
until docker exec pg2 pg_isready -q; do sleep 1; done
docker exec pg2 psql -U postgres -c 'SELECT * FROM notas;'
```

**Deberías ver:** el volumen sigue listado, y `pg2` devuelve **la misma fila**. Fíjate en `docker logs pg2`: no aparece la inicialización que sí hizo `pg`. Encontró el directorio de datos ya hecho —es la copia de [[las-cuatro-trampas]], que ocurrió una sola vez— y arrancó sobre él.

Lo que murió con `docker rm -f` fue la capa de escritura del contenedor y su nombre. El `estado` estaba en otro lado, que es la idea entera de [[escalamiento-y-orquestacion]] puesta a prueba.

## Tiempo 3: y ahora sí, matarlos

**Haz:**

```bash
docker rm -f pg2
docker volume rm pgdata
docker run -d --name pg3 -e POSTGRES_PASSWORD=fdd \
  -v pgdata:/var/lib/postgresql/data postgres:16
until docker exec pg3 pg_isready -q; do sleep 1; done
docker exec pg3 psql -U postgres -c 'SELECT * FROM notas;'
```

**Deberías ver:** `ERROR:  relation "notas" does not exist`. El `docker run` volvió a crear un volumen llamado `pgdata` —Docker lo hace solo, sin avisar—, pero es uno nuevo y vacío, y Postgres lo inicializó desde cero. De los cuatro comandos de esta página, `docker volume rm` es el único que borró un dato. Y no hay deshacer.

Limpia antes de seguir: `docker rm -f pg3 && docker volume rm pgdata`.

::: problem {#cont-p12-postgres-17 title="Un volumen de la 16, un servidor de la 17"}
Tienes un volumen inicializado por `postgres:16` y quieres actualizar: mismo volumen, imagen nueva.

```bash
docker volume create pg16data
docker run -d --name v16 -e POSTGRES_PASSWORD=fdd \
  -v pg16data:/var/lib/postgresql/data postgres:16
until docker exec v16 pg_isready -q; do sleep 1; done
docker rm -f v16
docker run -d --name v17 -e POSTGRES_PASSWORD=fdd \
  -v pg16data:/var/lib/postgresql/data postgres:17
docker logs v17
```

**Predice antes de correrlo:** ¿arranca `v17`? Si no, ¿qué lo impide, y por qué el mecanismo de esta página no lo resuelve?
:::

::: hint {of="cont-p12-postgres-17"}
El volumen no guarda «tus tablas»: guarda el **directorio de datos** de PostgreSQL, con su formato en disco. Pregúntate quién escribió ese formato, y si el servidor nuevo tiene alguna manera de saber que le sirve.
:::

::: answer {of="cont-p12-postgres-17"}
**No arranca.** `docker ps -a` lo muestra `Exited`, y `docker logs v17` trae el mensaje, literal:

```text
FATAL:  database files are incompatible with server
DETAIL:  The data directory was initialized by PostgreSQL version 16,
         which is not compatible with this version 17.x.
```

(El número de parche depende de la imagen del día; lo demás es palabra por palabra.)

El volumen hizo su trabajo **perfectamente**: entregó intacto el directorio de datos. El problema es que ese directorio tiene un formato en disco que cambia entre versiones mayores de PostgreSQL, y el servidor 17 se niega a tocarlo en vez de corromperlo. La negativa es la característica, no el fallo.

La lección general, que vale para cualquier servicio con estado: **un named volume preserva bytes, no compatibilidad.** Actualizar de mayor a mayor pide una migración explícita —`pg_upgrade`, o un `pg_dump` de la 16 restaurado en la 17—, y es un procedimiento, no una bandera.

Limpia: `docker rm -f v17 && docker volume rm pg16data`.
:::

Sigue con [[limpieza-de-docker]], porque todo esto dejó basura en tu disco.

> [!NOTE]
> **Si sólo recuerdas una cosa:** el contenedor es desechable porque el dato no está adentro; borrar el contenedor es rehacer, borrar el volumen es perder.
