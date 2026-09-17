---
id: ciclo-de-vida-de-un-contenedor
title: "El ciclo de vida de un contenedor"
nav_title: "El ciclo de vida"
summary: "Una sola idea explica todo el ciclo: un contenedor vive exactamente lo que vive su proceso principal."
status: ready
estimated_time: 12m
tags: [ciclo-de-vida, run, start, exec, logs, rm, pid, exited]
prerequisites: [a-docker-hub]
---

# El ciclo de vida de un contenedor

**Página 4 de 13 · sección 2 de 3**

Meta: que todo el ciclo se deduzca de una sola regla, en vez de memorizarse como doce comandos sueltos. Los doce están en [[chuleta-contenedores|la chuleta]]; esta página es la regla que los ordena.

::: figure {#cont-ciclo-de-vida title="Tres estados, y qué comando alcanza a cuál"}
![Máquina de estados de tres casillas rotuladas created, running y exited, con cada transición etiquetada por lo que la provoca: docker run, la salida del proceso PID 1 —que es la única razón por la que un contenedor se detiene—, docker start, docker stop y docker rm, que saca la casilla del dibujo junto con su capa de escritura. A la derecha, qué alcanza cada comando: docker ps sólo ve running, docker ps -a ve las tres, docker logs muestra lo que escribió ese proceso, y la flecha de docker exec -it entra a running y aparece tachada contra exited. Un caso al pie, el exited con código 127 del comando que no existe](../_assets/cont-ciclo-de-vida.svg)
:::

## En corto

- **Un contenedor vive exactamente lo que vive su proceso principal.** Todo lo demás de esta página sale de ahí.
- No hay «apagarse»: hay un `PID` 1 que terminó, y un cadáver que sigue en la lista hasta que lo borres.
- `ps` sólo ve a los vivos; `ps -a` ve a los muertos, y ahí está la respuesta de por qué falló.

## La pregunta número uno del principiante

Dos comandos, dos comportamientos que parecen magias distintas:

```bash
docker run ubuntu:24.04          # termina de inmediato
docker run -d ubuntu:24.04 sleep 300   # se queda corriendo cinco minutos
```

La explicación falsa —la que se saca del modelo mental de «máquina pequeña»— es que el primero está roto o que la imagen de Ubuntu «no trae nada». La verdadera es una sola frase:

**Un contenedor vive exactamente lo que vive su proceso principal.**

La imagen de Ubuntu trae como comando por defecto un `bash`. Sin terminal interactiva, ese `bash` no tiene de dónde leer, así que **termina en el acto** — y con él se acaba el contenedor, porque él *era* el contenedor. El segundo caso corre `sleep 300`, que tarda cinco minutos en terminar, así que el contenedor dura cinco minutos. Ni uno está roto ni el otro es especial: los dos duran lo que dura su `PID` 1.

Es la misma idea de [[anatomia-de-docker-run|la anatomía de `docker run`]] vista desde arriba: el contenedor no es una caja que contiene un proceso, **es** el proceso, con su vista recortada y su despensa medida.

## Los tres estados

**Haz:** arranca uno de verdad y míralo desde los dos lados.

```bash
docker run -d --name lab ubuntu:24.04 sleep 300
docker ps
docker ps -a
```

**Deberías ver:** el mismo contenedor en las dos listas, con `STATUS` en `Up ... seconds`. `docker ps` lista **sólo los vivos**; `docker ps -a` lista además los que ya terminaron. Que sean dos comandos y no uno es la fuente de la mitad de la confusión del primer día: «desapareció mi contenedor» casi siempre quiere decir «terminó, y estoy mirando la lista que no lo incluye».

**Haz:** ahora entra, sal, y mira qué pasó.

```bash
docker exec -it lab bash
# ya adentro:
ps aux
exit
docker ps -a
```

**Deberías ver:** adentro, dos o tres procesos —tu `bash` y el `sleep`, que es el `PID` 1—; y al salir, el contenedor **sigue corriendo**. Tu `bash` no era el proceso principal: era un invitado que `exec` metió al lado. Saliste tú, no él.

Compara eso con lo contrario: si hubieras arrancado con `docker run -it ubuntu:24.04 bash`, ese `bash` **sí** sería el `PID` 1, y escribir `exit` apagaría el contenedor. Mismo `exit`, resultado opuesto, y la diferencia es sólo quién era el proceso principal.

**Haz:** detén, revive y borra.

```bash
docker stop lab && docker ps -a
docker start lab && docker ps
docker rm -f lab && docker ps -a
```

**Deberías ver:** primero `Exited (137)`, después otra vez `Up`, y al final la lista sin `lab`. Un contenedor detenido **no es un contenedor que se fue**: es una capa de escritura y una entrada en la lista que siguen ocupando disco hasta que corres `rm`. Eso es lo que `docker rm` borra — y lo que se lleva con él es todo lo que ese proceso haya escrito adentro, que es el tema de las siguientes páginas.

## Se murió con error, ¿cómo averiguo por qué?

Es la segunda pregunta del principiante, y tiene una respuesta mecánica.

**Haz:** provoca la falla a propósito.

```bash
docker run --name roto ubuntu:24.04 comando-que-no-existe
docker ps -a --filter name=roto
docker logs roto
```

**Deberías ver:** el `run` devolviéndote el prompt en seguida, una fila con `Exited (127)` y, en `logs`, la línea que explica todo: `exec: "comando-que-no-existe": executable file not found in $PATH`.

Los dos comandos contestan cosas distintas y hay que correr los dos. `ps -a` te da el **código de salida**: es el número con el que terminó el proceso principal, tal cual, sin interpretación de Docker. Y `127` es una convención vieja de la shell: *no encontré el comando*. `logs` te da **lo que ese proceso escribió** por salida estándar y error estándar — que es exactamente lo que el shim estuvo sosteniendo mientras corría.

| Código | Qué suele querer decir |
|---|---|
| `0` | terminó bien; el contenedor hizo su trabajo y se acabó |
| `1` | el programa falló por su cuenta: lee `logs` |
| `126` | el archivo existe pero no es ejecutable — casi siempre falta `chmod +x` |
| `127` | no existe el comando; una errata, o no está instalado en esa imagen |
| `137` | lo mataron con `SIGKILL`: tu `docker stop` que se pasó del tiempo, o el límite de memoria |

::: problem {#cont-s2p4-predice-ps title="Predice `ps -a` en cada paso"}
**Escribe tus cinco predicciones antes de teclear nada.** Para cada paso, di qué imprime `docker ps -a` justo después: ¿aparece `demo`?, y si aparece, ¿con qué `STATUS`?

```bash
docker run -d --name demo ubuntu:24.04 sleep 20   # 1
# espera 25 segundos                              # 2
docker start demo                                 # 3
docker stop demo                                  # 4
docker rm demo                                    # 5
```

Y la pregunta que cierra la página: después del paso 2, corres `docker exec -it demo bash` y **falla**. ¿Con qué mensaje, y por qué falla? No contestes «porque está detenido» — explica qué es lo que `exec` necesita y no encuentra.

Cuando tengas las cinco escritas, córrelo y cuenta cuántas acertaste.
:::

::: hint {of="cont-s2p4-predice-ps"}
Para cada paso, hazte una sola pregunta: **¿está vivo el proceso principal?** Nada más decide el `STATUS`; el resto son consecuencias.

Y para la última, mira la flecha tachada de la figura, y acuérdate de que el `bash` de un `exec` no es el proceso principal, sino uno que llega **al lado** de otro.
:::

::: answer {of="cont-s2p4-predice-ps"}
**1.** Aparece, `Up X seconds`. El `sleep` está vivo.
**2.** Aparece, `Exited (0) X seconds ago`. El `sleep` terminó **bien**, así que el contenedor terminó bien. Sigue en la lista: terminar no es desaparecer.
**3.** Aparece, `Up X seconds`. `docker start` vuelve a lanzar el **mismo** comando de siempre, así que arranca otro `sleep 20` — y en veinte segundos va a volver a salir solo.
**4.** Aparece, `Exited (137)`. `stop` manda `SIGTERM` y espera diez segundos; `sleep` no lo atiende, así que le cae el `SIGKILL`, y eso es el 137. Compáralo con el `Exited (0)` del paso 2: **mismo estado final, causa distinta, y el código lo dice**.
**5.** **No aparece.** `rm` lo saca de la lista y borra su capa de escritura. Si querías algo de adentro, ya se fue.

**El `exec` que falla.** El mensaje es `Error response from daemon: container ... is not running`. La razón es que `exec` **no arranca nada: se mete en lo que ya existe.** Lo que necesita son los namespaces y el cgroup del contenedor, y esos existen sólo mientras hay un proceso vivo dentro de ellos; cuando el `PID` 1 terminó, se fueron con él y no hay adónde entrar. No es una prohibición de Docker, es que no queda vista en la que meterse.

De ahí sale el reflejo correcto para el resto del curso: si `exec` te dice `is not running`, **no insistas con `exec`**. Corre `docker ps -a` para ver el código de salida y `docker logs` para ver qué alcanzó a escribir; ésos son los dos comandos que sí funcionan sobre un contenedor muerto.
:::

Sigue con [[el-dockerfile-por-dentro]], que construye la imagen sobre la que corre todo esto.

> [!NOTE]
> **Si sólo recuerdas una cosa:** el contenedor vive lo que vive su `PID` 1; si terminó, `exec` no tiene dónde entrar y lo que queda son `ps -a` y `logs`.
