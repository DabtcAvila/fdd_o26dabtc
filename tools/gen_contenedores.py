"""Genera las figuras conceptuales SVG de la unidad de Contenedores.

Mismo patron que gen_regex.py y gen_git.py: paleta importada de svg_base, una
funcion por figura que devuelve una cadena SVG completa, y un catalogo
DIAGRAMAS que el generador y su prueba comparten como unica fuente de "que
figuras existen".

El catalogo de este modulo FUSIONA las figuras conceptuales con las cuatro
graficas de benchmark de gen_contenedores_bench.py, que dibujan CSV en vez de
ideas. Quien importe DIAGRAMAS de aqui ve las treinta figuras de la unidad.

Solo biblioteca estandar, a proposito: la guarda de la unidad IMPORTA este
modulo y el runner de CI solo instala pytest, pillow y pyyaml.

La raiz <svg> sale siempre de svg_base.marco(): trae width y height numericos
sin unidades y un viewBox que empieza en "0 0", que es lo que exige
test_svg_tamano_intrinseco.py. Cada SVG hornea su fondo y usa `fill` explicito
en todo texto, para que se lea igual en tema claro y en tema oscuro.

Los ids llevan prefijo "cont-" a proposito: los ids de objeto numerado de Raya
son unicos en TODO el curso, no por pagina.
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "course/8_contenedores/_assets"

from svg_base import (  # noqa: F401  (se reexportan para las guardas)
    FONDO, PANEL, TEXTO, SUAVE, LINEA, ACENTO, TINTE, AMBAR, CIAN, VIOLETA,
    ROJO, FUENTE, MONO, COLORES_FLECHA, arco, bucle, caja, celda, chip,
    cierre, cima_arco, curva, estado, flecha, marco, teclado, texto, _marca,
)

from gen_contenedores_bench import DIAGRAMAS as DIAGRAMAS_BENCH


# --------------------------------------------------------------------------
# Primitivas locales
#
# svg_base.py no se toca: modificarla regenera y revalida los 32 SVG de las
# unidades 6 y 7. Lo que falta aqui —trazos punteados, circulos, elipses— se
# construye sobre su paleta y sobre sus markers de punta de flecha.
# --------------------------------------------------------------------------


def linea(x1, y1, x2, y2, color=LINEA, grosor=2, guion=None):
    trazo = f' stroke-dasharray="{guion}"' if guion else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="{grosor}"{trazo}/>'
    )


def flecha_punteada(x1, y1, x2, y2, color=SUAVE, grosor=2, guion="6 6"):
    """flecha() de svg_base, pero con el trazo cortado."""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="{grosor}" stroke-dasharray="{guion}" '
        f'marker-end="url(#{_marca(color)})"/>'
    )


def caja_punteada(x, y, w, h, borde=SUAVE, radio=10, grosor=1.5, guion="7 7"):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radio}" '
        f'fill="none" stroke="{borde}" stroke-width="{grosor}" '
        f'stroke-dasharray="{guion}"/>'
    )


def relleno(x, y, w, h, color, radio=3):
    """Rectangulo macizo sin borde: barras, medidores, iconos."""
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" '
        f'height="{max(h, 0):.1f}" rx="{radio}" fill="{color}"/>'
    )


def circulo(cx, cy, r, color, borde="none", grosor=2):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" '
        f'stroke="{borde}" stroke-width="{grosor}"/>'
    )


def elipse(cx, cy, rx, ry, color, borde=LINEA, grosor=2):
    return (
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}" '
        f'stroke="{borde}" stroke-width="{grosor}"/>'
    )


def bloque(x, y, w, h, titulo, glosa, color, relleno_caja=PANEL,
           tam_titulo=15, mono=True, grosor=2):
    """Caja de cadena: un nombre arriba y su papel en una linea chica."""
    p = [caja(x, y, w, h, relleno_caja, color, radio=10, grosor=grosor)]
    escribir_titulo = teclado if mono else texto
    p.append(escribir_titulo(x + w / 2, y + h / 2 - 4, titulo, color,
                             tam_titulo))
    if glosa:
        p.append(texto(x + w / 2, y + h / 2 + 20, glosa, SUAVE, 11.5))
    return "".join(p)


def cadena(x0, y, alto_caja, piezas, sep=60, color_flecha=SUAVE):
    """Fila de cajas unidas por flechas. piezas = [(ancho, nombre, papel, color)]."""
    p = []
    x = x0
    centros = []
    for i, (ancho, nombre, papel, color) in enumerate(piezas):
        if i:
            p.append(flecha(x - sep + 4, y + alto_caja / 2, x - 6,
                            y + alto_caja / 2, color_flecha))
        p.append(bloque(x, y, ancho, alto_caja, nombre, papel, color))
        centros.append((x + ancho / 2, x, x + ancho))
        x += ancho + sep
    return "".join(p), centros


# --------------------------------------------------------------------------
# 1/1 · En mi maquina si funciona: el contenedor intermodal
# --------------------------------------------------------------------------

def _bultos(cx, cy):
    """Carga suelta: un barril, un saco y una caja, de tres tamanos."""
    return "".join((
        relleno(cx - 40, cy - 14, 20, 28, AMBAR, radio=6),
        relleno(cx - 13, cy - 9, 22, 22, VIOLETA, radio=10),
        relleno(cx + 15, cy - 16, 26, 32, ROJO, radio=3),
    ))


def _contenedor_icono(cx, cy):
    """El bulto sellado: una caja con corrugado y su precinto."""
    p = [caja(cx - 42, cy - 17, 84, 34, TINTE, ACENTO, radio=4, grosor=2.5)]
    for i in range(1, 4):
        p.append(linea(cx - 42 + i * 21, cy - 15, cx - 42 + i * 21, cy + 15,
                       ACENTO, 1.2))
    p.append(circulo(cx + 42, cy, 5, FONDO, ACENTO, 2))
    return "".join(p)


def cont_intermodal():
    """El mismo recorrido, con la carga suelta y con la caja sellada."""
    ancho, alto = 1240, 560
    aria = (
        "Dos recorridos paralelos del mismo muelle a la misma bodega pasando "
        "por camion, barco y tren. Arriba, la carga suelta de antes de 1956 se "
        "descarga y se vuelve a cargar en cada trasbordo, con su costo "
        "marcado; abajo, el contenedor sellado pasa de vehiculo en vehiculo "
        "sin abrirse. A la derecha, las equivalencias con el software: la "
        "carga es tu programa con sus dependencias, el contenedor es la "
        "imagen y los tres vehiculos son tu laptop, la maquina del companero "
        "y el servidor"
    )
    nodos = ("muelle", "camión", "barco", "tren", "bodega")
    w, sep, x0 = 108, 63, 40
    centros = [x0 + i * (w + sep) + w / 2 for i in range(5)]
    huecos = [x0 + i * (w + sep) + w + sep / 2 for i in range(4)]

    p = [marco(ancho, alto, aria)]
    p.append(texto(620, 42, "Del muelle a la bodega, dos maneras", TEXTO, 21, peso="600"))
    p.append(texto(620, 68, "el contenedor intermodal de McLean, 1956 — y el mismo truco en software", SUAVE, 14))

    # Recorrido de arriba: carga suelta.
    p.append(texto(x0, 104, "antes de 1956 · carga suelta", ROJO, 15, anclaje="start", peso="600"))
    for i, nombre in enumerate(nodos):
        x = x0 + i * (w + sep)
        p.append(caja(x, 118, w, 88, PANEL, ROJO))
        p.append(texto(x + w / 2, 140, nombre, TEXTO, 13.5))
        p.append(_bultos(x + w / 2, 176))
        if i:
            p.append(flecha(x - sep + 4, 162, x - 6, 162, ROJO))
    for hx in huecos:
        p.append(texto(hx, 228, "descargar y recargar", ROJO, 12))
        p.append(texto(hx, 246, "+ tiempo + costo", AMBAR, 12, peso="600"))

    # Recorrido de abajo: el bulto sellado.
    p.append(texto(x0, 284, "desde 1956 · el contenedor intermodal", ACENTO, 15, anclaje="start", peso="600"))
    for i, nombre in enumerate(nodos):
        x = x0 + i * (w + sep)
        p.append(caja(x, 298, w, 88, PANEL, ACENTO))
        p.append(texto(x + w / 2, 320, nombre, TEXTO, 13.5))
        p.append(_contenedor_icono(x + w / 2, 356))
        if i:
            p.append(flecha(x - sep + 4, 342, x - 6, 342, ACENTO))
    p.append(texto(436, 412, "en ningún trasbordo se abre la caja: se mueve entera, sellada", ACENTO, 13))
    for i, maquina in enumerate(("tu laptop", "la máquina del compañero", "el servidor")):
        p.append(texto(centros[i + 1], 442, maquina, CIAN, 12.5))

    # La columna de equivalencias.
    p.append(caja(880, 100, 320, 348, PANEL, CIAN))
    p.append(texto(1040, 130, "lo mismo, en software", CIAN, 16, peso="600"))
    p.append(linea(900, 252, 1180, 252, LINEA, 1))
    p.append(linea(900, 340, 1180, 340, LINEA, 1))
    p.append(texto(1040, 168, "la carga suelta", SUAVE, 13))
    p.append(texto(1040, 190, "≡", SUAVE, 15))
    p.append(texto(1040, 214, "tu programa, con todas", TEXTO, 14, peso="600"))
    p.append(texto(1040, 234, "sus dependencias", TEXTO, 14, peso="600"))
    p.append(texto(1040, 274, "el contenedor sellado", SUAVE, 13))
    p.append(texto(1040, 296, "≡", SUAVE, 15))
    p.append(teclado(1040, 322, "la imagen", ACENTO, 18))
    p.append(texto(1040, 362, "los tres vehículos", SUAVE, 13))
    p.append(texto(1040, 384, "≡", SUAVE, 15))
    p.append(texto(1040, 408, "tu laptop, la máquina del", CIAN, 13.5, peso="600"))
    p.append(texto(1040, 428, "compañero y el servidor", CIAN, 13.5, peso="600"))

    p.append(texto(620, 500, "McLean no inventó la caja: inventó que nadie tuviera que abrirla. En cada trasbordo se mueve el bulto entero, sellado.", SUAVE, 14))
    p.append(texto(620, 526, "Una imagen es eso. La máquina que la recibe no la abre para acomodar lo de adentro: la corre tal cual llegó.", SUAVE, 14))
    p.append(cierre())
    return "".join(p)


# --------------------------------------------------------------------------
# 1/2 · Namespaces y cgroups: dos preguntas distintas
# --------------------------------------------------------------------------

def _medidor(x, y, w, etiqueta, limite, fraccion, color, glosa):
    """Un cgroup: cuanto de un recurso puede usar el proceso."""
    return "".join((
        texto(x, y - 10, etiqueta, TEXTO, 14, anclaje="start", peso="600"),
        texto(x + w, y - 10, limite, color, 13, anclaje="end"),
        caja(x, y, w, 24, PANEL, LINEA, radio=6, grosor=1.5),
        relleno(x + 2, y + 2, (w - 4) * fraccion, 20, color, radio=5),
        texto(x, y + 44, glosa, SUAVE, 11.5, anclaje="start"),
    ))


def cont_ns_cgroups():
    """Namespaces = que puede ver. cgroups = cuanto puede usar."""
    ancho, alto = 1180, 700
    aria = (
        "Un proceso partido en dos mitades. A la izquierda, bajo el rotulo que "
        "puede ver, seis cajas de namespace etiquetadas pid, net, mnt, user, "
        "uts e ipc, con cgroup y time al pie como los dos tipos que faltan "
        "para llegar a ocho. A la derecha, bajo cuanto puede usar, tres "
        "medidores de cgroup para CPU, memoria y numero de procesos. La caja "
        "user va resaltada y unida por una linea continua al kernel del host, "
        "porque es el unico de los diez enlaces que no difiere del host"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(590, 42, "Namespaces y cgroups: dos preguntas distintas", TEXTO, 21, peso="600"))
    p.append(texto(590, 68, "no son dos mitades de lo mismo", SUAVE, 14))

    p.append(caja(40, 92, 1100, 356, "none", LINEA))
    p.append(texto(60, 116, "el proceso del contenedor", SUAVE, 13.5, anclaje="start"))
    p.append(linea(600, 100, 600, 440, LINEA, 1.5, "6 6"))

    p.append(texto(320, 152, "qué puede VER", CIAN, 18, peso="600"))
    p.append(texto(320, 174, "namespaces", SUAVE, 13))
    p.append(texto(870, 152, "cuánto puede USAR", AMBAR, 18, peso="600"))
    p.append(texto(870, 174, "cgroups", SUAVE, 13))

    ns = (
        ("pid", "qué procesos ve", CIAN, False),
        ("net", "su propia red", CIAN, False),
        ("mnt", "qué archivos ve", CIAN, False),
        ("user", "qué UID es adentro", AMBAR, True),
        ("uts", "su propio hostname", CIAN, False),
        ("ipc", "memoria compartida", CIAN, False),
    )
    for i, (nombre, glosa, color, resaltado) in enumerate(ns):
        x = 60 + (i % 3) * 180
        y = 196 + (i // 3) * 82
        p.append(caja(x, y, 160, 66, PANEL, color, grosor=3 if resaltado else 2))
        p.append(teclado(x + 80, y + 28, nombre, color, 17))
        p.append(texto(x + 80, y + 50, glosa, SUAVE, 11.5))

    p.append(caja_punteada(200, 360, 380, 56, SUAVE))
    p.append(texto(212, 392, "y dos tipos más, para ocho:", SUAVE, 12.5, anclaje="start"))
    p.append(chip(462, 388, "cgroup", SUAVE, tam=13))
    p.append(chip(548, 388, "time", SUAVE, tam=13))

    p.append(_medidor(660, 220, 440, "CPU", "--cpus=0.5", 0.5, AMBAR,
                      "ve todos los núcleos; sólo no puede usarlos todos"))
    p.append(_medidor(660, 300, 440, "memoria", "--memory=512m", 0.35, VIOLETA,
                      "pasarse no da un error: da un OOM kill"))
    p.append(_medidor(660, 380, 440, "procesos", "--pids-limit=100", 0.2, CIAN,
                      "el tope de PIDs: lo que frena una bomba de forks"))

    # El unico enlace que no difiere del host baja hasta el kernel compartido.
    p.append(flecha(140, 344, 140, 562, AMBAR, 2.5))

    p.append(caja(40, 496, 1100, 56, TINTE, ACENTO, grosor=2.5))
    p.append(texto(590, 530, "kernel del host — uno solo, compartido", TEXTO, 16, peso="600"))

    p.append(caja(40, 566, 520, 60, PANEL, AMBAR))
    p.append(texto(300, 590, "user es el único de los diez enlaces que NO difiere del host", AMBAR, 13, peso="600"))
    p.append(texto(300, 610, "Docker no activa user namespaces por omisión: root adentro es root afuera", SUAVE, 12))

    p.append(texto(590, 656, "ls /proc/1/ns/ imprime DIEZ enlaces y aquí hay OCHO tipos: pid y time salen además en su variante _for_children,", SUAVE, 13.5))
    p.append(texto(590, 678, "el namespace que heredarán los hijos. De esos diez, nueve difieren del host.", SUAVE, 13.5))
    p.append(cierre())
    return "".join(p)


# --------------------------------------------------------------------------
# 1/3 · Receta, congelado, servido
# --------------------------------------------------------------------------

def cont_tres_abstracciones():
    """Dockerfile, imagen y contenedor como receta, congelado y servido."""
    ancho, alto = 1160, 520
    aria = (
        "Tres paneles en fila con su analogia arriba y su termino abajo: la "
        "receta escrita es el Dockerfile, el platillo congelado es la imagen y "
        "el platillo servido es el contenedor, unidos por las flechas docker "
        "build y docker run. Del platillo congelado salen tres platos servidos "
        "identicos; bajo la imagen dice inmutable y bajo los contenedores dice "
        "efimeros"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(580, 42, "Receta, congelado, servido", TEXTO, 21, peso="600"))
    p.append(texto(580, 68, "las tres cosas que todo el mundo confunde", SUAVE, 14))

    p.append(caja(40, 96, 280, 330, PANEL, CIAN))
    p.append(texto(180, 128, "la receta escrita", SUAVE, 14))
    p.append(caja(100, 150, 160, 170, FONDO, CIAN, radio=8, grosor=1.5))
    for i, linea_df in enumerate(("FROM python:3.12", "WORKDIR /app", "COPY . .",
                                  "RUN pip install", "CMD [\"python\"]")):
        p.append(teclado(112, 178 + i * 24, linea_df, SUAVE, 11.5,
                         anclaje="start", peso="normal"))
    p.append(teclado(180, 368, "Dockerfile", CIAN, 20))
    p.append(texto(180, 396, "texto, y va en git", SUAVE, 12.5))

    p.append(caja(440, 96, 280, 330, PANEL, VIOLETA))
    p.append(texto(580, 128, "el platillo congelado", SUAVE, 14))
    for dx, dy in ((-40, 202), (0, 190), (40, 202)):
        p.append(teclado(580 + dx, dy, "❄", CIAN, 17))
    p.append(elipse(580, 248, 88, 30, PANEL, VIOLETA, 2.5))
    p.append(elipse(580, 242, 54, 18, FONDO, VIOLETA, 1.5))
    p.append(teclado(580, 300, "sha256:6a2f…", SUAVE, 12.5, peso="normal"))
    p.append(teclado(580, 368, "imagen", VIOLETA, 20))
    p.append(texto(580, 396, "inmutable", VIOLETA, 13, peso="600"))

    p.append(caja(840, 96, 280, 330, PANEL, ACENTO))
    p.append(texto(980, 128, "el platillo servido", SUAVE, 14))
    for cy in (180, 236, 292):
        p.append(elipse(980, cy, 70, 22, PANEL, ACENTO, 2))
        p.append(elipse(980, cy - 4, 42, 13, FONDO, ACENTO, 1.5))
    p.append(texto(980, 332, "tres, de la misma imagen", SUAVE, 12))
    p.append(teclado(980, 368, "contenedor", ACENTO, 20))
    p.append(texto(980, 396, "efímeros", ACENTO, 13, peso="600"))

    p.append(teclado(380, 150, "docker build", ACENTO, 15))
    p.append(flecha(326, 246, 434, 246, ACENTO))
    p.append(teclado(780, 150, "docker run", ACENTO, 15))
    for cy in (186, 240, 292):
        p.append(flecha(726, 246, 834, cy, ACENTO))

    p.append(texto(580, 468, "De una receta salen muchos congelados idénticos; de un congelado, muchos platos servidos.", SUAVE, 14))
    p.append(texto(580, 492, "Borrar el plato no toca el congelado. Cambiar la receta tampoco: para eso hay que volver a construir.", SUAVE, 13.5))
    p.append(cierre())
    return "".join(p)


# --------------------------------------------------------------------------
# 1/4 · Que pasa cuando escribes `docker run`
# --------------------------------------------------------------------------

def cont_anatomia_run():
    """La cadena real, con quien sostiene al proceso y quien ya se fue."""
    ancho, alto = 1280, 730
    aria = (
        "Cadena de cinco cajas: docker CLI, dockerd, containerd, "
        "containerd-shim-runc-v2 y runc, con el socket rotulado sobre la "
        "primera flecha. El proceso del contenedor cuelga del shim y no del "
        "daemon, y una flecha punteada sube del shim a PID 1 porque se "
        "desacopla con un doble fork. runc va en gris con marca de salida: "
        "corre en create y en start y sale las dos veces. Dos llamadas "
        "corrigen que el rootfs lo monta dockerd con overlay2 y que el cgroup "
        "lo crea systemd por D-Bus. Al pie, el orden real: proceso, cgroup, "
        "namespaces"
    )
    piezas = (
        (150, "docker", "lo que tecleas", CIAN),
        (150, "dockerd", "el daemon (root)", ROJO),
        (170, "containerd", "imágenes y tareas", VIOLETA),
        (236, "containerd-shim-runc-v2", "el supervisor del contenedor", ACENTO),
        (130, "runc", "crea y se va", SUAVE),
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(640, 42, "Qué pasa cuando escribes docker run", TEXTO, 21, peso="600"))
    p.append(texto(640, 68, "la cadena real, y qué queda de ella cuando el contenedor ya corre", SUAVE, 14))

    p.append(caja(770, 110, 200, 46, PANEL, SUAVE, radio=10, grosor=1.5))
    p.append(texto(870, 139, "PID 1 — systemd", TEXTO, 15, peso="600"))
    p.append(flecha_punteada(870, 196, 870, 162, SUAVE))
    p.append(texto(986, 130, "doble fork: el shim se desacopla", SUAVE, 12.5, anclaje="start"))
    p.append(texto(986, 148, "y queda reparentado a systemd", SUAVE, 12.5, anclaje="start"))

    x = 102
    bordes = []
    for i, (w, nombre, papel, color) in enumerate(piezas):
        if i:
            p.append(flecha(x - 56, 243, x - 6, 243, SUAVE))
        p.append(caja(x, 200, w, 86, PANEL, color))
        p.append(teclado(x + w / 2, 234, nombre, color, 14))
        p.append(texto(x + w / 2, 258, papel, SUAVE, 11.5))
        bordes.append((x, x + w, x + w / 2))
        x += w + 60
    p.append(teclado(282, 182, "/var/run/docker.sock", CIAN, 12.5, peso="normal"))

    # El proceso cuelga del shim, no del daemon.
    p.append(flecha(870, 290, 870, 348, ACENTO, 2.5))
    p.append(texto(744, 322, "cuelga del shim,", ACENTO, 12.5, anclaje="end", peso="600"))
    p.append(texto(744, 340, "no del daemon", ACENTO, 12.5, anclaje="end", peso="600"))
    p.append(caja(752, 352, 236, 92, TINTE, ACENTO))
    p.append(texto(870, 378, "el proceso del contenedor", TEXTO, 14, peso="600"))
    p.append(teclado(870, 404, "sleep 300", ACENTO, 15))
    p.append(texto(870, 426, "PID 1 dentro del contenedor", SUAVE, 11.5))

    # runc ya salio.
    p.append(chip(1113, 312, "sale ✗", SUAVE, tam=13))
    p.append(texto(1113, 346, "corre dos veces:", SUAVE, 11.5))
    p.append(texto(1113, 362, "create y start", SUAVE, 11.5))
    p.append(texto(1113, 378, "y sale las dos", SUAVE, 11.5))

    p.append(caja(50, 470, 596, 130, PANEL, AMBAR))
    p.append(texto(66, 498, "Dos cosas que se enseñan mal — y que runc NO hace", AMBAR, 14.5, anclaje="start", peso="600"))
    p.append(texto(66, 526, "· el rootfs ya está en disco desde el pull; lo monta dockerd con el", SUAVE, 12.5, anclaje="start"))
    p.append(texto(80, 544, "graphdriver overlay2 (o el shim, con el image store de containerd)", SUAVE, 12.5, anclaje="start"))
    p.append(texto(66, 570, "· el cgroup lo crea systemd: runc le pide una unidad scope por D-Bus", SUAVE, 12.5, anclaje="start"))
    p.append(texto(80, 588, "y sólo escribe los knobs que systemd no expone", SUAVE, 12.5, anclaje="start"))

    p.append(caja(680, 470, 550, 130, PANEL, ACENTO))
    p.append(texto(696, 498, "El árbol de procesos, con el contenedor ya corriendo", ACENTO, 14.5, anclaje="start", peso="600"))
    p.append(teclado(696, 524, "systemd", TEXTO, 13, anclaje="start", peso="normal"))
    p.append(teclado(712, 544, "└─ containerd-shim-runc-v2", TEXTO, 13, anclaje="start", peso="normal"))
    p.append(teclado(744, 564, "└─ sleep 300", ACENTO, 13, anclaje="start", peso="normal"))
    p.append(texto(696, 588, "ni dockerd ni containerd aparecen — y runc tampoco: ya salió", SUAVE, 12, anclaje="start"))

    p.append(texto(50, 646, "el orden real, dentro de runc:", SUAVE, 13, anclaje="start"))
    for cx, etiqueta in ((336, "1 · el proceso"), (556, "2 · el cgroup"),
                         (800, "3 · los namespaces")):
        p.append(chip(cx, 640, etiqueta, ACENTO, tam=13.5))
    p.append(flecha(426, 640, 471, 640, SUAVE))
    p.append(flecha(640, 640, 688, 640, SUAVE))
    p.append(texto(925, 636, "primero el PID, después el cgroup —", SUAVE, 12, anclaje="start"))
    p.append(texto(925, 654, "para que ningún hijo escape— y al final los namespaces", SUAVE, 12, anclaje="start"))

    p.append(texto(640, 706, "El camino de ejecución ya no pasa por Docker: cada syscall va directo al kernel. Lo que queda es un supervisor sosteniendo la salida y el código de salida.", SUAVE, 13.5))
    p.append(cierre())
    return "".join(p)


# --------------------------------------------------------------------------
# 1/5 · De uno a mil: escalamiento y orquestacion
# --------------------------------------------------------------------------

def cont_escalamiento():
    """Una copia funciona; cinco replicas con el estado adentro, no."""
    ancho, alto = 1220, 870
    aria = (
        "Dos escenarios. A la izquierda, una sola copia del servicio con su "
        "archivo de sesiones guardado adentro y funcionando. A la derecha, "
        "cinco replicas identicas de la misma imagen detras de un repartidor "
        "de carga, cada una con su propio archivo de sesiones marcado en rojo, "
        "y tres peticiones del mismo usuario que caen en replicas distintas y "
        "encuentran archivos distintos. Abajo, el mismo dibujo corregido: el "
        "estado sacado a una caja compartida fuera de los contenedores y el "
        "orquestador, que decide cuantas replicas hay y repone la que muere"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(610, 42, "De uno a mil: qué se rompe al escalar", TEXTO, 21, peso="600"))
    p.append(texto(610, 68, "el mismo servicio, una copia y cinco réplicas", SUAVE, 14))

    # Una copia.
    p.append(texto(60, 108, "una copia", ACENTO, 16, anclaje="start", peso="600"))
    p.append(caja(60, 150, 110, 60, PANEL, CIAN))
    p.append(texto(115, 176, "usuario", CIAN, 13))
    p.append(texto(115, 194, "una sesión", SUAVE, 11))
    p.append(flecha(176, 180, 246, 180, CIAN))
    p.append(caja(252, 130, 280, 150, PANEL, ACENTO))
    p.append(texto(392, 158, "el servicio", TEXTO, 14, peso="600"))
    p.append(texto(392, 178, "una sola copia", SUAVE, 11.5))
    p.append(caja(282, 196, 220, 60, TINTE, ACENTO, radio=8))
    p.append(teclado(392, 222, "sesiones.db", ACENTO, 14))
    p.append(texto(392, 244, "adentro del contenedor", SUAVE, 11))
    p.append(texto(296, 318, "Funciona. El usuario siempre vuelve", SUAVE, 13))
    p.append(texto(296, 338, "al mismo proceso y al mismo archivo.", SUAVE, 13))

    p.append(linea(570, 130, 570, 460, LINEA, 1.5, "6 6"))

    # Cinco replicas.
    p.append(texto(600, 108, "cinco réplicas de la misma imagen", ROJO, 16, anclaje="start", peso="600"))
    p.append(caja(600, 240, 100, 60, PANEL, CIAN))
    p.append(texto(650, 266, "el mismo", CIAN, 12.5))
    p.append(texto(650, 284, "usuario", CIAN, 12.5))
    p.append(flecha(706, 270, 724, 270, CIAN))
    p.append(caja(730, 140, 90, 310, PANEL, VIOLETA))
    p.append(texto(775, 286, "repartidor", VIOLETA, 12.5))
    p.append(texto(775, 304, "de carga", VIOLETA, 12.5))
    for i in range(5):
        y = 140 + i * 64
        golpeada = i in (0, 2, 4)
        color = ROJO if golpeada else LINEA
        p.append(caja(870, y, 310, 52, PANEL, color))
        p.append(texto(884, y + 22, f"réplica {i + 1}", TEXTO, 13, anclaje="start"))
        p.append(teclado(1166, y + 22, "sesiones.db", ROJO, 12, anclaje="end", peso="normal"))
        nota = "no te conoce: su archivo está vacío" if golpeada else "su propio archivo, con otra cosa adentro"
        p.append(texto(884, y + 40, nota, SUAVE, 10.5, anclaje="start"))
    for k, i in enumerate((0, 2, 4)):
        y = 140 + i * 64 + 26
        p.append(flecha(824, y, 864, y, CIAN))
        p.append(texto(844, y - 12, f"{k + 1}ª", CIAN, 11))
    p.append(texto(890, 494, "Cada petición cae en una réplica distinta y encuentra otro archivo.", SUAVE, 13))
    p.append(texto(890, 514, "La sesión se pierde: el estado adentro rompe el escalamiento.", ROJO, 13))

    p.append(linea(40, 548, 1180, 548, LINEA, 1.5, "6 6"))

    # El mismo dibujo, corregido.
    p.append(texto(610, 584, "lo mismo, corregido", ACENTO, 17, peso="600"))
    p.append(caja(40, 616, 230, 96, PANEL, VIOLETA))
    p.append(texto(155, 644, "el orquestador", VIOLETA, 14, peso="600"))
    p.append(texto(155, 666, "decide cuántas réplicas hay", SUAVE, 11.5))
    p.append(texto(155, 684, "y repone la que muere", SUAVE, 11.5))
    p.append(flecha_punteada(274, 656, 294, 656, VIOLETA))
    for i in range(5):
        x = 300 + i * 182
        p.append(caja(x, 616, 152, 80, PANEL, ACENTO))
        p.append(texto(x + 76, 644, "réplica", TEXTO, 13))
        p.append(texto(x + 76, 666, "sin estado", ACENTO, 12, peso="600"))
        p.append(texto(x + 76, 686, "desechable", SUAVE, 10.5))
        p.append(flecha(x + 76, 700, 505 + i * 88, 720, CIAN, 1.4))
    p.append(caja(470, 724, 420, 66, PANEL, CIAN))
    p.append(texto(680, 752, "el estado, afuera", CIAN, 15, peso="600"))
    p.append(texto(680, 774, "una base o un caché de sesiones, compartido por las cinco", SUAVE, 12))

    p.append(texto(610, 826, "Sacar el estado afuera es lo que hace intercambiables a las réplicas: matar una deja de ser un problema.", SUAVE, 13.5))
    p.append(texto(610, 848, "Quién decide cuántas hay y repone la que muere es el orquestador. Kubernetes es el nombre, y en este curso queda como deuda.", SUAVE, 13.5))
    p.append(cierre())
    return "".join(p)


# --------------------------------------------------------------------------
# 1/6 · VM contra contenedor
# --------------------------------------------------------------------------

def cont_vm_vs_contenedor():
    """Dos pilas sobre el mismo hardware: donde ocurre el aislamiento."""
    ancho, alto = 1180, 820
    aria = (
        "Dos pilas lado a lado sobre el mismo hardware y el mismo kernel del "
        "host. A la izquierda, el hipervisor y tres maquinas virtuales, cada "
        "una con su kernel invitado y su sistema operativo completo; a la "
        "derecha, tres contenedores que comparten el kernel del host y solo "
        "llevan su rootfs y su proceso. La frontera del aislamiento va "
        "resaltada en cada pila y una franja al pie compara arranque, tamano "
        "en disco y que le pasa a cada pila con un bug del kernel"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(590, 42, "Máquina virtual contra contenedor", TEXTO, 21, peso="600"))
    p.append(texto(590, 68, "dónde ocurre el aislamiento", SUAVE, 14))
    p.append(texto(310, 104, "tres máquinas virtuales", AMBAR, 17, peso="600"))
    p.append(texto(870, 104, "tres contenedores", ACENTO, 17, peso="600"))

    for i in range(3):
        x = 60 + i * 172
        p.append(caja(x, 140, 156, 270, PANEL, AMBAR))
        p.append(texto(x + 78, 164, "VM", AMBAR, 13, peso="600"))
        p.append(caja(x + 12, 176, 132, 46, FONDO, ACENTO, radio=6, grosor=1.5))
        p.append(texto(x + 78, 204, "tu proceso", ACENTO, 12.5))
        p.append(caja(x + 12, 230, 132, 92, FONDO, SUAVE, radio=6, grosor=1.5))
        p.append(texto(x + 78, 258, "sistema operativo", SUAVE, 11.5))
        p.append(texto(x + 78, 276, "completo", SUAVE, 11.5))
        p.append(texto(x + 78, 300, "init, libs, paquetes", SUAVE, 10.5))
        p.append(caja(x + 12, 330, 132, 66, FONDO, AMBAR, radio=6, grosor=1.5))
        p.append(texto(x + 78, 358, "kernel", AMBAR, 12.5, peso="600"))
        p.append(texto(x + 78, 378, "invitado", AMBAR, 12.5))

    p.append(caja(60, 428, 500, 66, TINTE, AMBAR, grosor=3.5))
    p.append(texto(310, 456, "hipervisor (KVM, QEMU, Hyper-V)", AMBAR, 15, peso="600"))
    p.append(texto(310, 478, "la frontera del aislamiento está aquí", AMBAR, 12.5))

    p.append(caja_punteada(620, 150, 500, 156, SUAVE))
    p.append(texto(870, 186, "lo que el contenedor NO lleva", SUAVE, 15, peso="600"))
    p.append(texto(870, 216, "· ningún kernel invitado", SUAVE, 13))
    p.append(texto(870, 240, "· ningún sistema operativo completo", SUAVE, 13))
    p.append(texto(870, 264, "· ningún hipervisor", SUAVE, 13))
    p.append(texto(870, 292, "por eso arranca en milisegundos y pesa megabytes", SUAVE, 12))

    for i in range(3):
        x = 620 + i * 172
        p.append(caja(x, 330, 156, 164, PANEL, ACENTO))
        p.append(texto(x + 78, 354, "contenedor", ACENTO, 13, peso="600"))
        p.append(caja(x + 12, 366, 132, 54, FONDO, ACENTO, radio=6, grosor=1.5))
        p.append(texto(x + 78, 398, "tu proceso", ACENTO, 12.5))
        p.append(caja(x + 12, 428, 132, 54, FONDO, SUAVE, radio=6, grosor=1.5))
        p.append(texto(x + 78, 450, "rootfs", SUAVE, 12.5))
        p.append(texto(x + 78, 468, "sólo lo que pediste", SUAVE, 10.5))

    p.append(caja(60, 508, 1060, 62, TINTE, ACENTO, grosor=3.5))
    p.append(texto(590, 534, "kernel del host (Linux) — uno solo", TEXTO, 16, peso="600"))
    p.append(texto(590, 558, "del lado del contenedor la frontera está aquí: es el mismo kernel para los tres", ACENTO, 12))

    p.append(caja(60, 584, 1060, 50, PANEL, LINEA))
    p.append(texto(590, 614, "hardware — CPU, memoria, disco, red", SUAVE, 15))

    p.append(caja(40, 656, 1100, 136, PANEL, LINEA))
    p.append(texto(360, 684, "máquina virtual", AMBAR, 13.5, anclaje="start", peso="600"))
    p.append(texto(760, 684, "contenedor", ACENTO, 13.5, anclaje="start", peso="600"))
    filas = (
        ("arranque", "decenas de segundos", "cientos de milisegundos"),
        ("tamaño en disco", "gigabytes", "decenas o cientos de MB"),
        ("un bug del kernel", "cae el invitado; el host sigue", "cae el kernel de todos: no hay un segundo kernel"),
    )
    for k, (criterio, vm, cont) in enumerate(filas):
        y = 716 + k * 28
        p.append(texto(70, y, criterio, TEXTO, 13, anclaje="start", peso="600"))
        p.append(texto(360, y, vm, SUAVE, 13, anclaje="start"))
        p.append(texto(760, y, cont, SUAVE, 13, anclaje="start"))
    p.append(cierre())
    return "".join(p)


# --------------------------------------------------------------------------
# 1/6 y 3/5 · El espectro no es una linea: son dos ejes
# --------------------------------------------------------------------------

def cont_espectro():
    """Donde aterriza la syscall, contra que privilegio tiene quien se escapa."""
    ancho, alto = 1200, 800
    aria = (
        "No es una linea, son dos ejes cruzados. El eje horizontal, donde "
        "aterriza la syscall que no controlas, ordena proceso suelto, "
        "contenedor, gVisor, Kata y VM completa. El eje vertical, que "
        "privilegio tiene quien se escapa, va de root en el host abajo a un "
        "usuario sin privilegios con su rango de subuid arriba. Contenedor "
        "rootful y rootless caen en la misma columna y se separan solo en el "
        "eje vertical; gVisor aparece dos veces, una a cada altura, porque "
        "tiene su propio modo rootless: los ejes se componen, no se ordenan"
    )
    columnas = (
        (386, "proceso suelto", SUAVE,
         ("la syscall va directo", "al kernel del host")),
        (558, "contenedor", ACENTO,
         ("la syscall va directo", "al kernel del host —", "el mismo kernel")),
        (730, "gVisor", CIAN,
         ("a un núcleo en espacio", "de usuario que reimplementa", "la interfaz de syscalls")),
        (902, "Kata", VIOLETA,
         ("a un segundo kernel real,", "dentro de una VM ligera")),
        (1074, "VM completa", AMBAR,
         ("a un kernel invitado,", "detrás del hipervisor")),
    )
    ARRIBA, ABAJO = 270, 480

    p = [marco(ancho, alto, aria)]
    p.append(texto(600, 42, "El aislamiento no es una línea: son dos ejes", TEXTO, 21, peso="600"))
    p.append(texto(600, 68, "y rootless sólo mueve uno de los dos", SUAVE, 14))

    p.append(flecha(300, 566, 300, 174, AMBAR))
    p.append(flecha(294, 560, 1166, 560, CIAN))
    for y in (ARRIBA, ABAJO):
        p.append(linea(300, y, 1160, y, LINEA, 1, "4 7"))

    p.append(texto(170, 126, "qué privilegio tiene", AMBAR, 14, peso="600"))
    p.append(texto(170, 146, "quien se escapa", AMBAR, 14, peso="600"))
    p.append(texto(730, 126, "Son dos preguntas independientes. Cada runtime ocupa una casilla de la rejilla:", SUAVE, 13))
    p.append(texto(730, 148, "una respuesta en el eje de abajo y otra en el de la izquierda.", SUAVE, 13))
    p.append(texto(288, 264, "un usuario sin privilegios,", SUAVE, 12.5, anclaje="end"))
    p.append(texto(288, 282, "con su rango de subuid", SUAVE, 12.5, anclaje="end"))
    p.append(texto(288, 484, "root en el host", SUAVE, 12.5, anclaje="end"))

    for cx, nombre, color, glosa in columnas:
        p.append(texto(cx, 592, nombre, color, 14, peso="600"))
        for k, renglon in enumerate(glosa):
            p.append(texto(cx, 614 + k * 16, renglon, SUAVE, 11))
    p.append(texto(730, 700, "dónde aterriza la syscall que no controlas   →", CIAN, 14, peso="600"))

    # Proceso suelto: no hay frontera que romper.
    p.append(circulo(386, ABAJO, 9, SUAVE))
    p.append(texto(386, 508, "nada que romper", SUAVE, 11.5))

    # El contenedor: misma columna, dos alturas.
    p.append(flecha(558, ABAJO - 18, 558, ARRIBA + 20, ACENTO, 2.5))
    p.append(texto(544, 374, "rootless", ACENTO, 12.5, anclaje="end", peso="600"))
    p.append(texto(544, 392, "sube sólo aquí", SUAVE, 11.5, anclaje="end"))
    p.append(circulo(558, ABAJO, 10, ROJO))
    p.append(texto(558, 508, "rootful", ROJO, 13, peso="600"))
    p.append(circulo(558, ARRIBA, 10, ACENTO))
    p.append(texto(558, 246, "rootless", ACENTO, 13, peso="600"))

    # gVisor, dos veces: tiene su propio modo rootless.
    p.append(linea(730, ABAJO - 18, 730, ARRIBA + 18, CIAN, 1.5, "5 6"))
    p.append(circulo(730, ABAJO, 10, CIAN))
    p.append(texto(730, 508, "gVisor", CIAN, 13, peso="600"))
    p.append(circulo(730, ARRIBA, 10, CIAN))
    p.append(texto(730, 246, "gVisor rootless", CIAN, 13, peso="600"))
    p.append(texto(746, 374, "su propio modo", CIAN, 11.5, anclaje="start"))
    p.append(texto(746, 390, "rootless", CIAN, 11.5, anclaje="start"))

    # Kata y VM: el eje horizontal los fija; el vertical no lo dice esta figura.
    for cx, nombre, color in ((902, "Kata", VIOLETA), (1074, "VM completa", AMBAR)):
        p.append(caja(cx - 30, 252, 60, 246, PANEL, color, radio=30, grosor=2.5))
        p.append(texto(cx, 232, nombre, color, 13, peso="600"))
        p.append(texto(cx, 520, "el eje vertical", SUAVE, 10.5))
        p.append(texto(cx, 534, "depende de cómo lo corras", SUAVE, 10.5))

    p.append(texto(600, 728, "Rootless no añade ninguna frontera: mismo kernel, misma superficie de syscalls. Mueve el eje vertical y no el horizontal.", SUAVE, 13.5))
    p.append(texto(600, 750, "Por eso gVisor tiene su propio modo rootless: los dos ejes se componen, no se ordenan.", SUAVE, 13.5))
    p.append(texto(600, 772, "Y rootless no sale gratis: habilitar user namespaces no privilegiados abre interfaces del kernel que normalmente están restringidas.", SUAVE, 13))
    p.append(cierre())
    return "".join(p)


# --------------------------------------------------------------------------
# 1/7 · Docker y Podman
# --------------------------------------------------------------------------

def cont_docker_vs_podman():
    """Con daemon y sin daemon, y el mito del 2x desarmado con los datos."""
    ancho, alto = 1260, 770
    aria = (
        "Las dos cadenas, una sobre otra. Arriba, docker CLI hablando por un "
        "socket con dockerd, marcado como proceso privilegiado siempre "
        "encendido, y de ahi containerd, el shim y runc. Abajo, podman, que "
        "hace fork-exec directo de conmon y de crun o runc y no deja nada "
        "permanente, con su caja de lo que si necesita rootless: rango en "
        "subuid y subgid y los binarios newuidmap y newgidmap. Un recuadro "
        "desarma el mito del doble de velocidad con tres barras medidas"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(630, 42, "Docker y Podman: la diferencia es arquitectónica", TEXTO, 21, peso="600"))
    p.append(texto(630, 68, "qué compra exactamente no tener daemon", SUAVE, 14))

    p.append(texto(50, 106, "Docker — con daemon", ROJO, 17, anclaje="start", peso="600"))
    p.append(teclado(209, 134, "/var/run/docker.sock", CIAN, 12.5, peso="normal"))
    docker = (
        (130, "docker", "lo que tecleas", CIAN),
        (150, "dockerd", "root · siempre encendido", ROJO),
        (165, "containerd", "imágenes y tareas", VIOLETA),
        (226, "containerd-shim-runc-v2", "supervisor", ACENTO),
        (120, "runc", "crea y se va", SUAVE),
    )
    x = 50
    for i, (w, nombre, papel, color) in enumerate(docker):
        if i:
            p.append(flecha(x - 54, 187, x - 6, 187, SUAVE))
        p.append(caja(x, 148, w, 78, PANEL, color))
        p.append(teclado(x + w / 2, 180, nombre, color, 13.5))
        p.append(texto(x + w / 2, 202, papel, SUAVE, 11))
        x += w + 58
    p.append(chip(313, 252, "proceso privilegiado", ROJO, tam=13))
    p.append(flecha(782, 228, 782, 246, ACENTO, 2))
    p.append(caja(669, 250, 226, 62, TINTE, ACENTO, radio=8))
    p.append(texto(782, 274, "el proceso del contenedor", TEXTO, 12.5))
    p.append(texto(782, 294, "cuelga del shim", ACENTO, 12))

    p.append(linea(40, 330, 1220, 330, LINEA, 1.5, "6 6"))

    p.append(texto(50, 366, "Podman — sin daemon, rootless", ACENTO, 17, anclaje="start", peso="600"))
    podman = ((50, 150, "podman", "tu propio proceso", ACENTO),
              (258, 165, "conmon", "supervisor, como el shim", ACENTO),
              (481, 200, "crun (o runc)", "crea y se va", SUAVE))
    for i, (px, w, nombre, papel, color) in enumerate(podman):
        if i:
            p.append(flecha(px - 54, 435, px - 6, 435, ACENTO))
            p.append(texto(px - 30, 382, "fork-exec", ACENTO, 11.5))
        p.append(caja(px, 396, w, 78, PANEL, color))
        p.append(teclado(px + w / 2, 428, nombre, color, 13.5))
        p.append(texto(px + w / 2, 450, papel, SUAVE, 11))
    p.append(chip(125, 502, "nada permanente", SUAVE, tam=13))
    p.append(flecha(340, 476, 340, 494, ACENTO, 2))
    p.append(caja(258, 498, 165, 62, TINTE, ACENTO, radio=8))
    p.append(texto(340, 522, "el proceso", TEXTO, 12.5))
    p.append(texto(340, 542, "cuelga de conmon", ACENTO, 11.5))

    p.append(caja(730, 380, 500, 175, PANEL, VIOLETA))
    p.append(texto(750, 410, "lo que rootless SÍ necesita", VIOLETA, 15, anclaje="start", peso="600"))
    p.append(texto(750, 440, "· un rango propio en /etc/subuid y /etc/subgid", SUAVE, 13, anclaje="start"))
    p.append(texto(750, 466, "· los binarios newuidmap y newgidmap", SUAVE, 13, anclaje="start"))
    p.append(texto(766, 490, "en Debian y Ubuntu vienen en el paquete uidmap,", SUAVE, 11.5, anclaje="start"))
    p.append(texto(766, 508, "que es Recommends y falta en instalaciones mínimas", SUAVE, 11.5, anclaje="start"))
    p.append(texto(750, 536, "sin eso:", SUAVE, 12, anclaje="start"))
    p.append(teclado(806, 536, "cannot find UID in /etc/subuid", ROJO, 12, anclaje="start", peso="normal"))

    p.append(caja(50, 580, 1180, 118, PANEL, AMBAR))
    p.append(texto(70, 608, "El mito del 2×, desarmado: fijando todo menos el runtime", AMBAR, 14.5, anclaje="start", peso="600"))
    barras = (("podman --runtime crun", 193, ACENTO),
              ("docker (runtime runc)", 330, CIAN),
              ("podman --runtime runc", 363, ROJO))
    for k, (etiqueta, ms, color) in enumerate(barras):
        y = 626 + k * 24
        p.append(teclado(70, y + 4, etiqueta, SUAVE, 12, anclaje="start", peso="normal"))
        p.append(relleno(310, y - 9, ms / 363 * 700, 17, color, radio=4))
        p.append(texto(320 + ms / 363 * 700, y + 4, f"{ms} ms", color, 12.5, anclaje="start", peso="600"))

    p.append(texto(630, 722, "Con el runtime igualado, Podman rootless sale ~10 % más lento que Docker. Lo que compra la ausencia de daemon no es velocidad:", SUAVE, 13.5))
    p.append(texto(630, 744, "es rootless, integración con systemd y ningún proceso privilegiado siempre encendido.", SUAVE, 13.5))
    p.append(cierre())
    return "".join(p)


# --------------------------------------------------------------------------
# 1/8 · Capas y cache
# --------------------------------------------------------------------------

def _pila_de_capas(y0, instrucciones, estados, hashes, paso=38):
    """Dockerfile a la izquierda, su pila de capas a la derecha."""
    p = []
    for i, instruccion in enumerate(instrucciones):
        y = y0 + i * paso
        tocada = estados[i][2]
        p.append(caja(58, y, 544, 32, FONDO, ROJO if tocada else "none",
                      radio=6, grosor=2 if tocada else 0))
        p.append(teclado(72, y + 21, instruccion, ROJO if tocada else TEXTO, 14,
                         anclaje="start", peso="normal"))
        if tocada:
            p.append(texto(596, y + 21, "← tocaste una línea", ROJO, 11.5,
                           anclaje="end"))
        p.append(flecha(616, y + 16, 684, y + 16, SUAVE, 1.5))
        etiqueta, color, _ = estados[i]
        p.append(caja(690, y, 440, 32, PANEL, color, radio=6, grosor=2))
        p.append(teclado(704, y + 21, hashes[i], SUAVE, 11.5, anclaje="start",
                         peso="normal"))
        p.append(texto(910, y + 21, f"capa {i + 1}", SUAVE, 11.5))
        p.append(texto(1116, y + 21, etiqueta, color, 12, anclaje="end",
                       peso="600"))
    return "".join(p)


def cont_capas_cache():
    """El cache es secuencial: una capa invalidada tumba las de abajo."""
    ancho, alto = 1300, 760
    aria = (
        "Un Dockerfile a la izquierda y su pila de capas a la derecha, cada "
        "capa con su hash truncado. Arriba, con COPY punto punto antes del RUN "
        "pip install, tocar una linea de codigo invalida esa capa y todas las "
        "de abajo, que caen en domino aunque su contenido no haya cambiado. "
        "Abajo, con COPY requirements.txt primero y el codigo despues, las "
        "capas de instalacion quedan rotuladas CACHED y solo se rehacen las "
        "dos ultimas"
    )
    CACHED = ("CACHED", ACENTO, False)
    INVAL = ("INVALIDADA", ROJO, False)
    TOCADA = ("INVALIDADA", ROJO, True)

    p = [marco(ancho, alto, aria)]
    p.append(texto(650, 42, "El caché de capas cae en dominó", TEXTO, 21, peso="600"))
    p.append(texto(650, 68, "el mismo cambio en una línea de código, con dos Dockerfiles", SUAVE, 14))

    p.append(texto(50, 104, "mal ordenado", ROJO, 16, anclaje="start", peso="600"))
    p.append(teclado(200, 104, "COPY . .  antes del  RUN pip install", SUAVE, 12.5, anclaje="start", peso="normal"))
    p.append(caja(50, 124, 560, 220, PANEL, LINEA))
    p.append(_pila_de_capas(
        144,
        ("FROM python:3.12-slim", "WORKDIR /app", "COPY . .",
         "RUN pip install -r requirements.txt", "CMD [\"python\", \"app.py\"]"),
        (CACHED, CACHED, TOCADA, INVAL, INVAL),
        ("sha256:6a2f…", "sha256:c81d…", "sha256:4be9…", "sha256:07ac…",
         "sha256:d5f1…"),
    ))
    p.append(flecha(1168, 236, 1168, 324, ROJO, 2.5))
    p.append(texto(1184, 262, "caen", ROJO, 12, anclaje="start", peso="600"))
    p.append(texto(1184, 280, "en dominó", ROJO, 12, anclaje="start", peso="600"))
    p.append(texto(1184, 302, "pip vuelve a", SUAVE, 10.5, anclaje="start"))
    p.append(texto(1184, 316, "correr entero,", SUAVE, 10.5, anclaje="start"))
    p.append(texto(1184, 330, "sin haber", SUAVE, 10.5, anclaje="start"))
    p.append(texto(1184, 344, "cambiado nada", SUAVE, 10.5, anclaje="start"))

    p.append(linea(40, 368, 1260, 368, LINEA, 1.5, "6 6"))

    p.append(texto(50, 400, "bien ordenado", ACENTO, 16, anclaje="start", peso="600"))
    p.append(teclado(200, 400, "COPY requirements.txt .  antes, y el código después", SUAVE, 12.5, anclaje="start", peso="normal"))
    p.append(texto(580, 400, "— reordenar parte el COPY en dos: una instrucción más", SUAVE, 12, anclaje="start"))
    p.append(caja(50, 420, 560, 258, PANEL, LINEA))
    p.append(_pila_de_capas(
        440,
        ("FROM python:3.12-slim", "WORKDIR /app", "COPY requirements.txt .",
         "RUN pip install -r requirements.txt", "COPY . .",
         "CMD [\"python\", \"app.py\"]"),
        (CACHED, CACHED, CACHED, CACHED, TOCADA, INVAL),
        ("sha256:6a2f…", "sha256:c81d…", "sha256:9d30…", "sha256:b17e…",
         "sha256:4be9…", "sha256:d5f1…"),
    ))
    p.append(texto(1184, 570, "pip no vuelve", ACENTO, 10.5, anclaje="start"))
    p.append(texto(1184, 584, "a correr", ACENTO, 10.5, anclaje="start"))
    p.append(flecha(1168, 596, 1168, 658, ROJO, 2.5))
    p.append(texto(1184, 614, "sólo estas", ROJO, 12, anclaje="start", peso="600"))
    p.append(texto(1184, 632, "dos se rehacen", ROJO, 12, anclaje="start", peso="600"))

    p.append(texto(650, 714, "El caché es secuencial: una capa sólo se reusa si TODAS las de arriba se reusaron. Por eso una capa invalidada tumba todo lo que sigue,", SUAVE, 13.5))
    p.append(texto(650, 738, "aunque su propio contenido no haya cambiado. La regla práctica: lo que cambia poco, arriba; lo que cambia en cada commit, hasta abajo.", SUAVE, 13.5))
    p.append(cierre())
    return "".join(p)


DIAGRAMAS_CONCEPTUALES = {
    "cont-intermodal": cont_intermodal,
    "cont-ns-cgroups": cont_ns_cgroups,
    "cont-tres-abstracciones": cont_tres_abstracciones,
    "cont-anatomia-run": cont_anatomia_run,
    "cont-escalamiento": cont_escalamiento,
    "cont-vm-vs-contenedor": cont_vm_vs_contenedor,
    "cont-espectro": cont_espectro,
    "cont-docker-vs-podman": cont_docker_vs_podman,
    "cont-capas-cache": cont_capas_cache,
}

# Las cuatro graficas de benchmark viven en su propio modulo porque dibujan un
# CSV y no una idea. El catalogo se fusiona aqui para que quien importe
# DIAGRAMAS vea todas las figuras de la unidad.
DIAGRAMAS = {**DIAGRAMAS_CONCEPTUALES, **DIAGRAMAS_BENCH}


def escribir(nombre):
    ASSETS.mkdir(parents=True, exist_ok=True)
    destino = ASSETS / f"{nombre}.svg"
    destino.write_text(DIAGRAMAS[nombre](), encoding="utf-8")
    return destino


def main(argv):
    nombres = argv[1:] or list(DIAGRAMAS)
    for nombre in nombres:
        if nombre not in DIAGRAMAS:
            raise SystemExit(f"diagrama desconocido: {nombre}")
        destino = escribir(nombre)
        print(f"{destino.name}  ({destino.stat().st_size / 1000:.1f} KB)")


if __name__ == "__main__":
    main(sys.argv)
