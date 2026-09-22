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

**Página 5 de 13 · sección 2 de 3**

Meta: construir una imagen y ver de qué está hecha, sin creerle nada al `build` que no puedas comprobar.

::: figure {#cont-build-contexto title="Qué se lleva exactamente el punto de `docker build -t mi-imagen .`"}
![Qué se lleva el punto final de docker build con la bandera -t: el directorio entero empaquetado y enviado al daemon como contexto, dibujado como un bulto con el .git y el entorno virtual pesados adentro, y el archivo .dockerignore recortándolos antes del envío. Una flecha aparte marca que la bandera -f cambia qué Dockerfile se lee pero no cambia el contexto, y otra que la bandera --no-cache sólo ignora las capas previas. Al pie, el error de quien escribe la ruta del Dockerfile donde va el contexto](../_assets/cont-build-contexto.svg)
:::

## En corto

- El `.` final de `docker build -t mi-imagen .` **no es «aquí»: es el contexto**, y se empaqueta y se envía entero al daemon.
- `docker history` te enseña la imagen por capas, y ahí se ve qué instrucción pesó.
- `CMD` se deja reemplazar por lo que escribas después de la imagen; `ENTRYPOINT` no — recibe eso como argumentos.

## El punto es el contexto, no «aquí»

`docker build` no lee tu carpeta: **el daemon** construye, y el daemon no ve tu disco. Por eso el CLI empaqueta el directorio que le señalas —el contexto— y se lo manda. El `.` no dice dónde está el `Dockerfile`; dice **qué se envía**.

Eso tiene dos consecuencias inmediatas. La primera la ves en la línea `transferring context: ... MB` del `build`: si en esa carpeta hay un `.git` de 400 MB o un entorno virtual, **eso viaja**, aunque ninguna instrucción lo copie. La segunda es que un `COPY` no puede tomar nada de fuera del contexto; `COPY ../datos .` falla siempre, y el mensaje —`forbidden path outside the build context`— es de los pocos que dicen la verdad completa.

**Haz:** monta el ejemplo de la unidad y mira cuánto viaja.

```bash
cd ~/fdd/docker-lab
cp -r ~/fdd/fdd_o26/codigo/08_contenedores/info .
cd info && ls -a
docker build -t info .
```

**Deberías ver:** las cinco instrucciones del `Dockerfile` ejecutándose, y arriba la línea del contexto con su peso. Si el peso te sorprende, la herramienta es **`.dockerignore`**: mismo formato que `.gitignore`, y recorta **antes** de enviar.

```text
.git
__pycache__/
.venv/
*.csv
```

Dos banderas que se confunden con esto y no son esto: **`-f`** cambia **qué `Dockerfile` se lee** y no toca el contexto —`docker build -f docker/Dockerfile.prod -t app .` sigue enviando el directorio actual—, y **`--no-cache`** sólo ignora las capas previas, para reconstruir desde cero. El error clásico del primer día es escribir `docker build -t info Dockerfile`: ahí le estás diciendo que el **contexto** es un archivo, y contesta que no es un directorio.

## De qué está hecha la imagen que salió

**Haz:** ábrela por capas y pésala contra una base distinta.

```bash
docker history info
docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.Size}}' | grep -E 'info|ubuntu|alpine'
```

**Deberías ver:** en `history`, una fila por capa, de la más nueva a la más vieja, con su `SIZE` y la instrucción que la creó — las que no tocan el sistema de archivos pesan `0B`, y tu imagen pesa casi exactamente lo que pesaba su base. Y en `images`, la diferencia que decide el tamaño de tu entrega: `ubuntu:24.04`, que es la base de `info`, ronda los **78 MB**; `alpine:3.20` ronda los **8 MB**. Un orden de magnitud de diferencia **antes** de que la imagen lleve una sola línea tuya.

Ahí está el consejo de la entrega, con su mecanismo: **el tamaño se elige en la primera línea, no se recorta en la última.** Borrar archivos en un `RUN` posterior no adelgaza la imagen — la capa de abajo sigue ahí, con los bytes dentro, y la de arriba sólo anota que ya no se ven. Y recuerda de [[capas-y-cache|capas y caché]] que cada instrucción es una capa: `history` es, literalmente, tu Dockerfile leído de abajo hacia arriba.

## `CMD` contra `ENTRYPOINT`

Las dos dicen qué corre al arrancar. La diferencia sólo se asoma cuando escribes algo **después** del nombre de la imagen en `docker run`, y ahí se separan del todo:

- Lo que escribes después de la imagen **reemplaza al `CMD`**.
- Lo que escribes después de la imagen **se le agrega al `ENTRYPOINT`** como argumentos.

Leerlo no basta. Constrúyelo.

**Haz:** un script y tres imágenes que sólo difieren en esas dos líneas.

```bash
cd ~/fdd/docker-lab && mkdir -p hola && cd hola
printf '#!/bin/sh\necho "hola, ${1:-mundo}"\n' > hola.sh && chmod +x hola.sh
printf 'FROM alpine:3.20\nWORKDIR /app\nCOPY hola.sh .\nCMD ["./hola.sh"]\n' > D.cmd
printf 'FROM alpine:3.20\nWORKDIR /app\nCOPY hola.sh .\nENTRYPOINT ["./hola.sh"]\n' > D.ent
printf 'FROM alpine:3.20\nWORKDIR /app\nCOPY hola.sh .\nENTRYPOINT ["./hola.sh"]\nCMD ["mundo"]\n' > D.amb
for t in cmd ent amb; do docker build -q -f D.$t -t hola-$t . ; done
```

**Deberías ver:** tres hashes, uno por imagen. El script imprime `hola, ` seguido de su primer argumento, o `mundo` si no recibe ninguno. **No lo corras todavía**: el ejercicio de abajo es predecir, y se arruina solo si miras antes.

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
Para cada una, arma a mano la línea de comando final que acaba corriendo dentro del contenedor y léela como la leería una shell. Hay dos reglas y ninguna excepción: lo que escribes **reemplaza** al `CMD`, y lo que escribes **se le pega detrás** al `ENTRYPOINT`.

En la 4, aplica la segunda regla literalmente y pregúntate qué acabó siendo el argumento `1`.
:::

::: answer {of="cont-s2p5-tres-formas"}
**1. `hola, mundo`.** No escribiste nada, así que corre el `CMD` tal cual y el script no recibe argumentos.

**2. `adios`.** Tu texto **reemplazó** al `CMD` entero: `hola.sh` ni siquiera se ejecutó. Lo que corrió fue `echo adios`, el `echo` de Alpine.

**3. `hola, clase`.** El `ENTRYPOINT` no se puede reemplazar: `clase` se le pegó detrás, así que corrió `./hola.sh clase`.

**4. `hola, echo`.** Aquí está la lección. Se aplicó la misma regla, sin excepción: el comando final fue `./hola.sh echo adios`, o sea `hola.sh` con **dos** argumentos. El script imprime el primero — `echo` — y el segundo se ignora. Tu `echo adios` no corrió como comando: se volvió **datos** para el programa que ya estaba fijado.

**5. `hola, mundo`.** Con los dos, el `CMD` deja de ser «el comando» y pasa a ser **los argumentos por defecto** del `ENTRYPOINT`: corre `./hola.sh mundo`. Y si escribieras `docker run --rm hola-amb clase`, tu palabra reemplaza al `CMD` —que es lo que el `CMD` sabe hacer— y sale `hola, clase`.

La regla de decisión, entonces: **`ENTRYPOINT` cuando la imagen *es* un programa** y quieres que lo que escriba el usuario sean sus argumentos; **`CMD` solo cuando la imagen es un entorno** y quieres poder entrar a hacer otra cosa. Y los dos juntos cuando quieres un programa fijo con argumentos cambiables — que es la forma en que están hechas casi todas las imágenes oficiales que usas.
:::

Sigue con [[arreglar-un-dockerfile]], que te da uno con tres defectos puestos a propósito.

> [!NOTE]
> **Si sólo recuerdas una cosa:** el `.` del `build` es el contexto que viaja entero, y lo que escribes después de la imagen reemplaza al `CMD` pero se le pega detrás al `ENTRYPOINT`.
