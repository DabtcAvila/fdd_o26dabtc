#!/usr/bin/env python3
"""Revision de contenido de las entregas: lo minimo que se puede comprobar.

`revisa_entrega.py` juzga la FORMA —donde viven los archivos, como se llama la
branch, que no haya basura—. Este script juzga el CONTENIDO MINIMO: que esten
los archivos que la tarea pidio, con su nombre exacto, y que no sean la
plantilla sin tocar.

No califica. Calificar es leer la bitacora y mirar la captura, y eso lo hace
una persona. Aqui solo se atrapa lo que un robot puede atrapar sin
equivocarse: el archivo que falta, el que quedo vacio, el que se subio con el
nombre cambiado y la plantilla que se entrego tal como venia.

Cada fallo dice QUE falta y QUE hacer. Un mensaje que solo dice "incorrecto"
obliga al estudiante a adivinar, y adivinar a las once de la noche del dia
que vence es como se abandona una materia.

El catalogo vive AQUI DENTRO, no en un archivo del repositorio, por la misma
razon que `TAREAS` vive en el workflow: bajo `pull_request_target` todo lo
que este script lee tiene que venir de la rama base o de la API. Si el
catalogo fuera un archivo que el pull request pudiera tocar, una entrega
podria reescribir su propio examen.

Una branch que no este en el catalogo no se revisa: las tareas de la unidad 7
nunca declararon nombre de branch, asi que no hay forma de saber que tarea es
y el script sale en verde sin decir nada.
"""
import json
import os
import re
import subprocess
import sys

# Extensiones que valen para una captura. El contrato dice png y acepta jpg;
# pdf tambien pasa porque varios lo entregaron asi en la unidad 7 y el
# contenido es el mismo. Lo que no se negocia es el resto del nombre.
EXT_CAPTURA = (".png", ".jpg", ".jpeg", ".pdf")
# Una captura de pantalla real no pesa 300 bytes. Este piso no distingue una
# buena de una mala; solo atrapa el archivo vacio y el placeholder.
MINIMO_CAPTURA = 5_000

CATALOGO = {
    "tarea-08-datacamp-intro": {
        "carpeta": "docker",
        "captura": "introduccion-a-docker",
        "seccion": "Introduction to Docker",
        "pide_url": True,
    },
    "tarea-08-datacamp-inter-1": {
        "carpeta": "docker",
        "captura": "intermedio-1-2",
        "seccion": "capítulos 1 y 2",
        # El curso no esta terminado todavia: no hay Statement of
        # Accomplishment que enlazar, asi que aqui solo se exige la fecha.
        "pide_url": False,
    },
    "tarea-08-datacamp-inter-2": {
        "carpeta": "docker",
        "captura": "intermedio-3-4",
        "seccion": "capítulos 3 y 4",
        "pide_url": True,
        # La ultima entrega cierra tambien la seccion de reflexion.
        "seccion_extra": "aprendiste",
    },
    "tarea-08-imagen": {
        "carpeta": "08_contenedores",
        "requeridos": ("bitacora.md", "mi-imagen.md", "info/info.sh",
                       "roto/Dockerfile"),
        "prohibidos": ("output.txt",),
    },
}


def _gh(*args):
    return subprocess.run(
        ["gh", "api", *args], capture_output=True, text=True, check=True
    ).stdout


def _pr_json(pr):
    repo = os.environ["GITHUB_REPOSITORY"]
    return json.loads(_gh(f"repos/{repo}/pulls/{pr}"))


def archivos_del_pr(pr):
    repo = os.environ["GITHUB_REPOSITORY"]
    salida = _gh(
        "--paginate", f"repos/{repo}/pulls/{pr}/files?per_page=100",
        "--jq", ".[] | {path: .filename, status: .status}",
    )
    return [json.loads(l) for l in salida.splitlines() if l.strip()]


def contenido(repo_head, sha, ruta):
    """Texto y tamaño de un archivo del pull request, leido por la API.

    Devuelve (texto_o_None, tamaño). El texto es None cuando el archivo es
    binario o no se pudo decodificar: una captura no se lee, solo se pesa.
    """
    import base64
    try:
        d = json.loads(_gh(f"repos/{repo_head}/contents/{ruta}?ref={sha}"))
    except subprocess.CalledProcessError:
        return None, 0
    tam = d.get("size", 0)
    if d.get("encoding") != "base64" or not d.get("content"):
        return None, tam
    crudo = base64.b64decode(d["content"])
    try:
        return crudo.decode("utf-8"), tam
    except UnicodeDecodeError:
        return None, tam


