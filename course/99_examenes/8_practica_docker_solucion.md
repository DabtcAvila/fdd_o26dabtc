---
id: practica-docker-solucion
title: "Práctica de Docker: clave"
nav_title: "Docker · clave de práctica"
summary: "Las respuestas de la práctica de Docker con una explicación corta de cada una, comprobadas corriendo los comandos: caché, .dockerignore, montajes, volúmenes y cinco errores."
status: ready
estimated_time: 20m
tags: [practica, solucion, docker, dockerfile, dockerignore, volumenes, cache, errores, anexo]
prerequisites: [practica-docker]
---

# Práctica de Docker: clave

**Anexo · Exámenes** · los ejercicios están en [[practica-docker]]. Resuélvelos antes de leer esto.

Cada respuesta se comprobó corriendo los comandos con Docker 29.6. Si tu terminal dice otra cosa, créele a tu terminal y avísale al profesor.

## Ejercicio 1 · Lee el Dockerfile

**a)** **Por la caché.** Docker reusa una capa mientras no cambie nada de lo que esa capa lee. Si `requirements.txt` va solo, el `pip install` depende únicamente de ese archivo: cambias tu código, y la instalación, que es lo lento, sale de la caché. Con un solo `COPY . .` antes del `pip install`, cualquier cambio en cualquier archivo reinstalaría todo.

**b)** `.dockerignore`, `Dockerfile`, `README.md`, `limpiar.py`, `reglas.py` y `requirements.txt`.

`COPY . .` copia todo el contexto **menos** lo que excluye el `.dockerignore`. Por eso no entran `crudos/`, `notas/` ni `salida/`, y sí entran el Dockerfile y el propio `.dockerignore`, que nadie excluyó.

**También vale:** quien agregue `.dockerignore` y `Dockerfile` a su propio `.dockerignore` los deja fuera. Es una buena costumbre, pero aquí no estaba.

**c)**

```bash
docker run --rm -v "$(pwd)/crudos":/app/crudos -v "$(pwd)/salida":/app/salida encuestas:1
```

Un `-v` por cada carpeta. Los dos van **antes** de la imagen, y nada detrás. Después de correrlo, `salida/limpio.csv` está en tu disco.

**También vale:** `$PWD` o `./crudos`, la ruta absoluta, o `--mount type=bind,…`. Ojo: `-v crudos:/app/crudos`, sin `./`, crea un named volume vacío llamado `crudos`, no monta tu carpeta.

**d)** Truena con `FileNotFoundError: … 'crudos/respuestas.csv'`. El `.dockerignore` dejó `crudos/` fuera de la imagen a propósito: los datos se montan al correr, no se hornean. Sin montaje, el archivo no existe dentro del contenedor.

**e)** Las capas van en orden, y cuando una se rehace, todas las que siguen también.

| Cambio | `COPY requirements.txt .` | `RUN pip install` | `COPY . .` |
|---|---|---|---|
| 1. `notas/ideas.md` | caché | caché | caché |
| 2. `reglas.py` | caché | caché | **se rehace** |
| 3. `requirements.txt` | **se rehace** | **se rehace** | **se rehace** |
| 4. `README.md` | caché | caché | **se rehace** |

- **Caso 1.** `notas/` está en el `.dockerignore`: para el build ese archivo no existe, así que nada cambió. Es el caso que más sorprende.
- **Casos 2 y 4.** El archivo entra con `COPY . .`, así que se rehace sólo ese paso. Es más rápido porque `pip` no se repite.
- **Caso 3.** Cambia lo primero que se lee, y todo lo de abajo cae detrás.

**f)** Dos cosas:

1. **`limpio.csv` entra a la imagen.** `salida/` ya no está excluida, así que `COPY . .` copia lo que el programa escribió en tu disco.
2. **El `COPY . .` se rehace cada vez que corres el programa**, porque cada corrida cambia `salida/` y el contexto ya no es el mismo.

Por eso las carpetas de datos y de resultados van en el `.dockerignore`.

**g)** No. Lo que escribes después del nombre de la imagen **reemplaza** al `CMD`. Corre `python reglas.py`, que sólo define cosas y termina sin imprimir nada.

**Repasa:** [[el-dockerfile-por-dentro]], [[capas-y-cache]] y [[rutas-en-docker]].

