---
id: examen-docker-enunciado
title: "Examen de Docker: enunciado"
nav_title: "Docker · enunciado"
summary: "El examen parcial de contenedores tal como se repartió, versiones A y B, sin respuestas: llevar un repo a una imagen y seguir qué cambia entre tu carpeta, la imagen y cada contenedor."
status: ready
estimated_time: 25m
tags: [examen, docker, dockerfile, volumenes, cache, anexo]
---

# Examen de Docker: enunciado

**Anexo · Exámenes** · sin respuestas. La solución está en [[examen-docker-solucion]].

**[Descargar el PDF](_assets/examen-docker.pdf)**: las cuatro hojas tal como se imprimieron (A y B, dos caras cada una).

Dura **25 minutos** y vale **10 puntos**. Sin apuntes, formularios ni dispositivos electrónicos: sólo las hojas, pluma o lápiz y goma. Dos ejercicios, uno por cara.

## Versión A

### 1. Del repo a la imagen (4 puntos)

```text
clima/            ← estás aquí
├── Dockerfile
├── README.md
├── requirements.txt
├── app/
│   ├── main.py
│   └── utils.py
└── data/
    └── clima.csv
```

`clima/` es un repo de Python. El programa es `app/main.py` (usa `app/utils.py`). En tu máquina los datos están en `data/`; dentro del contenedor el programa los lee de `/clima/data` y escribe ahí un resumen.

Queremos la imagen `clima:1`, así:

- dentro de la imagen se trabaja en `/clima`; ahí van `/clima/requirements.txt` y `/clima/app/`;
- al arrancar, el contenedor corre `python app/main.py` parado en `/clima`;
- `data/` **no** entra a la imagen: al correr, se monta en `/clima/data`.

Completa el Dockerfile. En cada `COPY`, el origen es una ruta **relativa** a `clima/` (el contexto del build) y el destino es una ruta **absoluta** dentro de la imagen. **(1 punto, 0.25 c/u)**

```text
FROM     python:3.12-slim
WORKDIR  (a)____________________
COPY     requirements.txt  (b)____________________
RUN      pip install -r requirements.txt
COPY     (c)____________________  /clima/app
CMD      (d)______________________________
```

Escribe cada comando completo. Tu terminal está en `clima/`.

**e)** Construye la imagen `clima:1`. **(0.5)**

**f)** El programa lee los datos de `/clima/data`. Corre `clima:1` en un contenedor que se borre al terminar y que monte tu carpeta `data/` en `/clima/data`. **(0.5)**

**g)** Abre una terminal `bash` en un contenedor **nuevo** de `clima:1`, que se borre al salir, para revisar `/clima` (escribe sólo el comando que abre la terminal). **(0.5)**

**h)** Con el Dockerfile ya completo, ¿qué archivos del repo quedan **dentro de la imagen**? Márcalos. **(0.5)**

`Dockerfile` · `README.md` · `requirements.txt` · `app/main.py` · `app/utils.py` · `data/clima.csv`

**i)** Alguien entra a la carpeta `clima/app/` (`cd app`) y desde ahí corre `docker build -t clima:1 -f ../Dockerfile .` ¿El build termina bien? ¿Por qué? **(0.5)**

**j)** En f), el programa escribe `/clima/data/resumen.csv` y luego el contenedor se borra. ¿Dónde existe ahora ese archivo: en tu carpeta `data/`, en la imagen o en ningún lado? ¿Y si lo hubiera escrito en `/clima/resumen.csv`? (mismas opciones) **(0.5)**

### 2. ¿Qué cambió? (6 puntos, 0.5 c/u)

En `lab/` hay sólo este Dockerfile y `nota.txt`, cuyo texto es la palabra **uno**:

```dockerfile
FROM alpine:3.20
WORKDIR /w
COPY nota.txt .
CMD ["cat", "nota.txt"]
```

No existen imágenes, contenedores, volúmenes ni caché previos. Los comandos se corren **en orden**, seguidos y sin pausas (ningún `sleep 600` alcanza a terminar), todos desde `lab/`: cada fila parte de lo que dejó la anterior. Contesta con **una palabra o frase corta**; si crees que un comando falla, escribe **error**.

| # | Comandos (en orden) | Pregunta |
|---|---|---|
| 1 | `docker build -t nota:1 .` ; `docker run -d --name c1 nota:1 sleep 600` ; `docker exec c1 sh -c 'echo dos > nota.txt'` | ¿Qué contiene `nota.txt` en tu carpeta `lab/`? |
| 2 | `docker build -t nota:1 .` | El paso `COPY`, ¿se vuelve a ejecutar o sale de la caché? ¿Por qué? (pocas palabras) |
| 3 | `echo tres > nota.txt` ; `docker run --rm nota:1` ; `docker exec c1 cat nota.txt` | ¿Qué imprime el run? ¿Y el exec? |
| 4 | `docker build -t nota:1 .` ; `docker run --rm nota:1` | ¿Qué imprime el run? |
| 5 | `docker run -d --name c2 -v "$(pwd)":/w nota:1 sleep 600` ; `docker exec c2 sh -c 'echo cuatro > nota.txt'` | ¿Qué contiene `nota.txt` en tu carpeta `lab/`? |
| 6 | `docker run --rm nota:1` | ¿Qué imprime? |
| 7 | `echo cinco > nota.txt` ; `docker exec c2 cat nota.txt` | ¿Qué imprime el exec? |
| 8 | `docker rm -f c1 c2` | El texto **dos**, ¿dónde existe ahora? (tu carpeta / la imagen / en ningún lado) |
| 9 | `echo seis > extra.txt` ; `docker run --rm -v "$(pwd)/extra.txt":/w/nota.txt nota:1` | ¿Qué imprime? |
| 10 | `docker build -t nota:1 .` ; `docker run --rm -v almacen:/w nota:1` | ¿Qué imprime el run? |
| 11 | `echo siete > nota.txt` ; `docker build -t nota:1 .` ; `docker run --rm -v almacen:/w nota:1` | ¿Qué imprime el run? |