def cuerpo_de_seccion(texto, aguja):
    """El cuerpo de la seccion de `certificaciones.md` que menciona `aguja`.

    Se busca por subcadena y no por titulo exacto: la plantilla los escribe
    con acentos y con un separador que es facil de teclear distinto, y
    rechazar a alguien por un caracter de puntuacion seria ridiculo.
    """
    bloques = re.split(r"^##\s+", texto, flags=re.M)[1:]
    for b in bloques:
        titulo = b.split("\n", 1)[0]
        if aguja.lower() in titulo.lower():
            return b.split("\n", 1)[1] if "\n" in b else ""
    return None


def _tiene_fecha(cuerpo):
    return bool(re.search(r"\d{4}-\d{2}-\d{2}|\d{1,2}\s+de\s+\w+|\d{1,2}/\d{1,2}/\d{2,4}", cuerpo))


def _tiene_url(cuerpo):
    return bool(re.search(r"https?://\S{10,}", cuerpo))


def _sin_llenar(cuerpo):
    """La seccion sigue como vino: solo rotulos, enlaces de plantilla y vacio."""
    util = [
        l.strip() for l in cuerpo.splitlines()
        if l.strip() and not l.strip().startswith(("![", "<!--"))
    ]
    # Los rotulos de la plantilla terminan en dos puntos y no traen valor.
    return all(l.endswith(":") or l.startswith(("Se llena", "#")) for l in util)


def revisa_certificaciones(texto, tarea, base):
    fallos = []
    seccion = tarea["seccion"]
    cuerpo = cuerpo_de_seccion(texto, seccion)
    if cuerpo is None:
        return [
            f"CERTIFICACIONES: no encuentro la seccion de «{seccion}» en\n"
            f"  {base}/certificaciones.md\n"
            "  Ese archivo se copia de codigo/docker/ y no se escribe a mano:\n"
            "  si le borraste los titulos, vuelve a copiarlo y llena el tuyo."
        ]
    if _sin_llenar(cuerpo) or not cuerpo.strip():
        fallos.append(
            f"CERTIFICACIONES: la seccion de «{seccion}» esta vacia en\n"
            f"  {base}/certificaciones.md\n"
            "  Entregaste la plantilla tal como venia. Llena esa seccion."
        )
        return fallos
    if not _tiene_fecha(cuerpo):
        fallos.append(
            f"CERTIFICACIONES: a la seccion de «{seccion}» le falta la fecha\n"
            "  en que terminaste el curso. Escribela en cualquier formato\n"
            "  legible: 2026-09-22, 22/09/2026 o 22 de septiembre de 2026."
        )
    if tarea.get("pide_url") and not _tiene_url(cuerpo):
        fallos.append(
            f"CERTIFICACIONES: a la seccion de «{seccion}» le falta la URL del\n"
            "  Statement of Accomplishment. Es la que DataCamp te da al\n"
            "  terminar el curso, y es la que se verifica en un clic."
        )
    return fallos


def revisa_imagen(archivos_rel, leer, base):
    """Los tres defectos del Dockerfile que si se pueden comprobar solos."""
    fallos = []
    df = leer("roto/Dockerfile")
    if df:
        if re.search(r"^\s*FROM\s+\S+:latest\s*$", df, re.M | re.I):
            fallos.append(
                f"DOCKERFILE: {base}/roto/Dockerfile sigue con una base sin\n"
                "  pinear (`:latest`). Es uno de los tres defectos que la tarea\n"
                "  pide arreglar: fija una version concreta."
            )
        if not re.search(r"^\s*USER\s+\S+", df, re.M | re.I):
            fallos.append(
                f"DOCKERFILE: {base}/roto/Dockerfile no declara ningun `USER`,\n"
                "  asi que el proceso sigue corriendo como root. Es otro de los\n"
                "  tres defectos que la tarea pide arreglar."
            )
    sh = leer("info/info.sh")
    if sh and "Discooooooooooo" in sh:
        fallos.append(
            f"INFO.SH: {base}/info/info.sh todavia trae el `echo` de depuracion\n"
            "  que la tarea pide borrar (el de las muchas oes)."
        )
    return fallos


