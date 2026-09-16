---
id: que-es-un-contenedor
title: "Qué es un contenedor"
nav_title: "Qué es un contenedor"
summary: "Un proceso de Linux con la vista recortada y la despensa medida: namespaces, cgroups, y el kernel que se comparte."
status: ready
estimated_time: 12m
tags: [contenedor, namespace, cgroup, kernel, proc, pid, kata]
prerequisites: [en-mi-maquina-si-funciona]
---

# Qué es un contenedor

**Página 2 de 9 · sección 1 de 3**

Meta: que «proceso aislado» deje de ser una frase hecha.

::: figure {#cont-ns-cgroups title="Namespaces: qué puede ver. Cgroups: cuánto puede usar"}
![Un proceso dentro de un recuadro partido en dos mitades. A la izquierda, bajo el rótulo «qué puede ver», seis cajas de namespace etiquetadas pid, net, mnt, user, uts e ipc, con cgroup y time en gris al pie como los dos tipos que faltan para llegar a ocho. A la derecha, bajo «cuánto puede usar», tres medidores de cgroup etiquetados CPU, memoria y número de procesos. La caja user va resaltada y unida al kernel del host por una línea continua, porque es el único de los diez enlaces que imprime ls /proc/1/ns/ que no difiere del host. Una nota al pie explica por qué son diez enlaces y ocho tipos: pid y time aparecen además en su variante _for_children](../_assets/cont-ns-cgroups.svg)
:::

## En corto

- Un contenedor es **un proceso de Linux normal** que comparte el kernel del host; no hay una máquina pequeña adentro.
- **Namespaces** deciden qué puede **ver** ese proceso; **cgroups** deciden cuánto puede **usar**.
- Hay **ocho tipos** de namespace, pero `ls /proc/<pid>/ns/` imprime **diez** enlaces, y con Docker por defecto sólo uno de los diez coincide con el host.

## El modelo mental equivocado sale caro

Casi todo el mundo llega pensando que un contenedor es una máquina virtual chiquita, y esa creencia hace predicciones falsas: que tarda medio minuto en arrancar, que tiene su propio kernel, que sigue prendido aunque su programa termine. Las tres son falsas, y de la tercera se cuelga la pregunta número uno del principiante en la sesión 2.

La forma más rápida de tirar la creencia es mirar desde afuera. Si el contenedor fuera una máquina, el host no vería sus procesos, igual que tu laptop no ve los procesos de una máquina virtual. Pero los ve: un `ps` en el host lista el proceso del contenedor con su PID del host, como cualquier otro. Está ahí, en la misma tabla de procesos, corriendo sobre el mismo kernel.

**Un contenedor no es una máquina pequeña: es un proceso de Linux con la vista recortada y la despensa medida.**

::: definition {#cont-def-pid title="`PID` y `/proc`"}
Un **`PID`** (*process id*) es el número con el que el kernel identifica a cada proceso vivo; el primero que arranca es el `PID` 1 y es el antepasado de todos los demás.

**`/proc`** es un sistema de archivos falso —no toca el disco— donde el kernel publica su estado como si fueran archivos: `/proc/<pid>/` es lo que el kernel sabe del proceso `<pid>`, y se lee con las mismas herramientas que cualquier archivo.
:::

## Namespaces: qué puede ver

Un *namespace* es una vista recortada de un recurso del kernel. El proceso pide ver «los procesos» o «la red» y el kernel le contesta con su recorte, no con el todo. No hay copia, no hay emulación y no hay costo: es el mismo kernel contestando distinto según quién pregunta.

::: table {#cont-tabla-ns title="Los seis namespaces que vas a notar"}

| Namespace | Qué recorta | Qué ves desde adentro |
|---|---|---|
| `pid` | la tabla de procesos | tu programa es el `PID` 1 y no existe ningún otro proceso del host |
| `net` | la pila de red | tus propias interfaces y tus propios puertos, separados de los del host |
| `mnt` | el árbol de archivos | el sistema de archivos de la imagen, no el tuyo |
| `uts` | el nombre de la máquina | un *hostname* propio, que por defecto es el id del contenedor |
| `ipc` | memoria compartida y colas | sólo las tuyas |
| `user` | el mapeo de usuarios | **con Docker, por defecto, nada**: ver la sección de abajo |

:::

## Ocho tipos, diez enlaces

Los que faltan para llegar a ocho son `cgroup` —que Docker activa por defecto sobre cgroups v2 desde la 20.10, y que le oculta al proceso en qué parte de la jerarquía de cgroups vive— y `time`, que permite correr con otro reloj monótono.

Pero si cuentas los enlaces de `ls /proc/<pid>/ns/` vas a obtener **diez**, no ocho, y no es que esta página te haya mentido: `pid` y `time` aparecen **dos veces cada uno**, en su forma normal y en su variante `_for_children`. La segunda no es el namespace del proceso, es el que **heredarán sus hijos**. Son diez enlaces sobre ocho tipos.

## Cgroups: cuánto puede usar

Los namespaces no limitan nada: un proceso que sólo se ve a sí mismo puede seguir comiéndose toda la RAM de la máquina. Eso lo pone el otro mecanismo, los *control groups*: un árbol de grupos donde cada nodo tiene cuotas de CPU, de memoria y de número de procesos, y el kernel contabiliza lo que consumen todos sus miembros.

Namespaces y cgroups son **ortogonales** y separables. Un contenedor típico usa los dos, pero puedes tener recorte de vista sin cuota, o cuota sin recorte de vista — de hecho, tu propia sesión de escritorio ya vive dentro de un cgroup.

## La fila incómoda: `user`

Aquí va la verdad que la mitad de internet dice al revés: **Docker no activa user namespaces por defecto.** Sin ese namespace, el UID 0 de adentro **es** el UID 0 del host; no hay traducción. El proceso está recortado por todos los demás namespaces y confinado por *capabilities*, seccomp y AppArmor, pero su usuario no está mapeado a otro.

Se puede activar, con `userns-remap` en la configuración del daemon, y Podman *rootless* lo hace siempre: ahí el root de adentro se mapea a **tu** usuario. La consecuencia práctica de no tenerlo se toca con la mano en la sesión 2, cuando un archivo escrito desde el contenedor aparezca en tu carpeta siendo de `root`.

Y si el kernel es uno solo y compartido, queda una pregunta abierta: **¿qué haces cuando no quieres compartirlo?** Se llama **Kata Containers**, y es lo último de esta unidad, en la sesión 3.

::: problem {#cont-p2-diez-enlaces title="Diez enlaces, ¿cuántos difieren?"}
Se reparte impresa la salida de los dos lados. Arriba, `ls -la /proc/1/ns/` en el host. Abajo, `docker exec <nombre> ls -la /proc/1/ns/` en un contenedor recién arrancado. Se recortaron los permisos, el dueño y la fecha, que son idénticos en los veinte renglones:

```text
HOST                                   CONTENEDOR
cgroup            -> cgroup:[4026531835]     cgroup            -> cgroup:[4026532678]
ipc               -> ipc:[4026531839]        ipc               -> ipc:[4026532554]
mnt               -> mnt:[4026531841]        mnt               -> mnt:[4026532552]
net               -> net:[4026531840]        net               -> net:[4026532556]
pid               -> pid:[4026531836]        pid               -> pid:[4026532555]
pid_for_children  -> pid:[4026531836]        pid_for_children  -> pid:[4026532555]
time              -> time:[4026531834]       time              -> time:[4026532679]
time_for_children -> time:[4026531834]       time_for_children -> time:[4026532679]
user              -> user:[4026531837]       user              -> user:[4026531837]
uts               -> uts:[4026531838]        uts               -> uts:[4026532553]
```

En parejas: **¿cuántos de los diez difieren, y cuál no?** Y la de verdad importante: ¿qué consecuencia tiene el que no difiere?
:::

::: hint {of="cont-p2-diez-enlaces"}
El número entre corchetes es el inodo del namespace: si es el mismo número, es literalmente el mismo namespace, no uno igualito. Busca el renglón donde las dos columnas coinciden y vuelve a leer la sección de arriba que habla de él.
:::

::: answer {of="cont-p2-diez-enlaces"}
**Difieren nueve. El único que coincide es `user`.**

El contenedor tiene su propia tabla de procesos, su propia red, su propio árbol de archivos, su propio nombre de máquina — todo eso son inodos nuevos. Pero comparte el user namespace del host, porque **Docker no lo activa por defecto**.

Y ésa es toda la explicación de algo que te va a pasar en el laboratorio de la sesión 2: cuando el contenedor escriba un archivo en una carpeta tuya, el archivo va a salir siendo de **`root`**. No es un bug ni un permiso mal puesto: el UID 0 de adentro es el UID 0 de afuera, porque nadie los separó.

Si en tu propia salida `time` y `time_for_children` también coinciden con el host, es que tu runtime no creó un *time namespace* —es lo único de los diez que cambia entre runtimes y versiones— y el conteo te da ocho. El renglón que importa no se mueve: `user` coincide **siempre** con Docker por defecto.
:::

Sigue con [[receta-imagen-contenedor]], que separa las tres cosas que todo el mundo confunde.

> [!NOTE]
> **Si sólo recuerdas una cosa:** namespaces es qué puede ver y cgroups es cuánto puede usar; el kernel siempre es el del host.
