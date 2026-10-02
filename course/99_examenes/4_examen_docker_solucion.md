---
id: examen-docker-solucion
title: "Examen de Docker: solución"
nav_title: "Docker · solución"
summary: "La solución del examen de Docker, versiones A y B, inciso por inciso y casilla por casilla: la respuesta, por qué es ésa, qué otras formas valían y cómo comprobarlo en tu terminal."
status: ready
estimated_time: 25m
tags: [examen, solucion, docker, dockerfile, volumenes, cache, anexo]
prerequisites: [examen-docker-enunciado]
---

# Examen de Docker: solución

**Anexo · Exámenes** · el enunciado está en [[examen-docker-enunciado]]. Contéstalo antes de leer esto.

Cada respuesta de aquí se comprobó corriendo los comandos con Docker 29.6, desde cero. Tú puedes hacer lo mismo: crea la carpeta, escribe el Dockerfile y el archivo de texto, y corre la secuencia. Lo que imprima tu terminal es la autoridad, no esta página. Al terminar, borra lo que creaste: los contenedores, las imágenes `nota:1` o `color:1` y el volumen `almacen` o `bodega`.

## Cómo se calificó

- **Ejercicio 1**: 4 puntos. Los huecos a–d valen 0.25 cada uno; los incisos e–j, 0.5 cada uno.
- **Ejercicio 2**: 6 puntos, 12 casillas de 0.5.
- Es a mano: no se descuenta por comillas ni espacios, ni por escribir `$(pwd)`, `$PWD` o `./`. Se descuenta cuando el comando haría otra cosa.
- En `docker run` el orden de las opciones no importa mientras vayan **antes** del nombre de la imagen. Lo que va después de la imagen ya es el comando que corre el contenedor.
- En el ejercicio 2 cada casilla se califica contra el estado **correcto** de la fila anterior, no contra lo que contestaste antes. «error» valía cero en todas: ningún comando del ejercicio falla.

Las dos versiones miden lo mismo. Si entiendes por qué una respuesta de la A es la que es, la B sale igual; por eso aquí se explica a fondo la A y la B va más corta, señalando sólo dónde cambia.

## Versión A · 1. Del repo a la imagen

El Dockerfile completo:

```dockerfile
FROM python:3.12-slim
WORKDIR /clima
COPY requirements.txt /clima/
RUN pip install -r requirements.txt
COPY app /clima/app
CMD ["python", "app/main.py"]
```

### a) `WORKDIR`

**Respuesta:** `/clima`

**Por qué.** `WORKDIR` fija la carpeta donde corre todo lo que sigue, en el build (`RUN`, el `.` de un `COPY`) y al arrancar el contenedor (`CMD`). Si no existe, la crea. El enunciado pide trabajar en `/clima`.

**También valía:** `/clima/`. Una ruta relativa valía cero.

### b) Destino del primer `COPY`

**Respuesta:** `/clima/`

**Por qué.** El destino es dentro de la imagen y el enunciado lo pide absoluto. Con la barra final, Docker lo trata como carpeta y deja el archivo como `/clima/requirements.txt`, justo donde el `RUN pip install -r requirements.txt` lo busca, porque el `WORKDIR` es `/clima`.

**También valía:** `/clima/requirements.txt`, y también `/clima` sin barra: la carpeta ya existe porque la creó el `WORKDIR`, y Docker copia el archivo adentro (comprobado). `.` o `./` también funcionan, por el `WORKDIR`, pero el enunciado pedía ruta absoluta: valían una fracción.

**Repasa:** [[el-dockerfile-por-dentro]] y [[rutas-en-docker]].

### c) Origen del segundo `COPY`

**Respuesta:** `app`

**Por qué.** El origen se lee **del contexto del build**, que es `clima/`. Desde ahí, la carpeta del programa se llama `app`. Copia `main.py` y `utils.py` a `/clima/app`.

**También valía:** `app/` o `./app`.

**No valía:**

- `.`, porque copia todo el contexto: mete `data/` y `README.md`, que el enunciado deja fuera, y anida mal (`/clima/app/app/main.py`).
- Rutas que salen del contexto (`clima/app`, `../app`, una ruta absoluta de tu máquina). El build sólo ve lo que hay dentro del contexto.

### d) `CMD`

**Respuesta:** `["python", "app/main.py"]`

**Por qué.** `CMD` es lo que corre al **arrancar** un contenedor, no durante el build. Como el `WORKDIR` es `/clima`, la ruta relativa `app/main.py` apunta a `/clima/app/main.py`. Hace falta el intérprete: un `.py` no se ejecuta solo.

