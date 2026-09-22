---
id: lab-sin-volumen
title: "Lab A: sin volumen"
nav_title: "Lab A: sin volumen"
summary: "Seis experimentos, ocho casos, sin volúmenes: editas en tu carpeta, en el Dockerfile o adentro del contenedor, y en cada caso predices qué cambió."
status: ready
estimated_time: 25m
tags: [imagen, contenedor, build, capa-de-escritura, docker-commit, docker-diff]
prerequisites: [donde-vive-cada-byte]
---

# Lab A: sin volumen

**Página 5 de 16 · sección 2 de 3**

Meta: predecir, antes de correrlo, qué ve un contenedor según dónde editaste: en tu carpeta, en el Dockerfile o adentro.

::: figure {#cont-lab-sin-volumen title="Qué cambia qué, sin volúmenes"}
![Matriz para predecir, sin respuestas: ocho filas y tres columnas de preguntas. Las filas son lo que haces: editar app.py en el host sin build; editarlo en el host y hacer build; editar el Dockerfile sin build; editar adentro con docker exec; editar adentro y luego docker stop y docker start; editar adentro y luego docker rm; editar adentro y luego docker build; editar adentro y luego docker commit. Las columnas preguntan si lo ve el contenedor que ya corría, si lo ve un contenedor nuevo de la imagen y si cambió la imagen. Cada celda lleva un signo de interrogación: predice cada una antes de correrla; las respuestas están en la tabla del final](../_assets/cont-lab-sin-volumen.svg)
:::

## En corto

- Seis experimentos, ocho casos, una regla: la imagen sólo cambia con `docker build`, y el build lee **tu carpeta**, nunca un contenedor.
- Un contenedor **nunca se actualiza solo**: sigue con la imagen con la que nació. Para ver lo nuevo, lo recreas.
- Lo que editas adentro vive en la capa de escritura de **ese** contenedor y muere con su `docker rm`.

## El montaje

**Haz:**

```bash
mkdir -p ~/fdd/docker-lab/lab-a && cd ~/fdd/docker-lab/lab-a
cp ~/fdd/fdd_o26/codigo/08_contenedores/volumenes/app.py .
printf '%s\n' 'FROM python:3.12-slim' 'WORKDIR /app' 'COPY . .' \
  'CMD ["python", "app.py"]' > Dockerfile
docker build -t app:1 .
docker run --rm app:1 | head -3
```

**Deberías ver:**
- la cabecera `Lab 1: Bind Mounts` entre dos filas de `=`;
- es la línea que vas a cambiar; `| head -3` muestra sólo eso.

### 1. Editas tu carpeta, sin build: `app.py` y el Dockerfile

**Predice:** si cambias la cabecera a `HOST` y el `CMD` a `python --version`, ¿qué imprime `app:1`?

**Haz:**

```bash
sed -i 's/Bind Mounts/HOST/' app.py
sed -i 's/"app.py"/"--version"/' Dockerfile
docker run --rm app:1 | head -3
docker inspect -f '{{.Config.Cmd}}' app:1
sed -i 's/"--version"/"app.py"/' Dockerfile
```

**Deberías ver:**
- `Lab 1: Bind Mounts` otra vez;
- `inspect` (que le pregunta a la imagen su `CMD`) dice `[python app.py]`;
- la última línea deja el Dockerfile como estaba; `app.py` se queda con `HOST`.

**Por qué:** `COPY . .` copió `app.py` al momento del build, y la imagen ya horneada no vuelve a leer el Dockerfile. Tus ediciones sólo existen en tu disco.

> [!TIP]
> En macOS, `sed -i ''` — sólo en tu host. Lo de `docker exec ... sed` corre en Linux: déjalo igual.

### 2. Haces build, con un contenedor que ya corría

**Predice:** tras el build, ¿cuál de los dos dice `HOST`? ¿Y de qué imagen dice `docker ps` que es `viejo`?

**Haz:**

```bash
docker run -d --name viejo app:1 sleep infinity
docker build -t app:1 .
docker run --rm app:1 | head -3
docker exec viejo python app.py | head -3
docker ps --filter name=viejo --format '{{.Image}}'
docker images app
```

**Deberías ver:**
- el contenedor nuevo dice `Lab 1: HOST`; `viejo` sigue con `Lab 1: Bind Mounts`;
- `ps` no dice `app:1`: da un ID pelón de 12 caracteres, distinto del `IMAGE ID` que muestra `docker images app`.

**Por qué:** el tag `app:1` se movió a la imagen nueva; `viejo` se quedó con la anterior, ya sin nombre: una huérfana ([[limpieza-de-docker|2/8]]). Para ver lo nuevo, se recrea.

### 3. Editas adentro, con `docker exec`

**Predice:** ¿quién ve `DENTRO`: `viejo`, un contenedor nuevo, o los dos? ¿Qué muestra `docker logs viejo`?

**Haz:**

```bash
docker exec viejo sed -i 's/Bind Mounts/DENTRO/' app.py
docker exec viejo python app.py | head -3
docker diff viejo | grep ' /app'
docker run --rm app:1 | head -3
docker logs viejo
```

**Deberías ver:**
- `viejo` dice `Lab 1: DENTRO`; el contenedor nuevo, `Lab 1: HOST`;
- `docker diff`: `C /app`, `C /app/app.py`, `A /app/output.txt` (`C` cambiado, `A` añadido);
- `output.txt` lo escribe `app.py` al correr; sin el `grep` salen además los `__pycache__`;
- `docker logs viejo`: **nada**. Sólo captura la salida del PID 1 (`sleep`), no lo que corre `exec`.

**Por qué:** `docker diff` es la capa de escritura de `viejo`, listada. La imagen no se enteró.

### 4. Editas adentro y haces build

**Predice:** ¿`DENTRO` entra a `app:1`?

**Haz:**

```bash
docker build -t app:1 .
docker run --rm app:1 | head -3
docker images app
```

**Deberías ver:**
- el paso `COPY . .` marcado `CACHED`;
- el mismo `IMAGE ID` del experimento 2;
- `Lab 1: HOST`.

**Por qué:** el build lee tu carpeta, y ahí nada cambió. El contenedor no es parte del contexto.

### 5. `docker commit`: la vía directa de adentro a una imagen

**Predice:** ¿`app:parche` corre con `DENTRO`?

**Haz:**

```bash
docker commit viejo app:parche
docker run --rm app:parche python app.py | head -3
docker history app:parche | head -2
docker inspect -f '{{.Config.Cmd}}' app:parche
```

**Deberías ver:**
- `Lab 1: DENTRO`;
- en `history`, una capa de unos 20 kB cuyo `CREATED BY` dice `sleep infinity`;
- el `CMD` quedó en `[sleep infinity]`.

**Por qué funciona y no se usa:**
- la capa dice el comando del contenedor, no tu `sed`, y se llevó su `CMD`: `docker run --rm app:parche` a secas se cuelga y Ctrl-C no lo para;
- el Dockerfile no se entera: el próximo build la ignora;
- nadie la reproduce: ni siquiera trae el `HOST` del experimento 2, porque `viejo` nació de la imagen vieja.

### 6. `docker stop` + `docker start`, y luego `docker rm`

**Predice:** ¿`DENTRO` sobrevive al reinicio? ¿Y al `rm`?

**Haz:**

```bash
docker stop viejo && docker start viejo
docker exec viejo python app.py | head -3
docker rm -f viejo
docker exec viejo python app.py
docker run --rm app:1 | head -3
```

**Deberías ver:**
- tras el reinicio, `Lab 1: DENTRO`. El `stop` tarda unos 10 s: `sleep` ignora la señal ([[ciclo-de-vida-de-un-contenedor|2/2]]);
- tras el `rm`, `Error response from daemon: No such container: viejo`;
- el nuevo dice `Lab 1: HOST`: la imagen nunca tuvo `DENTRO`.

**Por qué:** detener no borra: es la misma capa de escritura. `rm` sí, y con ella se van el cambio y los `docker logs`.

Deja la carpeta y las imágenes: [[limpieza-de-docker]] las reusa. La versión larga, con volúmenes: [[los-ocho-casos|2/15]].

> [!TIP]
> **Con Podman:** el build dice `--> Using cache` en vez de `CACHED`; el `history` del commit muestra `/bin/sh` y unos 45 kB; `rm -f` espera 10 s; el error es `no container with name or ID "viejo"`.

## ¿Qué cambió?

| Lo que haces | ¿Lo ve el que ya corría? | ¿Lo ve uno nuevo? | ¿Cambió la imagen? |
|---|---|---|---|
| Editas en el host, sin build | no | no | no |
| Editas en el host + build | no | sí | sí (imagen nueva) |
| Editas el Dockerfile, sin build | no | no | no |
| Editas adentro con `exec` | sí | no | no |
| Adentro + `stop`/`start` | sí (sigue) | no | no |
| Adentro + `docker rm` | ya no existe | no | no |
| Adentro + build | sí (es su capa) | no | no: el build lee tu carpeta |
| Adentro + `docker commit` | sí (es su capa) | sí, de la imagen nueva | sí: una que el Dockerfile no conoce |

::: problem {#cont-lab-a-build title="«Hice build y no funciona»"}
Tu compañero corrigió un bug con `docker exec ... vim app.py` y ahí funcionó. Hizo `docker build -t app:1 .`, corrió un contenedor nuevo y el bug volvió. Jura que el build está roto. ¿Qué pasó y qué debe hacer?
:::

::: hint {of="cont-lab-a-build"}
¿De dónde lee el build? Revisa el experimento 4.
:::

::: answer {of="cont-lab-a-build"}
- El build no está roto: leyó su carpeta, donde el bug sigue. La corrección vive en la capa de escritura de aquel contenedor.
- Rescate: `docker cp viejo:/app/app.py .` (con el nombre de su contenedor) trae el archivo corregido a su carpeta.
- Luego `docker build` y recrear el contenedor. Lo de adentro sólo sirvió para probar.
:::

Sigue con [[lab-con-volumen]], donde tu carpeta entra al contenedor sin pasar por la imagen.

> [!NOTE]
> **Si sólo recuerdas una cosa:** la imagen sólo la cambia un build, el build sólo lee tu carpeta, y lo que editas adentro muere con ese contenedor.