def main():
    rama = os.environ["RAMA"]
    tarea = CATALOGO.get(rama)
    if not tarea:
        print(f"La branch '{rama}' no esta en el catalogo de contenido: "
              "no hay nada que revisar aqui. OK.")
        return 0

    autor = os.environ["AUTOR"]
    mantenedores = {
        m.strip().lower()
        for m in os.environ.get("MANTENEDORES", "").split(",") if m.strip()
    }
    if autor.lower() in mantenedores:
        print(f"{autor} es mantenedor del curso: sin restricciones. OK.")
        return 0

    pr = os.environ["PR"]
    datos = _pr_json(pr)
    repo_head = datos["head"]["repo"]["full_name"]
    sha = datos["head"]["sha"]

    base = f"estudiantes/{autor}/{tarea['carpeta']}"
    vivos = [a["path"] for a in archivos_del_pr(pr) if a["status"] != "removed"]
    dentro = [p for p in vivos if p.startswith(base + "/")]
    rel = {p[len(base) + 1:] for p in dentro}

    if not dentro:
        print("La entrega no paso la revision de contenido.\n")
        print(f"- UBICACION: no toca ningun archivo dentro de {base}/\n"
              f"  Esa es la carpeta que le toca a la branch '{rama}'.\n")
        return 1

    cache = {}

    def leer(ruta_rel):
        if ruta_rel not in cache:
            cache[ruta_rel] = contenido(repo_head, sha, f"{base}/{ruta_rel}")
        return cache[ruta_rel][0]

    fallos = []

    for prohibido in tarea.get("prohibidos", ()):
        if prohibido in rel:
            fallos.append(
                f"SOBRA: {base}/{prohibido} no se sube.\n"
                "  La tarea lo dice explicitamente: ese archivo lo genera el\n"
                "  laboratorio en tu maquina y no viaja al repositorio."
            )

    if "seccion" in tarea:
        if "certificaciones.md" not in rel:
            fallos.append(
                f"FALTA: {base}/certificaciones.md\n"
                "  Es uno de los dos archivos de esta entrega. Se copia de\n"
                "  codigo/docker/ con el comando del ritual y se llena; no se\n"
                "  crea a mano."
            )
        else:
            texto = leer("certificaciones.md")
            if texto is None:
                fallos.append(
                    f"FALTA: no pude leer {base}/certificaciones.md como texto.\n"
                    "  Deberia ser un archivo Markdown."
                )
            else:
                fallos += revisa_certificaciones(texto, tarea, base)
                extra = tarea.get("seccion_extra")
                if extra:
                    cuerpo = cuerpo_de_seccion(texto, extra)
                    if cuerpo is None or _sin_llenar(cuerpo) or not cuerpo.strip():
                        fallos.append(
                            "CERTIFICACIONES: falta la ultima seccion, la de una\n"
                            "  cosa que aprendiste y no sabias. Son dos o tres\n"
                            "  lineas y se llenan en esta entrega, la ultima."
                        )

    if "captura" in tarea:
        nombre = tarea["captura"]
        halladas = [r for r in rel
                    if r.rsplit(".", 1)[0] == nombre and r.endswith(EXT_CAPTURA)]
        if not halladas:
            parecidas = [r for r in rel if r.endswith(EXT_CAPTURA)]
            pista = (f"\n  Encontre esto en su lugar: {', '.join(sorted(parecidas))}"
                     if parecidas else "")
            fallos.append(
                f"FALTA: la captura {base}/{nombre}.png\n"
                "  Ese nombre exacto importa porque la plantilla de\n"
                "  certificaciones.md ya lo enlaza: con otro nombre, la imagen\n"
                f"  sale rota. Si te quedo en jpg no pasa nada.{pista}"
            )
        else:
            _, tam = cache.setdefault(
                halladas[0], contenido(repo_head, sha, f"{base}/{halladas[0]}"))
            if tam and tam < MINIMO_CAPTURA:
                fallos.append(
                    f"CAPTURA: {base}/{halladas[0]} pesa {tam} bytes, que es\n"
                    "  demasiado poco para una captura de pantalla. Parece que\n"
                    "  se subio vacia o a medias. Vuelve a subirla."
                )

    for req in tarea.get("requeridos", ()):
        if req not in rel:
            fallos.append(
                f"FALTA: {base}/{req}\n"
                "  Es uno de los cuatro archivos que pide esta entrega."
            )

    if "requeridos" in tarea:
        fallos += revisa_imagen(rel, leer, base)

    if fallos:
        print("La entrega no paso la revision de contenido.\n")
        for f in fallos:
            print(f"- {f}\n")
        print(
            "Esto NO es la calificacion: es lo minimo que se revisa solo.\n"
            "Corrige y haz push a ESTA MISMA branch; el pull request se\n"
            "actualiza y la revision se vuelve a correr. No abras otro."
        )
        return 1

    print(f"Contenido correcto para '{rama}': "
          f"{len(dentro)} archivo(s) en {base}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