**También valía:** `["python", "/clima/app/main.py"]`, `python3`, y la forma shell `CMD python app/main.py`.

**No valía:** `["app/main.py"]` sin intérprete, ni `RUN` en lugar de `CMD`. `RUN` correría el programa una vez durante el build y el contenedor no haría nada al arrancar.

**Repasa:** [[receta-imagen-contenedor]].

### e) Construir

**Respuesta:** `docker build -t clima:1 .`

**Por qué.** `-t clima:1` le pone nombre y etiqueta a la imagen. El `.` final es el **contexto**: la carpeta cuyos archivos puede ver el build, en este caso `clima/`.

**Errores típicos:** sin el `.` final el comando falla, porque el build exige un contexto (cero). Sin `-t clima:1` construye una imagen sin nombre (la mitad).

### f) Correr con los datos montados

**Respuesta:** `docker run --rm -v "$(pwd)/data":/clima/data clima:1`

**Por qué.**

- `--rm` borra el contenedor al terminar.
- `-v ruta-de-tu-máquina:ruta-del-contenedor` es un **bind mount**: tu carpeta `data/` aparece dentro del contenedor en `/clima/data`. Lo que el programa lea o escriba ahí es tu disco.
- La imagen va al final y **nada** detrás, porque lo que va detrás reemplaza al `CMD`.

**También valía:** `$PWD/data`, `./data`, la ruta absoluta, sin comillas si la ruta no tiene espacios, o `--mount type=bind,src="$(pwd)/data",dst=/clima/data`.

**La trampa:** `-v data:/clima/data`, sin `./` ni ruta, **no** monta tu carpeta. Un nombre sin `/` es un **named volume**: Docker crea un volumen vacío llamado `data`, y el programa no encuentra `clima.csv` (comprobado: `FileNotFoundError`). Una opción escrita después de la imagen tampoco funciona: se vuelve parte del comando.

**Repasa:** [[lab-con-volumen]] y [[anatomia-de-docker-run]].

### g) Una terminal en un contenedor nuevo

**Respuesta:** `docker run --rm -it clima:1 bash`

**Por qué.** `bash` después de la imagen reemplaza al `CMD`: en vez del programa, arranca una shell. `-it` le da a esa shell una terminal y le conecta tu teclado. Sin eso, `bash` no tiene de dónde leer y termina en el acto.

**También valía:** `-i -t` separados, o `--entrypoint bash`.

**Errores típicos:** sin `-it`, bash termina al instante. Sin `bash`, corre el programa en vez de una shell. Sin `--rm`, funciona pero el contenedor queda guardado. `docker exec` valía cero: entra a un contenedor que **ya** está corriendo, y aquí no hay ninguno y se pedía uno nuevo.

### h) ¿Qué queda dentro de la imagen?

**Respuesta:** sólo `requirements.txt`, `app/main.py` y `app/utils.py`.

**Por qué.** A la imagen entra lo que un `COPY` mete, nada más. El Dockerfile no se copia a sí mismo, `README.md` no lo copia nadie, y `data/` se monta al correr, sin entrar a la imagen.

### i) Build desde `clima/app/`

**Respuesta:** **no termina bien.** Falla en un `COPY` con `"/requirements.txt": not found` o `"/app": not found` (comprobado).

**Por qué.** El `.` es el contexto, y parado en `app/` el contexto es `clima/app/`. Ahí no hay `requirements.txt`, ni una carpeta `app/` adentro. `-f ../Dockerfile` sólo dice qué archivo de instrucciones leer; **no** mueve el contexto. Las rutas de origen de un `COPY` se leen del contexto, no de donde está el Dockerfile.

**También valía:** correrlo desde `clima/app/` con `..` como contexto (`docker build -t clima:1 -f ../Dockerfile ..`) sí funciona, y explicarlo así demostraba el mismo entendimiento. «No encuentra el Dockerfile» valía poco: `-f ../Dockerfile` sí lo encuentra.

**Repasa:** [[rutas-en-docker]].

### j) ¿Dónde queda lo que escribe el programa?

**Respuesta.**

- `/clima/data/resumen.csv` existe en **tu carpeta `data/`**: `/clima/data` era tu carpeta montada, y borrar el contenedor no toca tu disco.
- `/clima/resumen.csv` **no existe en ningún lado**: cayó en la capa de escritura del contenedor, que se borra con él.

