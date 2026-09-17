---
id: lo-que-cuesta
title: "Lo que cuesta"
nav_title: "Lo que cuesta"
summary: "Números propios de arranque y de ejecución, con su pie de versiones, y cómo leerlos sin engañarte."
status: ready
estimated_time: 15m
tags: [benchmark, arranque, overhead, launch, running, coreutils, overlay, medicion]
prerequisites: [capas-y-cache]
---

# Lo que cuesta

**Página 9 de 9 · sección 1 de 3**

Meta: tener números propios de lo que cuesta un contenedor, y saber leerlos.

::: figure {#cont-bench-arranque title="Cuánto tarda en arrancar un contenedor, y qué mide de verdad el baseline"}
![Gráfica de barras horizontales en escala logarítmica con la mediana de diez repeticiones. Docker con ubuntu 24.04 tarda 427.6 ms y con alpine 429.8 ms; Podman con ubuntu 24.04 tarda 212.7 ms y con alpine 193.3 ms; la última barra, rotulada a pelo, dice fork más execve y mide 1.8 ms. Las dos barras de cada runtime salen prácticamente del mismo largo, y una anotación lo señala: cambiar de imagen no cambia el arranque, medio punto porcentual en Docker, porque arrancar no descomprime nada, la imagen ya quedó desplegada en disco desde el pull. Otra anotación aclara que el baseline no es el piso del cronómetro sino el fork más execve de /usr/bin/date, que su mediana es 1.8 ms y su media 3.1 ms por el ramp-up de frecuencia del CPU en las primeras repeticiones. Al pie, la máquina, el kernel y las versiones de los dos runtimes](../_assets/cont-bench-arranque.svg)
:::

## En corto

- Hay **dos** costos y se confunden todo el tiempo: el de **crear** un contenedor, que se paga una vez, y el de **correr** adentro, que se pagaría mientras corre.
- El primero es real y se mide en cientos de milisegundos. **El segundo, en la práctica, no existe.**
- Ningún número de esta página vale sin su pie de versiones, y las dos sorpresas que trae eran, las dos, estar midiendo otra cosa.

## Los pies, porque no hay una sola tanda

Lo cómodo sería decir que todos los números de esta unidad salen de la misma máquina y de la misma corrida. No es cierto, y decirlo aquí es el mejor ejemplo que esta página puede dar de lo que enseña: **el pie no es un trámite que se pega al final del número, es parte del número**. Son dos tandas, con **dos** excepciones dentro de la primera, y las cuatro se dicen.

**Tanda 1 — los cuatro experimentos de benchmark.** De aquí salen la gráfica de arranque, la de escala, la de ejecución y la del contenedor anidado, y con ellas los números que citan la página 5 y la 7. Éste es el pie que hay que arrastrar cada vez que alguien repita uno de ellos fuera de contexto:

> **Intel Core i7-7700HQ · Linux 6.12 · Docker 28.4.0 · Podman 4.6.2 (rootless, runtime `crun`) · imágenes `ubuntu:24.04` y `alpine` · GNU coreutils 8.32 en el host y 9.4 dentro de la imagen · mediana de 10 repeticiones en arranque y de 5 en ejecución, más un warm-up descartado.**

**La excepción, dentro de esa misma tanda: el experimento de escala es una sola corrida.** `exp2_scale.csv` tiene un punto por tamaño —1, 5, 10 y 20 contenedores— sin repeticiones y, por lo tanto, sin mediana: ese «mediana de 10» del pie **no lo cubre**. Y aun así basta para lo que ese experimento hace, con una condición. Lo que se argumenta con él no es un tiempo, es **qué se contó de cada lado**: el daemon contra los supervisores, RSS contra PSS. Ése es un error de orden de magnitud, y repetir la corrida diez veces habría dado diez versiones del mismo error, no lo habría corregido. Lo que no se puede hacer es citar «Docker tarda 5.52 s con veinte contenedores» como si fuera una mediana: es **una** corrida, y se dice así.

**La segunda excepción: el experimento de anidamiento son cuatro repeticiones, no diez.** `exp4_nested.csv` trae cuatro por serie, y ese «mediana de 10» del pie tampoco lo cubre. Cuatro es poco para afinar un número y suficiente para lo que ese experimento afirma, que es un **signo**: anidar cuesta algo, y ese algo no es cero. Cuánto, con esas cuatro repeticiones, sólo se puede decir con la mano abierta: el arranque de Docker dentro de Docker sale **+8 %** sobre Docker a secas, y el de Podman anidado **+45 %** sobre Podman. Escribir «un orden de magnitud» habría sido exagerar diez veces con cuatro mediciones, que es exactamente lo que esta página existe para no hacer. La regla que sale de aquí es la misma de arriba, y es la que conviene llevarse: **un pie que aplica a casi todos los números de una página no aplica a ninguno**. O lo cubre entero, o dice de qué se excluye.

**Tanda 2 — la comparación de runtimes OCI de la página 7.** Los 215 / 361 / 373 ms que desarman el mito del 2× **no son de la tanda 1**. Se midieron después, en otra máquina y con otras versiones, a propósito para esa pregunta:

> **Docker 29.6.0 · Podman 4.6.2 (rootless) · `crun` y `runc` del sistema · Linux 6.17.9 · imagen `ubuntu:24.04` · comando `echo ok` · mediana de 20 repeticiones más un warm-up descartado por brazo.**

Esos tres brazos se comparan **entre sí** —para eso se midieron juntos, en la misma tanda y fijando todo menos el runtime— y con ningún número de la tanda 1. Poner los 215 ms de Podman con `crun` al lado de los 212.7 ms de la gráfica de arranque y concluir cualquier cosa sería justo el error que esta página existe para evitar: son otro kernel, otro Docker y otra máquina.

Los scripts y los CSV de las dos tandas están publicados en `_assets/benchmarks/`, para que puedas rehacerlo.

## LAUNCH y RUNNING

**LAUNCH** es lo que cuesta **crear** el contenedor: armar los namespaces, el cgroup, el rootfs, el supervisor. Se paga **una vez**, al arrancar.

**RUNNING** es lo que costaría **estar adentro**: que tu programa tarde más en calcular, en leer o en escribir por el hecho de estar dentro de un contenedor. Se pagaría **todo el tiempo**.

Confundirlos es lo que produce la frase «los contenedores son 20 % más lentos». Casi siempre, quien la dice midió un LAUNCH y lo repartió sobre un trabajo corto. Y ya tienes el mecanismo para saber por qué RUNNING es casi cero: en la página 4 quedó que la `syscall` de tu proceso va **directo al kernel del host**, sin pasar por el daemon, por `containerd` ni por `runc`. No hay nadie en el camino a quien pagarle.

## Arranque: el costo que sí existe

Docker tarda **~428 ms** y Podman **~213 ms** en tener un contenedor corriendo. Dos cosas que leer en esa gráfica, y ninguna es la obvia.

**Cambiar de imagen no cambia el arranque.** Docker tarda 427.6 ms con `ubuntu:24.04` y 429.8 ms con `alpine`: medio punto porcentual, sobre imágenes que se llevan un orden de magnitud en tamaño. La explicación es la de la página 4: **arrancar no descomprime la imagen**. Las capas quedaron desplegadas en disco desde el `pull`, y lo único que falta es apilarlas. Elegir `alpine` sirve para muchas cosas —bajar rápido, ocupar menos disco, tener menos superficie— pero **no** para arrancar más rápido.

**El baseline de 1.8 ms no es el piso del cronómetro.** Es la trampa favorita de esta página. El script mide el intervalo entre un `date` y el siguiente, así que ese 1.8 ms **es el `fork` más el `execve` de `/usr/bin/date`**: es el costo de arrancar un programa — el programa equivocado, uno que no hace nada. No es «cero» y no es el error de medición; es una tercera cosa. Y es la **mediana**: la media de las mismas diez repeticiones es **3.1 ms**, porque las primeras corren con el CPU todavía en frecuencia baja. Publicar la media sin decirlo habría inflado el baseline al doble.

## Ejecución: los dos resultados, diciendo qué miden

::: figure {#cont-bench-overhead title="Ejecución dentro de un contenedor ya corriendo: los dos workloads, diciendo qué miden"}
![Gráfica del experimento de ejecución, con los dos workloads en paneles separados porque miden cosas distintas, sobre contenedores que ya estaban corriendo y con la mediana de cinco repeticiones. En el panel del hash, que genera 100 MiB y les saca sha256sum, a pelo tarda 1.035 s, docker exec 0.781 s y podman exec 0.850 s: el contenedor sale más rápido, y la anotación encima dice que la razón no es el contenedor sino que el host corre GNU coreutils 8.32 y la imagen ubuntu 24.04 corre 9.4, otra implementación de sha256sum y no otro kernel. En el panel del sort, que genera un millón de números, los revuelve y los ordena, a pelo tarda 1.416 s, docker exec 1.524 s y podman exec 1.504 s, o sea más 7.6 por ciento en Docker; esa barra va entera, con la nota de que parte del margen es el propio docker exec, que el experimento nunca midió aparte. Rotulada al centro, la conclusión: ejecutar dentro de un contenedor no cuesta. Al pie, la máquina, el kernel, los runtimes y la versión de coreutils de cada lado](../_assets/cont-bench-overhead.svg)
:::

**El `hash` sale a favor del contenedor, y no por ser contenedor.** Calcular el SHA-256 de 100 MiB tarda 1.035 s en el host y 0.781 s dentro de Docker. Es tentador inventar una teoría; la verdad es más aburrida y se comprueba en una línea: **el host corre GNU coreutils 8.32 y la imagen `ubuntu:24.04` corre 9.4**, y sobre el mismo archivo de 100 MiB el `sha256sum` de 9.4 tarda **0.19 s** contra **0.65 s** del de 8.32. El experimento comparó dos implementaciones distintas de `sha256sum`, no dos formas de ejecutar. Y para cerrar las dos explicaciones que suenan bien y son falsas: **no es SHA-NI** —este CPU no tiene esa instrucción— y **no es `/dev/urandom`**, que rinde igual de los dos lados.

**El `sort` sale al revés, +7.6 %.** Ordenar un millón de números tarda 1.416 s a pelo y 1.524 s con `docker exec`. Y aquí toca decir lo incómodo: **buena parte de ese margen es el propio `docker exec`**, que arranca un proceso nuevo dentro del contenedor y que este experimento **nunca aisló**. Se podría medir —un `docker exec <c> true` contra un `bash -c true`— pero no se midió, así que aquí no va ningún porcentaje «neto»: no hay dato que lo sostenga. Lo que sí sostiene el dato es la conclusión de arriba: sobre un trabajo de segundo y medio, el margen es de centésimas, y una parte de ellas ni siquiera es del contenedor.

> [!NOTE]
> Sí existe un costo real de VFS: resolver una ruta a través de un `overlay` de varias capas cuesta un poco más que en un sistema de archivos plano. Pero es de microsegundos por apertura, y ninguno de estos dos workloads abre archivos: abren uno y trabajan un segundo. El VFS no explica nada de lo que se ve arriba.

## Cuatro conclusiones

**1. Arrancar cuesta, y el número es de cientos de milisegundos.** Si tu diseño arranca miles de contenedores cortos, ése es tu costo y hay que sumarlo. Si arranca unos cuantos y los deja corriendo, es irrelevante.

**2. Ejecutar dentro no cuesta.** Es la tesis de la unidad y estos números la sostienen: el margen del `sort` es de centésimas sobre segundos, y el del `hash` salió al revés. Cuando alguien mida una diferencia grande, la explicación casi nunca es «el contenedor».

**3. Un número sin su pie no vale nada.** Las dos sorpresas de esta página —el `hash` a favor del contenedor y el baseline de 1.8 ms— eran lo mismo: estar midiendo otra cosa y no haberlo dicho.

**4. Antes de «qué contaste» va «con qué lo mediste».** Es el error que se comete primero, porque `free -m` es lo que ya sabes usar: pesar una carta en la báscula del baño en vez de en la postal. Lo que `free -m` reporta es la memoria de **toda la máquina**, y se mueve sola aunque tú no hagas nada —el kernel recicla *page cache*, libera *buffers*, compacta *slab*—: muestreada una vez por segundo durante minuto y medio, **sin tocar un solo contenedor**, se movió **358 MB**. En esa misma máquina y en ese mismo rato, un `ubuntu:24.04` con un `sleep` adentro pesa **2.3 MiB** en Docker y **98 kB** en Podman, leídos por el cgroup que le toca a ese contenedor: eso es lo que hacen `docker stats` y `podman stats`, leer `memory.current` del cgroup y de nadie más. La señal está dos o tres órdenes de magnitud por debajo del ruido, así que con `free -m` no la habrías visto nunca — y peor, habrías visto *algo*, porque el ruido no está en blanco. La prueba de que el cgroup sí es el instrumento correcto está en `exp2_scale.csv`: los KB por contenedor **no se mueven** al pasar de 1 a 20 contenedores —434, 438, 441, 437 en Docker; 102, 98, 97, 97 en Podman—, que es exactamente lo que se le pide a un instrumento, dar la misma respuesta a la misma pregunta. Y ojo con la tentación de comparar esos 437 KB con los 2.3 MiB de arriba: son otra máquina, otra versión de Docker y otra imagen. **La cifra absoluta se mueve; la estabilidad no.** De aquí sale la regla, que no es de contenedores y por eso vale la pena llevársela entera: **usa siempre el instrumento más específico que tengas**, y si sólo tienes uno grueso, di de qué tamaño es su ruido antes de publicar la señal.

> **El pie de los dos números medidos aquí:** Docker 29.6.0 · Podman 4.6.2 (rootless) · Linux 6.17.9 —las mismas versiones de la tanda 2—, `free -m -s 1 -c 90` contra `docker stats --no-stream` y `podman stats --no-stream` sobre un `ubuntu:24.04` corriendo `sleep`.

## Lo que esta página no midió, y por qué hay clase el martes

Escribir sí tiene un costo, y es **cualitativo** hasta que alguien lo mida bien. El `overlay` paga **copy-up**: la primera vez que tu proceso escribe sobre un archivo que vive en una capa inferior de sólo lectura, el kernel **copia el archivo entero** a la capa de escritura antes de dejarte tocarlo. Un archivo de 2 GB al que le cambias un byte se copia completo, una vez.

La cifra que circulaba —«el overlay escribe ~20 % más lento»— **no se publica aquí**, y vale la pena decir por qué: su propio CSV reporta a Podman **3.7× más rápido que bare metal** en la misma prueba. Nadie escribe casi cuatro veces más rápido dentro de un contenedor; lo que midió fue el **page cache**. Un resultado imposible en la misma tabla invalida la tabla entera, no sólo ese renglón.

El copy-up, en cambio, es mecanismo y no ruido, y es media razón de ser de la sesión del martes: si escribir dentro de la capa del contenedor se paga y además se pierde al borrarlo, los datos tienen que vivir en otro lado.

## Repítelo

El punto de publicar los scripts es que los corras. Están en `_assets/benchmarks/` con sus CSV, y tus números van a salir distintos — otra CPU, otro kernel, otras versiones. Eso es lo esperado: lo que se transfiere es el método, no la cifra.

Una advertencia, porque es la que hace que el experimento se sostenga: **`bench_runtime.sh` fija la imagen en `ubuntu:24.04` a propósito.** Hoy `ubuntu:latest` apunta a 26.04, cuyo `coreutils` está reimplementado en Rust, y con esa imagen **el resultado del `hash` invierte el signo**. Si cambias la etiqueta, no estás repitiendo el experimento: estás haciendo otro, y el pie tiene que decirlo.

::: problem {#cont-p9-quinientos title="Quinientos contenedores de dos segundos"}
Tienes que procesar 500 archivos. Dos diseños, con el mismo trabajo total de cómputo:

- **A**: un contenedor por archivo — 500 contenedores que corren 2 s cada uno.
- **B**: un solo contenedor que procesa los 500 archivos en 1000 s.

Con los números de esta página y Docker, contesta:

1. ¿Cuánto tiempo suma el **arranque** en cada diseño?
2. ¿Qué fracción del tiempo total es, en cada uno?
3. ¿Cambia algo usar Podman? ¿Y cambiar `ubuntu:24.04` por `alpine`?
4. De los dos costos, ¿cuál estás pagando en A, y qué rediseño lo baja? El trabajo de cómputo es el mismo en los dos, así que no vale hacerlo más rápido.
:::

::: hint {of="cont-p9-quinientos"}
Multiplica antes de opinar. Y para la 4: pregúntate cuántas veces se paga cada uno de los dos costos en cada diseño — uno se paga por contenedor y el otro por segundo.
:::

::: answer {of="cont-p9-quinientos"}
**1.** En **A**, `500 × 428 ms` = **214 s** de puro arranque. En **B**, un solo arranque: **0.43 s**.

**2.** En A, 214 s sobre 1214 s de total: **~18 % del reloj**, o **+21 %** sobre el trabajo útil. En B, **0.04 %** — ruido.

**3.** Con Podman, `500 × 213 ms` = **107 s**: se corta a la mitad, y sigue siendo un impuesto de ~10 %. Con `alpine` **no cambia nada**, medio punto porcentual, porque el arranque no descomprime la imagen. Cambiar de runtime ataca el costo; cambiar de imagen no lo toca.

**4.** Estás pagando **LAUNCH**, 500 veces. RUNNING no lo estás pagando: los 1000 s de cómputo cuestan lo mismo adentro que afuera. El rediseño no es acelerar el trabajo —es el mismo— sino **arrancar menos veces**: agrupar los archivos en, digamos, 20 contenedores de 50 cada uno baja el arranque de 214 s a 8.6 s, menos del 1 %. Y ojo con la salida fácil: arrancarlos en paralelo reparte esos 214 s entre los núcleos, pero no los borra, y encima le sumas contención. La pregunta correcta no es «¿cómo arranco más rápido?», es **«¿por qué estoy arrancando 500 veces?»**.
:::

Con esto cierra la sección. Sigue con [[contenedores-con-las-manos]], la sesión del martes, con teclado: instalar los dos runtimes y averiguar dónde vive cada byte que escribe un contenedor.

> [!NOTE]
> **Si sólo recuerdas una cosa:** crear un contenedor cuesta cientos de milisegundos y correr adentro no cuesta; cualquier número que diga otra cosa está midiendo algo que no dijo.
