---
id: el-dockerfile-por-dentro
title: "El Dockerfile por dentro"
nav_title: "El Dockerfile por dentro"
summary: "Qué se lleva el punto de docker build, de qué capas está hecha la imagen que sale, y la diferencia entre CMD y ENTRYPOINT."
status: ready
estimated_time: 15m
tags: [dockerfile, build, contexto, dockerignore, history, cmd, entrypoint, alpine]
prerequisites: [ciclo-de-vida-de-un-contenedor]
---

# El Dockerfile por dentro

**Página 3 de 16 · sección 2 de 3**

Meta: construir una imagen y ver de qué está hecha, sin creerle nada al `build` que no puedas comprobar.

::: figure {#cont-build-contexto title="Qué se lleva exactamente el punto de `docker build -t mi-imagen .`"}
![Qué significa el punto final de docker build con la bandera -t: el directorio que hace de contexto, el único lugar de donde el build puede leer. A la izquierda, la carpeta con app.py y requirements.txt livianos y el .git, el entorno virtual y los datos crudos pesados; en medio, .dockerignore como un colador que los recorta; a la derecha, lo que llega al daemon, que con BuildKit pide sólo lo que nombran los COPY: con COPY punto punto es todo el directorio menos lo recortado. Un COPY de ../datos falla con failed to compute cache key, not found. Al pie, tres notas: la bandera -f cambia qué Dockerfile se lee pero no el contexto, --no-cache sólo ignora las capas previas, y quien escribe la ruta del Dockerfile donde va el contexto recibe unable to prepare context, path not found](../_assets/cont-build-contexto.svg)
:::

## En corto

- El `.` final de `docker build -t mi-imagen .` **no es «aquí»: es el contexto**; viaja al daemon lo que tus `COPY` piden, y con `COPY . .` es todo.
- `docker history` te enseña la imagen por capas, y ahí se ve qué instrucción pesó.
- `CMD` se deja reemplazar por lo que escribas después de la imagen; `ENTRYPOINT` no — recibe eso como argumentos.

## El punto es el contexto, no «aquí»

- **El daemon construye** y no ve tu disco: el `.` le dice de qué carpeta puede pedir archivos —**el contexto**—, no dónde está el `Dockerfile`.
- **Viaja lo que tus `COPY` piden.** Con `COPY . .` —el patrón común, y el de la entrega 2/9— eso es **todo**, incluidos `.git` y `.venv`. Por eso existe `.dockerignore`.
- **Nada de fuera entra.** En `COPY ../datos .` el `..` se recorta a la raíz del contexto: sin `datos/` adentro falla con `"/datos": not found`; **con** un `datos/` dentro del contexto, copia **ése** sin error. Ésa es la trampa.

**Haz:** una carpeta con 50 MB de relleno y un `COPY . .`; construye, ignora el relleno, construye otra vez.

```bash
mkdir -p ~/fdd/docker-lab/peso && cd ~/fdd/docker-lab/peso
printf 'FROM alpine:3.20\nWORKDIR /app\nCOPY . .\n' > Dockerfile
head -c 50M /dev/zero > relleno.bin
docker build -t peso . 2>&1 | grep -A1 'load build context'
echo relleno.bin > .dockerignore
docker build -t peso . 2>&1 | grep -A1 'load build context'
```

**Deberías ver:** bajo `load build context`, la línea `transferring context:` con su peso:
- el primer `build`: `52.44MB` — el relleno viajó entero;
- el segundo: `81B` — `.dockerignore` lo recortó **antes** de enviar.

Ese número es de la **primera** transferencia: si repites un `build` sin cambios, sólo viaja la diferencia (unos bytes). Con el builder viejo, sin BuildKit, sí se mandaba la carpeta entera siempre. Un `.dockerignore` típico, con el formato de `.gitignore`, un patrón por línea: `.git`, `.venv/`, `__pycache__/`, `*.csv`.

## Las banderas que se confunden con el punto

| Lo que escribes | Qué cambia | Qué **no** cambia |
|---|---|---|
| `.` (el último argumento) | de qué carpeta se pueden copiar archivos | dónde se busca el `Dockerfile` (por defecto, adentro de esa carpeta) |
| `-f docker/Dockerfile.prod` | qué `Dockerfile` se lee | el contexto: sigue siendo el `.` |
| `--no-cache` | ignora las capas previas: `COPY` y `RUN` se vuelven a ejecutar | el contexto, el `Dockerfile` y el nombre |
| `-t peso` | el nombre con el que queda la imagen | nada de lo que se construye |

**Haz:** comete a propósito el error clásico del primer día, en la misma carpeta: `docker build -t peso Dockerfile`.

**Deberías ver:** `ERROR: failed to build: unable to prepare context: path "Dockerfile" not found`. Dice *not found* aunque el archivo está ahí: buscaba una carpeta, porque ahí va el contexto.

> [!TIP]
> En Podman los mensajes cambian: `context must be a directory` para este error, `possible escaping context directory error` para el `COPY ../`, y `podman build -q` imprime el hash sin el prefijo `sha256:`.

## De qué está hecha la imagen

**Haz:** construye el ejemplo de la unidad, ábrelo por capas y pésalo contra otra base.

```bash
cd ~/fdd/docker-lab && cp -r ~/fdd/fdd_o26/codigo/08_contenedores/info .
cd info && docker build -q -t info .
docker history info
docker images --format '{{.Repository}}:{{.Tag}}  {{.Size}}' | grep -E '^(info|ubuntu|alpine):'
```

**Deberías ver:**
- en `history`, una fila por capa, **de la más nueva a la más vieja**, con su `SIZE` y la instrucción que la creó;
- `CMD` y `WORKDIR` pesan `0B`; `COPY` y `RUN` pesan `341B` cada una; la capa `ADD file:...` de la base, `78.2MB`;
- en `images`, al menos estas tres filas: `info:latest  78.2MB`, `ubuntu:24.04  78.2MB`, `alpine:3.20  7.81MB`.

**Lo que se lee ahí:**
- **Tu imagen pesa lo que su base.** Tus cuatro instrucciones, además del `FROM`, no suman ni un KB.
- **El tamaño se elige en la primera línea**: Alpine es un orden de magnitud menos antes de una sola línea tuya.
- **Una capa posterior no adelgaza la de abajo.** `RUN chmod` sólo cambió un permiso y aun así pesa `341B`: guardó otra copia entera de `info.sh`. Un `RUN rm` igual: la capa de abajo conserva los bytes.
- `history` es tu Dockerfile leído de abajo hacia arriba (repaso: [[capas-y-cache|capas y caché]]).

## `CMD` contra `ENTRYPOINT`

Las dos dicen qué corre al arrancar. Se separan sólo cuando escribes algo **después** del nombre de la imagen en `docker run`:

- Lo que escribes después de la imagen **reemplaza al `CMD`**.
- Lo que escribes después de la imagen **se le agrega al `ENTRYPOINT`** como argumentos.

**Haz:** un script y tres imágenes que sólo difieren en esas dos líneas.

```bash
cd ~/fdd/docker-lab && mkdir -p hola && cd hola
printf '#!/bin/sh\necho "hola, ${1:-mundo}"\n' > hola.sh && chmod +x hola.sh
printf 'FROM alpine:3.20\nWORKDIR /app\nCOPY hola.sh .\nCMD ["./hola.sh"]\n' > D.cmd
printf 'FROM alpine:3.20\nWORKDIR /app\nCOPY hola.sh .\nENTRYPOINT ["./hola.sh"]\n' > D.ent
printf 'FROM alpine:3.20\nWORKDIR /app\nCOPY hola.sh .\nENTRYPOINT ["./hola.sh"]\nCMD ["mundo"]\n' > D.amb
for t in cmd ent amb; do docker build -q -f D.$t -t hola-$t . ; done
```

**Deberías ver:** tres líneas `sha256:...`, una por imagen.
- El script imprime `hola, ` y su primer argumento, o `mundo` si no recibe ninguno.
- **No lo corras todavía**: el ejercicio es predecir, y se arruina si miras antes.

::: problem {#cont-s2p5-tres-formas title="Escribe qué imprime cada una, y luego corre"}
Las tres imágenes se construyeron del mismo `hola.sh`. Cambia una línea: `CMD`, `ENTRYPOINT`, o los dos.

**Escribe tu predicción de las cinco líneas antes de teclear.** Palabra por palabra, incluida la coma.

```bash
docker run --rm hola-cmd                # 1
docker run --rm hola-cmd echo adios     # 2
docker run --rm hola-ent clase          # 3
docker run --rm hola-ent echo adios     # 4
docker run --rm hola-amb                # 5
```

Después córrelas y cuenta cuántas acertaste. La 4 es la que casi nadie predice bien; cuando la veas, explica **por qué** el resultado es ése y no `adios`.
:::

::: hint {of="cont-s2p5-tres-formas"}
Para cada una, arma a mano el comando final que corre dentro del contenedor y léelo como una shell. Dos reglas, ninguna excepción:
- lo que escribes **reemplaza** al `CMD`;
- lo que escribes **se le pega detrás** al `ENTRYPOINT`.

En la 4, aplica la segunda regla literalmente y pregúntate qué acabó siendo el argumento `1`.
:::

::: answer {of="cont-s2p5-tres-formas"}
**1. `hola, mundo`.** No escribiste nada, así que corre el `CMD` tal cual y el script no recibe argumentos.

**2. `adios`.** Tu texto **reemplazó** al `CMD` entero: `hola.sh` ni siquiera se ejecutó. Lo que corrió fue `echo adios`, el `echo` de Alpine.

**3. `hola, clase`.** El `ENTRYPOINT` no se puede reemplazar: `clase` se le pegó detrás, así que corrió `./hola.sh clase`.

**4. `hola, echo`.** Aquí está la lección, con la misma regla sin excepción:
- el comando final fue `./hola.sh echo adios`: `hola.sh` con **dos** argumentos;
- el script imprime el primero —`echo`— e ignora el segundo;
- tu `echo adios` no corrió como comando: se volvió **datos** para el programa ya fijado.

**5. `hola, mundo`.** Con los dos, el `CMD` deja de ser «el comando» y pasa a ser **los argumentos por defecto** del `ENTRYPOINT`: corre `./hola.sh mundo`. Y si escribieras `docker run --rm hola-amb clase`, tu palabra reemplaza al `CMD` —que es lo que el `CMD` sabe hacer— y sale `hola, clase`.

La regla de decisión:
- **`ENTRYPOINT`** cuando la imagen *es* un programa: lo que escriba el usuario son sus argumentos.
- **`CMD`** solo cuando la imagen es un entorno y quieres poder entrar a hacer otra cosa.
- **Los dos** cuando quieres un programa fijo con argumentos cambiables: así están hechas casi todas las imágenes oficiales que usas.
:::

Sigue con [[donde-vive-cada-byte]]: ya sabes qué hay en la imagen; falta saber dónde cae lo que escribe el contenedor.

> [!NOTE]
> **Si sólo recuerdas una cosa:** el `.` del `build` es el contexto, del que viaja lo que tus `COPY` piden (con `COPY . .`, todo), y lo que escribes después de la imagen reemplaza al `CMD` pero se le pega detrás al `ENTRYPOINT`.