**Por qué.** Un contenedor escribe en dos sitios posibles: en un montaje, que vive fuera de él, o en su **capa de escritura**, que es suya y muere con él. Nunca escribe en la imagen: la imagen es de sólo lectura. «En la imagen» valía cero.

**Repasa:** [[donde-vive-cada-byte]].

## Versión A · 2. ¿Qué cambió?

Tres lugares distintos guardan un `nota.txt`, y casi todo el ejercicio consiste en no confundirlos:

| Lugar | Cambia cuando… |
|---|---|
| Tu carpeta `lab/` | lo editas tú, o un contenedor que la tenga montada escribe en ella |
| La imagen `nota:1` | corres `docker build`, que copia lo que hay en tu carpeta en ese momento |
| La capa de escritura de cada contenedor | ese contenedor escribe en una ruta que no está montada |

Un contenedor nuevo arranca leyendo la imagen. Un montaje tapa lo que la imagen tiene en esa ruta.

**Repasa:** [[lab-sin-volumen]], [[lab-con-volumen]], [[el-archivo-compartido]] y [[los-ocho-casos]].

### Fila 1 · `uno`

c1 no tiene nada montado, así que `echo dos > nota.txt` escribió en **su** capa de escritura. Tu carpeta no se enteró.

**Compruébalo:** `cat nota.txt` en `lab/`.

### Fila 2 · caché

El `COPY` sale de la caché. El build lee **tu carpeta**, y ahí `nota.txt` sigue diciendo `uno`: el contexto no cambió. Lo que hay dentro de c1 no es parte del contexto.

**Valía:** «caché», «CACHED» o «no se ejecuta», con un porqué que diga que el build lee tu carpeta y no el contenedor. «Se vuelve a ejecutar» valía cero.

**Compruébalo:** `docker build --progress=plain -t nota:1 .` imprime `CACHED` debajo del paso `COPY`.

**Repasa:** [[capas-y-cache]].

### Fila 3 · run: `uno` · exec: `dos`

- **run:** un contenedor nuevo lee la imagen, y la imagen tiene `uno`. Editaste tu carpeta (`tres`), pero sin un build la imagen no se entera.
- **exec:** c1 sigue vivo y conserva su capa de escritura, donde dice `dos`.

### Fila 4 · `tres`

Ahora sí hubo build: copió el `nota.txt` de tu carpeta, que dice `tres`. El contenido cambió, así que el `COPY` ya no sale de la caché.

### Fila 5 · `cuatro`

c2 tiene tu carpeta montada en `/w`, y el `WORKDIR` es `/w`. Escribir `nota.txt` dentro de c2 es escribir en tu disco.

### Fila 6 · `tres`

Contenedor nuevo, sin montaje: lee la imagen. La imagen no cambia por lo que pase en tu carpeta; el último build fue el de la fila 4.

### Fila 7 · `cinco`

El montaje funciona en las dos direcciones. Escribiste `cinco` en tu carpeta, y c2 lo ve al instante, sin build ni reinicio, porque lee tu disco.

### Fila 8 · en ningún lado

`dos` sólo vivía en la capa de escritura de c1, y `docker rm` se la llevó. A estas alturas tu carpeta dice `cinco` y la imagen dice `tres`.

### Fila 9 · `seis`

También se puede montar **un archivo** suelto. `extra.txt` de tu máquina aparece en `/w/nota.txt` y tapa al de la imagen; el `cat` lee el montado.

### Fila 10 · `cinco`

Dos cosas pasan en esta fila:

1. El build copia tu carpeta, que dice `cinco`. La imagen ahora dice `cinco`.
2. `-v almacen:/w` es un **named volume** que no existía. Docker lo crea, y como está **vacío**, primero le copia lo que la imagen tiene en `/w`. El `cat` lee `cinco`.

**Repasa:** [[named-volumes-y-postgres]].

### Fila 11 · `cinco`

La imagen ya dice `siete`, pero `almacen` ya **no** está vacío: guardó `cinco` la primera vez. Un volumen con contenido tapa lo que la imagen tiene en esa ruta, y Docker no lo vuelve a llenar. Por eso un volumen sobrevive a una imagen nueva: es lo que permite actualizar una base de datos sin perder sus datos.

**Compruébalo:** `docker run --rm -v almacen:/w alpine:3.20 cat /w/nota.txt` también imprime `cinco`.

## Versión B · 1. Del repo a la imagen

La misma lógica que la A, con `ventas/`, `src/` y los datos en `/datos`. **Cuidado:** aquí f) es la terminal y g) es el montaje, al revés que en la A.

