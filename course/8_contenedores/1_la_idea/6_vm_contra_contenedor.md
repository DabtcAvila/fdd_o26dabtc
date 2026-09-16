---
id: vm-contra-contenedor
title: "VM contra contenedor"
nav_title: "VM contra contenedor"
summary: "Dónde ocurre el aislamiento en cada uno, tres casos en los que el contenedor no es la respuesta, y por qué en macOS y Windows siempre hay una VM de por medio."
status: ready
estimated_time: 10m
tags: [vm, hipervisor, kernel, aislamiento, gvisor, kata, macos, windows]
prerequisites: [escalamiento-y-orquestacion]
---

# VM contra contenedor

**Página 6 de 9 · sección 1 de 3**

Meta: entender dónde ocurre el aislamiento, y cuándo el contenedor no es la respuesta.

::: figure {#cont-vm-vs-contenedor title="Dónde está la frontera del aislamiento en cada pila"}
![Dos pilas lado a lado sobre el mismo hardware. A la izquierda, tres máquinas virtuales: cada una lleva su proceso, un sistema operativo completo con init, librerías y paquetes, y su propio kernel invitado; las tres se apoyan en un hipervisor —KVM, QEMU o Hyper-V— que está resaltado como la frontera del aislamiento. A la derecha, tres contenedores: cada uno lleva sólo su proceso y su rootfs con lo que se pidió, y los tres se apoyan directamente en un único kernel del host, también resaltado, porque ahí está la frontera de ese lado. Un recuadro enumera lo que el contenedor no lleva: ningún kernel invitado, ningún sistema operativo completo, ningún hipervisor. Al pie, una franja comparativa de tres filas: arranque, decenas de segundos contra cientos de milisegundos; tamaño en disco, gigabytes contra decenas o cientos de megabytes; y un bug del kernel, que en la VM tumba al invitado mientras el host sigue, y del lado del contenedor cae el kernel de todos porque no hay un segundo kernel](../_assets/cont-vm-vs-contenedor.svg)
:::

## En corto

- La diferencia no es de tamaño: es **dónde está la frontera**. En la VM la pone el hipervisor, debajo de un kernel invitado; en el contenedor la pone el kernel del host, que es uno solo para todos.
- Todo lo bueno del contenedor —arranca en milisegundos, pesa megabytes— sale de no llevar kernel propio, y todo lo malo también.
- Hay tres casos en los que la respuesta correcta sigue siendo una máquina virtual.

## La misma tabla, leída dos veces

::: table {#cont-tabla-vm title="Máquina virtual contra contenedor"}

| | Máquina virtual | Contenedor |
|---|---|---|
| Qué aísla | hardware virtual completo, con su hipervisor | vistas del kernel: namespaces y cgroups |
| Kernel | uno **propio** por cada VM | el del host, **compartido** por todos |
| Qué arranca | un sistema operativo entero, desde cero | un proceso |
| Arranque | decenas de segundos | cientos de milisegundos |
| Tamaño en disco | gigabytes | decenas o cientos de MB |
| Costo mientras corre | el del sistema operativo invitado, siempre encendido | el de tu proceso y nada más |
| Un bug del kernel | cae el invitado; el host sigue | cae el kernel de todos: **no hay un segundo kernel** |
| Kernel distinto del host | sí, cualquiera | no: es literalmente el mismo |

:::

Las primeras seis filas son el argumento a favor del contenedor y son las que todo el mundo cita. Las dos últimas son la letra chica, y son las que deciden los tres casos de abajo. **Las ocho filas salen de la misma causa**: no hay un segundo kernel. Por eso arranca rápido, por eso pesa poco, y por eso no te protege de un kernel roto.

## Tres veces que el contenedor no es la respuesta

**1. Necesitas hardware directo.** Un dispositivo que hay que manejar de verdad, un módulo de kernel propio, un driver que no está en el host. Un contenedor no tiene kernel, así que no tiene dónde cargar un módulo: lo que carga módulos es el kernel del host, y hacerlo desde adentro requiere romper el aislamiento por completo. Si tu programa necesita su propio kernel para hablar con el fierro, necesitas una máquina.

**2. Necesitas aislamiento máximo.** Vas a correr código que no escribiste tú y que podría ser hostil: la entrega de un alumno, el trabajo de un cliente, un binario que te llegó por correo. Un contenedor comparte el kernel, así que todo el kernel es superficie de ataque: una vulnerabilidad ahí se salta el aislamiento. **Ésta es una deuda que sí se paga**, y con una respuesta intermedia: hay runtimes que ponen un segundo kernel debajo del contenedor sin renunciar a la forma de trabajar con imágenes. Se llama **Kata**, y es lo último de la unidad, en la sesión 3.

**3. Necesitas un kernel distinto.** Correr Windows sobre Linux, probar contra un kernel viejo, usar una característica que tu host no tiene. No hay truco posible: el kernel del contenedor **es** el del host. Lo que se necesita es una VM, y de hecho es justo lo que hacen Docker Desktop y `podman machine` — que es la siguiente sección de esta página.

## En macOS y en Windows siempre hay una VM de por medio

Este hecho sostiene tres páginas de la sesión 2, así que vale la pena decirlo despacio: **los contenedores son una función del kernel de Linux.** Namespaces y cgroups son código de Linux; no existen en el kernel de macOS ni en el de Windows.

Entonces, ¿cómo corre `docker run` en una MacBook? Porque hay **una máquina virtual con Linux adentro**, encendida todo el tiempo. Docker Desktop la arranca por ti y la esconde bien; con Podman la arrancas explícitamente, con `podman machine init` y `podman machine start`, y por eso ahí el detalle no se puede ignorar. En Windows el papel lo hace WSL2, que también es una VM con un kernel de Linux real adentro. En los tres casos el contenedor sigue siendo un proceso de Linux sobre un kernel de Linux — sólo que ese kernel no es el de tu sistema operativo.

De ahí salen consecuencias que se tocan con la mano en la sesión 2 y que no son curiosidades: montar una carpeta tuya dentro del contenedor **cruza la frontera de esa VM**, y eso lo hace más lento y hace que los permisos y el dueño de los archivos se comporten distinto que en Linux nativo. Si trabajas en Mac o en Windows, ese renglón te va a tocar.

## El aislamiento no es una línea

![Rejilla de dos ejes que ordena las opciones de aislamiento. El eje horizontal pregunta dónde aterriza la syscall que no controlas y va de izquierda a derecha: proceso suelto y contenedor, que la mandan directo al kernel del host; gVisor, que la manda a un núcleo en espacio de usuario que reimplementa la interfaz de syscalls de Linux; Kata, que la manda a un segundo kernel real dentro de una VM ligera; y la VM completa, que la manda a un kernel invitado detrás del hipervisor. El eje vertical pregunta qué privilegio tiene quien se escapa, y va de root en el host abajo a un usuario sin privilegios con su rango de subuid arriba. Contenedor rootful y contenedor rootless ocupan la misma columna y sólo se separan en el eje vertical, con una flecha corta que marca que rootless mueve un eje y no el otro; gVisor aparece dos veces, una a cada altura, porque tiene su propio modo rootless. Al pie, la conclusión: rootless no añade ninguna frontera, mismo kernel y misma superficie de syscalls, y los dos ejes se componen en vez de ordenarse](../_assets/cont-espectro.svg)

Entre «contenedor» y «máquina virtual» hay cosas en medio, y una de ellas aparece aquí por primera vez: **gVisor**, que no pone un kernel real ni renuncia a poner uno, sino que **reimplementa la interfaz de syscalls de Linux en espacio de usuario** y atiende ahí las llamadas de tu proceso. La figura de arriba es la que se desarma entera en la sesión 3; por ahora quédate con que no es una recta de «poco» a «mucho» aislamiento, sino dos preguntas distintas que se responden por separado.

::: problem {#cont-p6-si-fuera-vm title="Lo mismo, pero en una VM"}
Este comando arranca un contenedor que sirve una página web:

```bash
docker run -d -p 8080:80 --memory 512m nginx:1.27
```

Arranca en unos cientos de milisegundos y la imagen pesa unas decenas de MB. Ahora responde, para el caso en que exactamente lo mismo se hiciera levantando una máquina virtual con Ubuntu e instalando nginx adentro:

1. **Arranque** — ¿en qué cambia el tiempo, y por qué?
2. **Tamaño** — ¿qué hay que descargar y guardar en cada caso?
3. **Kernel** — ¿cuál kernel ejecuta a `nginx` en cada caso?
4. **Qué ve del host** — si alguien se escapa de `nginx`, ¿en qué máquina aparece?

Una frase por respuesta, y en la 4 di **qué tendría que romper** para llegar al host en cada caso.
:::

::: hint {of="cont-p6-si-fuera-vm"}
Las cuatro preguntas tienen la misma causa detrás, y está en la tabla de arriba: la VM lleva un kernel propio y el contenedor no. Contesta cada una empezando por ahí.
:::

::: answer {of="cont-p6-si-fuera-vm"}
**1. Arranque.** De cientos de milisegundos a decenas de segundos. El contenedor sólo hace nacer un proceso —el rootfs ya estaba en disco desde el `pull`—; la VM arranca un sistema operativo completo: firmware, kernel, init, servicios y hasta entonces `nginx`.

**2. Tamaño.** El contenedor baja las capas de `nginx:1.27`, decenas de MB, y **comparte** las que ya tuvieras de otras imágenes. La VM necesita una imagen de disco con Ubuntu entero: gigabytes, y no comparte nada con nadie.

**3. Kernel.** En el contenedor, `nginx` corre sobre **el kernel de tu host**, el mismo que ejecuta tu navegador. En la VM corre sobre **un kernel invitado propio**, que puede ser de otra versión o de otra distribución. El límite de `--memory 512m` también cambia de naturaleza: en el contenedor es una cuota de cgroup que el kernel del host contabiliza; en la VM es memoria que el hipervisor le entrega al invitado y que el invitado administra por su cuenta.

**4. Qué ve del host.** En los dos casos `nginx` empieza viendo poco. La diferencia es qué hay que romper para salir: desde el contenedor, **una vulnerabilidad del kernel del host** —y ese kernel es el tuyo, el que corre todo lo demás—; desde la VM, primero el kernel invitado y **después** el hipervisor, que es una segunda frontera y mucho más chica. Por eso el caso 2 de arriba sigue siendo de VM, y por eso existe Kata.
:::

> [!NOTE]
> **Si sólo recuerdas una cosa:** el contenedor no lleva kernel propio; de ahí sale que arranque en milisegundos y de ahí sale que un bug del kernel sea un bug de todos.
