---
id: docker-y-podman
title: "Docker y Podman"
nav_title: "Docker y Podman"
summary: "La diferencia entre los dos es arquitectónica, y lo que compra correr sin daemon no es la velocidad."
status: ready
estimated_time: 14m
tags: [docker, podman, daemon, rootless, subuid, uidmap, conmon, benchmarking]
prerequisites: [vm-contra-contenedor]
---

# Docker y Podman

**Página 7 de 9 · sección 1 de 3**

Meta: entender que la diferencia entre los dos es arquitectónica, y qué compra exactamente no tener daemon.

::: figure {#cont-docker-vs-podman title="Las dos cadenas, y qué compra exactamente no tener daemon"}
![Las dos cadenas dibujadas una sobre otra. Arriba, Docker: el CLI que tecleas habla por el socket /var/run/docker.sock con dockerd, rotulado como root y siempre encendido y marcado como proceso privilegiado; de ahí sale containerd, de ahí un containerd-shim-runc-v2 que hace de supervisor, y al final runc, que crea y se va. El proceso del contenedor cuelga del shim. Abajo, Podman sin daemon y rootless: podman es tu propio proceso y hace fork-exec de conmon, que es el supervisor equivalente al shim, y conmon hace fork-exec de crun o de runc, que también crea y se va; el rótulo dice que no queda nada permanente y el proceso cuelga de conmon. Al costado, un recuadro con lo que rootless sí necesita: un rango propio en /etc/subuid y /etc/subgid y los binarios newuidmap y newgidmap, que en Debian y Ubuntu vienen en el paquete uidmap, que es Recommends y falta en instalaciones mínimas, y el error que sale sin eso, cannot find UID in /etc/subuid. Abajo del todo, el mito del 2x desarmado fijando todo menos el runtime: podman con crun 193 ms, docker con runc 330 ms y podman con runc 363 ms, con la conclusión de que con el runtime igualado Podman rootless sale unos 10 por ciento más lento, y que lo que compra la ausencia de daemon no es velocidad sino rootless, integración con systemd y ningún proceso privilegiado siempre encendido](../_assets/cont-docker-vs-podman.svg)
:::

## En corto

- Docker es un cliente que le habla por un socket a un **daemon que corre como `root` y nunca se apaga**; Podman hace `fork` y `exec` de sus propios procesos y no deja nada permanente encendido.
- Lo que compra la ausencia de daemon **no es velocidad**: con el runtime igualado, Podman rootless sale ~10 % más lento.
- Lo que sí compra es otra cosa, y es la que importa: rootless, integración con systemd y ningún proceso privilegiado siempre encendido.

## Los cuatro problemas del daemon

`daemon` y `socket` se definieron en [[anatomia-de-docker-run|la página 4]]; aquí se cobran.

**1. Un proceso privilegiado siempre encendido.** `dockerd` arranca con la máquina, corre como `root` y sigue ahí tengas o no contenedores. Es superficie de ataque permanente, aunque no lo uses en tres semanas.

**2. El socket es equivalente a `root`.** Quien puede escribir en `/var/run/docker.sock` le da órdenes a un proceso que es `root`, y una de esas órdenes es «móntame el disco entero adentro de un contenedor». Meter a alguien al grupo `docker` es darle `root` sin decírselo. Esa frase se desarma con las manos en la sesión 3.

**3. Todo cuelga de él, y de una forma rara.** Ya lo mediste en la página 4: matar el daemon **no** toca a los contenedores, pero reiniciarlo **sí los mata**, porque `live-restore` viene en `false`. Un `apt upgrade` que reinicie el servicio se lleva lo que estuviera corriendo.

**4. systemd no ve tus contenedores.** Para systemd existe `docker.service` y nada más; quien arrancó el contenedor fue el daemon, por dentro. No puedes pedirle a systemd que lo supervise, lo reinicie si muere o lo arranque al encender la máquina como haría con cualquier otra unidad — tienes que pedírselo a Docker, con su propia política de reinicio, que es un segundo supervisor encima del primero.

## El modelo fork-exec

Podman no tiene a quién pedirle nada: **lo hace él**.

```text
podman  →  conmon  →  crun (o runc)
```

Sin socket, sin daemon, sin servicio. `podman run` es un proceso tuyo, que hace `fork` y `exec` de `conmon`, que hace `fork` y `exec` del runtime. Cuando el comando `podman` termina, `conmon` se queda sosteniendo la salida y el código de salida del contenedor — exactamente el papel del shim en Docker. **La pieza que desaparece es el daemon, no el supervisor**, y esa distinción es la que decide el ejercicio de abajo.

De ahí sale algo que sorprende la primera vez: `podman ps` no le pregunta a nadie. Lee el estado del disco, en tu propio directorio, porque no hay un proceso central que sea dueño de la verdad.

## Rootless, con lo que de verdad necesita

«Rootless» quiere decir que el contenedor corre con **tu** usuario, sin `root` en ninguna parte de la cadena. No es una bandera: son dos cosas concretas que tienen que existir en la máquina, y por eso falla en instalaciones mínimas.

**Un rango propio en `/etc/subuid` y `/etc/subgid`.** Son los UID y GID que el sistema te presta para que los mapees adentro. Un renglón como `alumna:100000:65536` quiere decir que el UID 0 de adentro es el 100000 de afuera: dentro del contenedor eres `root`, y para el kernel del host eres un usuario que no existe y no puede nada. Sin ese renglón, el error es literal: `cannot find UID in /etc/subuid`.

**Los binarios `newuidmap` y `newgidmap`.** Son los que escriben ese mapeo, y son `setuid` porque escribirlo es justamente lo que un usuario normal no puede hacer solo. Vienen en el paquete **`uidmap`**, que en Debian y Ubuntu es **`Recommends`, no `Depends`**: una imagen base, un contenedor, un servidor instalado con `--no-install-recommends` o un WSL recién creado **no lo traen**, y Podman falla sin decir que le falta un paquete.

Ése es el porqué. El **procedimiento** —qué escribir, en qué orden, qué instalar— vive en la primera página de la sección 2, «Instalar Docker y Podman», y está escrito para copiarse.

Y un matiz que ya viste en la figura del espectro de la página 6: **rootless no añade ninguna frontera**. El kernel sigue siendo el mismo y la superficie de `syscall` es idéntica. Lo que cambia es con qué privilegio sale quien se escape.

## Tres filas, y el resto en la chuleta

::: table {#cont-tabla-docker-podman title="Las tres diferencias que cambian lo que haces"}

| | Docker | Podman |
|---|---|---|
| Quién arranca el contenedor | un daemon `root` siempre encendido, al otro lado de un socket | tu propio proceso, con `fork` y `exec` |
| Qué queda vivo cuando ya corre | `dockerd`, `containerd` y un shim por contenedor | un `conmon` por contenedor, y nada más |
| Quién eres adentro | `root` del host, salvo que lo configures | tú, mapeado a tu rango de `/etc/subuid` |

:::

La tabla larga de diez filas —red, volúmenes, `compose`, `pods`, dónde guarda cada uno sus imágenes— es referencia, no argumento, y por eso vive en la chuleta de la unidad.

Mientras tanto, el hecho práctico: los dos CLI son compatibles comando por comando, y `alias docker=podman` funciona para casi todo lo de este curso. «Casi» es la palabra: no hay servicio que arrancar, las imágenes viven en otro lado y, en rootless, los archivos que escriba el contenedor en tu carpeta salen siendo **tuyos** y no de `root`. Eso último no es un detalle, es media sesión 2.

## Lo que la ausencia de daemon no compra

Circula que Podman arranca al doble de velocidad. El número existe —213 ms contra 428 ms— pero la explicación es falsa, y la forma de verlo es fijar todo menos la pieza sospechosa:

| Qué se midió | Mediana |
|---|---:|
| `podman --runtime crun` | 193 ms |
| `docker` (usa `runc`) | 330 ms |
| `podman --runtime runc` | 363 ms |

Leído en orden: lo que compra la mitad del tiempo es **`crun`, que es el runtime por defecto de Podman y está escrito en C**, no la ausencia del daemon. Con el runtime igualado —`runc` de los dos lados— **Podman rootless sale ~10 % más lento que Docker**, porque el mapeo de usuarios y la red en espacio de usuario cuestan algo.

Así que la frase honesta es: no tener daemon no te hace más rápido. Te da rootless, te deja tratar un contenedor como una unidad de systemd y te quita un proceso `root` encendido las veinticuatro horas. Con eso basta para elegirlo; el 2× no hacía falta y encima era mentira.

![Dos paneles del experimento de escala, de 1 a 20 contenedores. El izquierdo, tiempo de arranque: Docker sube de 0.35 a 5.52 segundos y Podman de 0.19 a 2.74. El derecho, memoria del supervisor en MiB tal como la midió el script y sin corregir nada: la línea casi plana del RSS de dockerd, alrededor de 179 a 184 MiB, contra la suma del RSS de todos los conmon de Podman, que sube de 1.7 a 35.8 MiB y parece que va a cruzarla. Una nota al pie advierte que ésta es la medición cruda: el script mide sólo el RSS de dockerd y nunca cuenta los containerd-shim, uno por contenedor, y del lado de Podman suma el RSS de procesos que comparten páginas entre sí](../_assets/cont-bench-escala.svg)

::: problem {#cont-p7-el-cruce title="El cruce que no existe"}
La gráfica de arriba es la medición cruda de un script que mide la memoria del supervisor al pasar de 1 a 20 contenedores. Dibujada así, las dos líneas parecen ir a cruzarse: el RSS de `dockerd` se queda casi plano —179 MiB con un contenedor, 184 MiB con veinte— y la suma del RSS de los `conmon` de Podman sube de 1.7 a 35.8 MiB. De ahí salió la conclusión que circula: «a partir de unos 100 contenedores, Docker usa menos memoria».

El script tiene **dos errores**, y los dos datos que faltan son éstos:

- Del lado de Docker sólo se midió el RSS de `dockerd`. **Nunca se contó el `containerd-shim-runc-v2`, que es uno por contenedor** y pesa **11.0 MB** de RSS cada uno.
- Del lado de Podman se **sumó** el RSS de todos los `conmon`. Medidos aparte: `conmon` pesa **2.02 MB** de RSS, y **doce `conmon` juntos son 25 MB de RSS pero 4 MB de PSS**.

Contesta:

1. Corrige la curva de Docker. ¿Cuánta memoria de supervisor hay a 1 contenedor, y a 20?
2. ¿Por qué está mal sumar los RSS de los `conmon`, y qué número hay que usar en su lugar?
3. Con las dos correcciones, ¿dónde queda el cruce?
4. ¿Qué regla de benchmarking sale de los dos errores? Una frase.
:::

::: hint {of="cont-p7-el-cruce"}
Las dos correcciones son la misma pregunta hecha dos veces: **¿estoy contando lo mismo de los dos lados?** Para la 1, vuelve a la cadena de la página 4 y cuenta cuántos supervisores hay en Docker cuando corren veinte contenedores. Para la 2, pregúntate qué le pasa a una página de memoria que doce procesos comparten cuando sumas doce RSS.
:::

::: answer {of="cont-p7-el-cruce"}
**1. Docker es el `dockerd` medido más `11 × N`.** Con un contenedor, `179 + 11 × 1` = **190**; con veinte, `184 + 11 × 20` = **404**, o sea el daemon más veinte shims. La línea no era plana: era plana **porque el script sólo miraba el daemon**. Docker tiene un supervisor por contenedor igual que Podman, sólo que además tiene el daemon.

**2. Porque el RSS no es aditivo.** El RSS cuenta entera cada página residente del proceso, **incluidas las que comparte con otros**: doce `conmon` son doce copias del mismo binario y de las mismas librerías, así que sumar sus RSS cuenta esas páginas doce veces. La métrica que sí reparte cada página entre quienes la usan es el **PSS**, y está en `/proc/<pid>/smaps_rollup`. Medido: 25 MB de RSS contra **4 MB de PSS** — sumar RSS **infla a Podman unas seis veces**.

**3. No hay cruce.** A N = 1, Docker va 190 MB contra ~2 MB; a N = 20, 404 MB contra ~7 MB de PSS. **Podman gana en todo N**, y por dos órdenes de magnitud. El «cruce en 100 contenedores» era un artefacto de contar el supervisor por contenedor de un lado y no del otro, y de sumar una métrica que no se suma.

**4. La regla.** Un benchmark no compara herramientas: compara **lo que mediste** de cada una. Antes de publicar un número, dilo en voz alta —«medí el RSS del daemon contra la suma de los RSS de los supervisores»— y la mitad de los errores se caen solos. Y la segunda mitad: si vas a sumar una métrica, asegúrate de que sea aditiva.
:::

Sigue con [[capas-y-cache]], que explica por qué un `build` a veces tarda tres segundos y a veces tres minutos.

> [!NOTE]
> **Si sólo recuerdas una cosa:** Podman no es Docker más rápido; es Docker sin un proceso `root` siempre encendido, y eso se paga con ~10 % de arranque, no se cobra.