## Ejercicio 2 · ¿Qué cambió?

La misma pregunta de siempre, fila por fila: ¿este contenedor lee la imagen, una carpeta de tu disco, un volumen o su propia capa de escritura?

| # | Respuesta | Por qué |
|---|---|---|
| 1 | `adios` | `docker stop` detiene el proceso, pero **no borra** el contenedor ni su capa de escritura. `docker start` lo arranca con la misma capa. Sólo `docker rm` la borra. |
| 2 | `hola` | Contenedor nuevo sin montaje: lee la imagen. Lo que pa escribió es de pa. |
| 3 | `luna` | `caja` es un named volume nuevo: Docker lo llenó con el `/s` de la imagen (`hola`), y pb escribió `luna` encima. El otro contenedor monta **el mismo** volumen, así que lee `luna`. |
| 4 | `luna` | La imagen ya dice `sol`, pero `caja` no está vacío: tapa lo que la imagen tiene en `/s`, y Docker no vuelve a llenarlo. |
| 5 | `sol` | Sin montaje, la imagen recién construida. |
| 6 | `luna` | pb sigue montando `caja`. |
| 7 | `sol` | Borraste el volumen. El `caja` de este run es uno **nuevo** y vacío, así que Docker lo llena con la imagen actual, que dice `sol`. |
| 8 | `adios` | pa nunca se tocó. Reconstruir la imagen no cambia los contenedores que ya existen: cada uno se quedó con la imagen con la que nació más su capa. |
| 9 · primero | `nube` | Montaste tu carpeta en `/s`: lee tu disco. |
| 9 · segundo | `sol` | Sin montaje, lee la imagen; no ha habido build desde la fila 4. |
| 10 | se rehace | Tu carpeta cambió (`nube`) desde el último build: el contexto es distinto, así que la caché ya no sirve para el `COPY`. |
| 11 · primero | `x` | Lo que va después de la imagen reemplaza al `CMD`. Ese contenedor escribió en su propia capa y leyó lo que escribió. |
| 11 · segundo | `nube` | Contenedor nuevo, capa nueva: el `x` se fue con el anterior, que tenía `--rm`. La imagen dice `nube` desde el build de la fila 10. |
| 12 | en ningún lado, los dos | `adios` vivía en la capa de pa, y `docker rm` se la llevó. `luna` vivía en el primer `caja`, que borraste en la fila 7. |

**Para recordar:**

- `stop` conserva la capa de un contenedor, y `rm` la borra.
- Un volumen vacío se llena con la imagen. Uno con contenido tapa a la imagen.
- Un build nuevo no cambia los contenedores que ya existen.

**Repasa:** [[ciclo-de-vida-de-un-contenedor]], [[named-volumes-y-postgres]], [[donde-vive-cada-byte]] y [[los-ocho-casos]].

## Ejercicio 3 · Lee el error

| # | Qué pasó | Qué harías |
|---|---|---|
| 1 | Ya existe un contenedor llamado `pa`, y los nombres no se repiten. | Si no lo necesitas, `docker rm -f pa` y vuelve a correr. Si sí, usa otro nombre en `--name`. |
| 2 | Falta el contexto: el `.` final. El build no sabe qué carpeta mandar. | `docker build -t saludo:1 .` |
| 3 | `exec` entra a un contenedor **corriendo**, y pa está detenido. | `docker start pa` y luego el `exec`. Su capa sigue ahí: stop no la borró. |
| 4 | La imagen es Alpine, y Alpine no trae `bash`: trae `sh`. | `docker run --rm -it saludo:1 sh` |
| 5 | El contexto es `proyecto/app/`, y un `COPY` no puede salir de él. Docker busca `datos` **dentro** del contexto y no está. | Construir desde `proyecto/`, con `docker build -t app:1 -f app/Dockerfile .`, y cambiar la línea a `COPY datos /datos`. |

**También vale:**

- En el 5, mover `datos/` dentro de `app/`. Si los datos son grandes o cambian, lo mejor es no copiarlos y montarlos al correr, como en el ejercicio 1.
- En el 4, cualquier imagen que sí traiga `bash`, si de verdad lo necesitas.

**Repasa:** [[anatomia-de-docker-run]], [[ciclo-de-vida-de-un-contenedor]] y [[las-cuatro-trampas]].
