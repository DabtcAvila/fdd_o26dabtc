---
id: donde-vive-cada-byte
title: "Dónde vive cada byte"
nav_title: "Dónde vive cada byte"
summary: "Cuatro lugares posibles para lo que escribe un contenedor, y cada uno muere con un comando distinto. Es la tabla que ordena toda la clase."
status: ready
estimated_time: 10m
tags: [overlay, volumen, bind-mount, capa-de-escritura, copy-up, persistencia]
prerequisites: [arreglar-un-dockerfile]
---

# Dónde vive cada byte

**Página 7 de 13 · sección 2 de 3**

Meta: dejar de preguntar «¿se guardó?» y empezar a preguntar «¿en cuál de los cuatro se guardó?». De ahí sale, sin adivinar, qué comando se lo lleva.

::: figure {#cont-overlay-volumen title="Los cuatro lugares donde puede caer un byte que escribe un contenedor"}
![Corte del sistema de archivos que ve un contenedor, colgando de la raíz. Abajo, apiladas y en sólo lectura, las capas de la imagen, rotuladas con las instrucciones que las produjeron: FROM python 3.12 slim, RUN pip install y COPY; las escribe docker build y mueren con docker rmi. Encima de ellas, dibujada por overlayfs, la capa de escritura del contenedor: la escribe el proceso de adentro y muere con docker rm, con una nota que explica el copy-up, es decir que la primera vez que el proceso escribe sobre un archivo que venía de una capa inferior, el archivo se copia entero hacia arriba. A un costado cuelgan dos rutas montadas aparte, que no pasan por el overlay: diagonal app, que sale de un bind mount apuntando a una carpeta del disco del host y que no muere nunca porque es tu disco, y diagonal var diagonal lib diagonal postgresql diagonal data, que sale de un named volume guardado en el área de Docker y que sobrevive a docker rm y muere con docker volume rm. Abajo, la tabla de cuatro filas con las mismas cuatro respuestas, una columna para quién escribe cada una, otra para qué comando la borra y otra que dice si sobrevive a docker rm: sí, NO, sí y sí](../_assets/cont-overlay-volumen.svg)
:::

## En corto

- Lo que un contenedor escribe cae en **uno de cuatro lugares**, y cada uno tiene un dueño distinto y un comando distinto que lo destruye.
- Sólo uno de los cuatro muere con `docker rm`: **la capa de escritura**. Los otros tres sobreviven, y por eso los datos no se guardan ahí.
- Esta tabla **predice el resultado** de todos los experimentos que siguen en la sección. Si te la sabes, no tienes que memorizar ninguno.

## La pila que ves desde adentro

En [[capas-y-cache]] quedó que la imagen es una pila de capas de **sólo lectura**. Entonces, ¿cómo escribe algo un contenedor, si su sistema de archivos no se puede escribir?

Con una capa más encima. El driver `overlay2` apila las capas de la imagen y le pone arriba una **capa de escritura** vacía, propia de ese contenedor; lo que ves desde adentro es la suma de todas, aplanada. Todo lo que el proceso cree crear o modificar aterriza en esa capa de arriba, y sólo ahí.

De ahí sale el **copy-up**, la deuda que dejó abierta [[lo-que-cuesta]]: la primera vez que tu proceso escribe sobre un archivo que venía de una capa inferior, el kernel **copia el archivo entero** hacia arriba antes de dejarte tocarlo. Un archivo de 2 GB al que le cambias un byte se copia completo, una vez. No es una teoría: es media razón de ser de esta clase, porque escribir dentro de la capa del contenedor se paga **y además se pierde**.

## Los otros dos no pasan por el overlay

Un **bind mount** toma un directorio de tu disco y lo hace aparecer en una ruta de adentro. No hay copia ni sincronización: es **el mismo directorio**, visto desde dos lados. Por eso lo escriben los dos, y por eso `docker rm` no puede tocarlo — borrar el contenedor no borra tu disco.

Un **named volume** es un directorio que administra el propio Docker, guardado en su área (`/var/lib/docker/volumes/`), con un nombre en vez de una ruta. Lo escribe el contenedor, sobrevive a `docker rm` y sólo muere cuando tú se lo pides con `docker volume rm`.

Que los dos **se salten el overlay** no es sólo una regla de persistencia: es también una regla de diseño. Si tu programa escribe mucho —una base de datos, un log que crece, un archivo grande que se reescribe—, **monta un volumen**, y no únicamente para que los datos sobrevivan. Al escribir sobre un montaje no hay capas apiladas de por medio ni hay **copy-up**: los bytes van al sistema de archivos del host, como los de cualquier otro proceso. Y cuánto se recupera con eso tiene número: en la misma máquina y sobre el mismo disco, Docker escribió **510 MB/s** en un volumen contra **380 MB/s** en la capa overlay — un **34 %** más rápido por no pasar por ahí, con mediana de **tres** repeticiones. La cifra que circula por internet, «el overlay escribe ~20 % más lento», no es ésta ni sale de ningún lado que puedas revisar; ésta sí, y su pie —máquina, kernel, versiones y por qué el otro brazo de ese mismo CSV se tiró— está en [[lo-que-cuesta|1/9]]. Lo que se transfiere es el signo y el mecanismo, no el 34 %: en tu disco y con tu carga va a salir otro número, así que si lo necesitas exacto, **mídelo en tu disco**.

::: table {#cont-tabla-bytes title="Las cuatro respuestas, con su dueño y su comando"}

| Dónde vive el byte | Quién lo escribe | Qué lo borra | ¿Sobrevive a `docker rm`? |
|---|---|---|---|
| Las capas de la imagen | `docker build` | `docker rmi` | sí |
| La capa de escritura | el proceso de adentro | `docker rm` | **no** |
| Bind mount | el host y el contenedor | tú, borrando el archivo | sí — **es tu disco** |
| Named volume | el contenedor | `docker volume rm` | sí |

:::

La fila que hay que leer despacio es la segunda, porque es la única que dice «no» y es donde cae **todo** lo que escribes sin pensarlo. La tercera y la cuarta existen justamente para sacar los bytes de ahí.

## Las tres, con las manos

**Haz:** escribe en la capa de escritura y mira qué pasa al borrar el contenedor.

```bash
cd ~/fdd/docker-lab
docker run -d --name capa ubuntu:24.04 sleep 300
docker exec capa bash -c 'echo hola > /datos.txt'
docker exec capa cat /datos.txt
docker rm -f capa && docker run -d --name capa ubuntu:24.04 sleep 300
docker exec capa cat /datos.txt
```

**Deberías ver:** `hola` la primera vez —el mismo contenedor, la misma capa— y `No such file or directory` la segunda. El `rm` se llevó la capa de escritura entera; el contenedor nuevo arranca de la imagen, que nunca supo de tu archivo. Bórralo con `docker rm -f capa` antes de seguir.

**Haz:** el mismo `echo`, pero sobre un bind mount.

```bash
docker run --rm -v "$(pwd)":/trabajo ubuntu:24.04 bash -c 'echo hola > /trabajo/datos.txt'
ls -l datos.txt
```

**Deberías ver:** el archivo **en tu carpeta**, aunque el contenedor ya no existe: el `--rm` lo borró en cuanto terminó. De quién quedó ese archivo es otra pregunta, y tiene cuatro respuestas: [[el-archivo-compartido]].

**Haz:** ahora un named volume, que no es una ruta tuya sino un nombre.

```bash
docker volume create datos-lab
docker run --rm -v datos-lab:/trabajo ubuntu:24.04 bash -c 'echo hola > /trabajo/datos.txt'
docker run --rm -v datos-lab:/trabajo ubuntu:24.04 cat /trabajo/datos.txt
docker volume ls
```

**Deberías ver:** `hola` en el **segundo** contenedor, que no tiene nada que ver con el primero: el volumen sobrevivió a los dos. Y `datos-lab` listado, ocupando disco hasta que alguien lo borre.

::: problem {#cont-s2p7-una-fila title="Una fila, y todo lo que se deduce de ella"}
Corriste esto, y el programa escribió un archivo en `/app/salida.txt`:

```bash
cd ~/fdd/docker-lab
docker run --rm -v "$(pwd)":/app mi-imagen:v1
```

1. ¿En **cuál de las cuatro filas** cae `salida.txt`? Una frase con el porqué.
2. ¿Qué comando lo borra? ¿Y qué **no** lo borra?
3. El `--rm` destruyó el contenedor al terminar. ¿Cambia eso tu respuesta?
4. Si hubieras corrido exactamente lo mismo **sin** el `-v`, ¿en qué fila habría caído, y qué habría pasado con el archivo?
:::

::: hint {of="cont-s2p7-una-fila"}
La pregunta que decide las cuatro es siempre la misma: **¿esa ruta de adentro está montada desde algún lado, o no?** Si lo está, el byte nunca pasó por el overlay. Si no lo está, cayó en la capa de escritura y ya sabes con qué muere.
:::

::: answer {of="cont-s2p7-una-fila"}
**1. En el bind mount**, tercera fila. `/app` está montado desde `~/fdd/docker-lab`, así que escribir ahí adentro es escribir en **tu disco**: no es una copia que después se sincroniza, es el mismo directorio visto desde los dos lados.

**2.** Lo borra **`rm salida.txt`** en tu terminal, como cualquier archivo tuyo. No lo borra `docker rm`, no lo borra `docker rmi mi-imagen:v1` y no lo borra `docker volume prune`, porque Docker no es el dueño de ese directorio.

**3. No cambia nada, y ése es el punto.** El `--rm` se llevó la capa de escritura del contenedor —la única fila que muere con `docker rm`—, y `salida.txt` no estaba ahí. Por eso el archivo sigue en tu carpeta después de que el contenedor dejó de existir.

**4. Habría caído en la capa de escritura**, segunda fila: sin `-v`, `/app` no está montado desde ningún lado, así que `/app/salida.txt` es una ruta más del overlay. El programa habría corrido igual, habría dicho que escribió el archivo, y el `--rm` lo habría destruido junto con el contenedor. **Sin error, sin aviso y sin archivo** — que es exactamente la falla que esta tabla existe para que no te sorprenda.
:::

Sigue con [[rutas-en-docker]], porque montar bien depende de una cosa más que todavía no viste: cómo se escribe el lado izquierdo del `-v`.

> [!NOTE]
> **Si sólo recuerdas una cosa:** de los cuatro lugares donde puede caer un byte, sólo la capa de escritura muere con `docker rm` — y es donde cae todo lo que escribes sin decir dónde.