```dockerfile
FROM python:3.12-slim
WORKDIR /ventas
COPY requirements.txt /ventas/
RUN pip install -r requirements.txt
COPY src /ventas/src
CMD ["python", "src/cargar.py"]
```

| Inciso | Respuesta | También valía · no valía |
|---|---|---|
| a | `/ventas` | `/ventas/`. Relativa: no. |
| b | `/ventas/` | `/ventas/requirements.txt`, `/ventas`. `.` o `./` funcionan, pero el enunciado pedía absoluta. |
| c | `src` | `src/`, `./src`. `.` mete `entrada/` y `README.md`, y anida mal. |
| d | `["python", "src/cargar.py"]` | `/ventas/src/cargar.py`, `python3`, forma shell. Sin intérprete o con `RUN`: no. |
| e | `docker build -t ventas:1 .` | Sin el `.`: falla. Sin `-t`: imagen sin nombre. |
| f | `docker run --rm -it ventas:1 bash` | `-i -t`, `--entrypoint bash`. `docker exec`: no, no hay contenedor vivo. |
| g | `docker run --rm -v "$(pwd)/entrada":/datos ventas:1` | `$PWD`, `./entrada`, ruta absoluta, `--mount type=bind`. `-v entrada:/datos` es un named volume vacío: no encuentra `enero.csv`. |
| h | `requirements.txt`, `src/cargar.py`, `src/formatos.py` | Ni el Dockerfile, ni `README.md`, ni `entrada/`. |

### i) Build desde `ventas/src/`

**No termina bien.** Parado en `src/`, el contexto es `ventas/src/`, donde no hay `requirements.txt` ni una carpeta `src/` adentro. Falla en un `COPY` con `"/requirements.txt": not found` o `"/src": not found`. `-f ../Dockerfile` no mueve el contexto. (La clave impresa para calificar decía `"/app"` en este inciso; en la versión B la carpeta es `src`.)

### j) ¿Dónde queda lo que escribe el programa?

`/datos/limpio.csv` existe en **tu carpeta `entrada/`**, porque `/datos` era tu carpeta montada. `/ventas/limpio.csv` **no existe en ningún lado**: cayó en la capa de escritura, que se borró con el contenedor.

## Versión B · 2. ¿Qué cambió?

El mismo modelo de tres lugares que en la A. La diferencia es el orden: aquí el contenedor con montaje (k1) aparece primero y el que escribe en su capa (k2) después.

| # | Respuesta | Por qué |
|---|---|---|
| 1 | `verde` | k1 tiene tu carpeta montada en `/cfg`: lee tu disco al instante, sin build. |
| 2 | `rojo` | Contenedor nuevo sin montaje: lee la imagen, construida cuando tu carpeta decía `rojo`. |
| 3 | `verde` | El build de esta fila metió `verde` en la imagen; el `echo azul` dentro de k2 cayó en la capa de escritura de k2, no en tu carpeta. |
| 4 | caché | Tu carpeta no cambió desde el build de la fila 3 (sigue `verde`); lo de k2 no es parte del contexto. |
| 5 · run | `verde` | La imagen tiene `verde`. |
| 5 · exec | `azul` | k2 conserva su capa de escritura. |
| 6 | `gris` | k1 escribe en `/cfg`, que es tu carpeta. |
| 7 | `verde` | La imagen no se enteró: no hubo build desde la fila 3. |
| 8 | en ningún lado | `azul` sólo vivía en la capa de k2, y `docker rm` se la llevó. Tu carpeta dice `gris`; la imagen, `verde`. |
| 9 | `negro` | Montar un archivo: `otro.txt` tapa al `/cfg/color.txt` de la imagen. |
| 10 | `gris` | El build metió `gris` en la imagen. `bodega` no existía: vacío, Docker le copia el `/cfg` de la imagen. |
| 11 | `gris` | La imagen ya dice `blanco`, pero `bodega` ya no está vacío y tapa a la imagen. |

Si una casilla de la B no te cuadra, busca la fila de la A que hace lo mismo: la 1 de la B es la 7 de la A (montaje leyendo tu disco), la 3 es la 1 (escribir en la capa), la 4 es la 2 (caché), y las filas 9 a 11 son idénticas en las dos.

> [!TIP]
> Para el próximo examen, antes de contestar cada fila pregúntate dos cosas: ¿este contenedor tiene algo montado en esa ruta? ¿Hubo un `docker build` desde la última vez que cambió mi carpeta? Con esas dos respuestas sale casi todo el ejercicio 2.