En el papel, cada fila tiene sus comandos uno por renglón; aquí van separados por `;`. La fila 3 tiene dos casillas: 12 casillas en total.

## Versión B

### 1. Del repo a la imagen (4 puntos)

```text
ventas/           ← estás aquí
├── Dockerfile
├── README.md
├── requirements.txt
├── src/
│   ├── cargar.py
│   └── formatos.py
└── entrada/
    └── enero.csv
```

`ventas/` es un repo de Python. El programa es `src/cargar.py` (usa `src/formatos.py`). En tu máquina los CSV están en `entrada/`; dentro del contenedor el programa los lee de `/datos` y escribe ahí uno limpio.

Queremos la imagen `ventas:1`, así:

- dentro de la imagen se trabaja en `/ventas`; ahí van `/ventas/requirements.txt` y `/ventas/src/`;
- al arrancar, el contenedor corre `python src/cargar.py` parado en `/ventas`;
- `entrada/` **no** entra a la imagen: al correr, se monta en `/datos`.

Completa el Dockerfile, con las mismas reglas de rutas que en la versión A. **(1 punto, 0.25 c/u)**

```text
FROM     python:3.12-slim
WORKDIR  (a)____________________
COPY     requirements.txt  (b)____________________
RUN      pip install -r requirements.txt
COPY     (c)____________________  /ventas/src
CMD      (d)______________________________
```

Escribe cada comando completo. Tu terminal está en `ventas/`.

**e)** Construye la imagen `ventas:1`. **(0.5)**

**f)** Abre una terminal `bash` en un contenedor **nuevo** de `ventas:1`, que se borre al salir, para revisar `/ventas` (escribe sólo el comando que abre la terminal). **(0.5)**

**g)** El programa lee los datos de `/datos`. Corre `ventas:1` en un contenedor que se borre al terminar y que monte tu carpeta `entrada/` en `/datos`. **(0.5)**

**h)** Con el Dockerfile ya completo, ¿qué archivos del repo quedan **dentro de la imagen**? Márcalos. **(0.5)**

`Dockerfile` · `README.md` · `requirements.txt` · `src/cargar.py` · `src/formatos.py` · `entrada/enero.csv`

**i)** Alguien entra a la carpeta `ventas/src/` (`cd src`) y desde ahí corre `docker build -t ventas:1 -f ../Dockerfile .` ¿El build termina bien? ¿Por qué? **(0.5)**

**j)** En g), el programa escribe `/datos/limpio.csv` y luego el contenedor se borra. ¿Dónde existe ahora ese archivo: en tu carpeta `entrada/`, en la imagen o en ningún lado? ¿Y si lo hubiera escrito en `/ventas/limpio.csv`? (mismas opciones) **(0.5)**

### 2. ¿Qué cambió? (6 puntos, 0.5 c/u)

En `cfg/` hay sólo este Dockerfile y `color.txt`, cuyo texto es la palabra **rojo**:

```dockerfile
FROM alpine:3.20
WORKDIR /cfg
COPY color.txt .
CMD ["cat", "color.txt"]
```

Las mismas reglas que en la versión A: nada previo, todo en orden y desde `cfg/`, ningún `sleep 600` termina; una palabra o frase corta, o **error**.

| # | Comandos (en orden) | Pregunta |
|---|---|---|
| 1 | `docker build -t color:1 .` ; `docker run -d --name k1 -v "$(pwd)":/cfg color:1 sleep 600` ; `echo verde > color.txt` ; `docker exec k1 cat color.txt` | ¿Qué imprime el exec? |
| 2 | `docker run --rm color:1` | ¿Qué imprime? |
| 3 | `docker build -t color:1 .` ; `docker run -d --name k2 color:1 sleep 600` ; `docker exec k2 sh -c 'echo azul > color.txt'` | ¿Qué contiene `color.txt` en tu carpeta `cfg/`? |
| 4 | `docker build -t color:1 .` | El paso `COPY`, ¿se vuelve a ejecutar o sale de la caché? ¿Por qué? (pocas palabras) |
| 5 | `docker run --rm color:1` ; `docker exec k2 cat color.txt` | ¿Qué imprime el run? ¿Y el exec? |
| 6 | `docker exec k1 sh -c 'echo gris > color.txt'` | ¿Qué contiene `color.txt` en tu carpeta `cfg/`? |
| 7 | `docker run --rm color:1` | ¿Qué imprime? |
| 8 | `docker rm -f k1 k2` | El texto **azul**, ¿dónde existe ahora? (tu carpeta / la imagen / en ningún lado) |
| 9 | `echo negro > otro.txt` ; `docker run --rm -v "$(pwd)/otro.txt":/cfg/color.txt color:1` | ¿Qué imprime? |
| 10 | `docker build -t color:1 .` ; `docker run --rm -v bodega:/cfg color:1` | ¿Qué imprime el run? |
| 11 | `echo blanco > color.txt` ; `docker build -t color:1 .` ; `docker run --rm -v bodega:/cfg color:1` | ¿Qué imprime el run? |

La fila 5 tiene dos casillas: 12 casillas en total.

Cuando termines, califícate con [[examen-docker-solucion]].
