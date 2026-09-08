#!/usr/bin/env python3
"""Revision automatica de las entregas del curso.

Cuatro reglas, todas bloqueantes. El mensaje de cada fallo dice que archivo y
que hacer, porque el punto es que el estudiante se corrija solo en treinta
segundos y no que adivine.

Las cuentas listadas en MANTENEDORES quedan exentas: son quienes publican
material en la zona roja.

Corre con el token de solo lectura de `pull_request`, asi que un fork no puede
influir en lo que este script decide.
"""
import json
import os
import subprocess
import sys

BASURA = (
    ".DS_Store", "Thumbs.db", "desktop.ini", ".env",
    "__pycache__/", "node_modules/", ".ipynb_checkpoints/", ".venv/",
)
BASURA_SUFIJOS = (".pyc", ".pyo", ".class", ".o")

RAIZ_ESTUDIANTES = "estudiantes/"


def archivos_del_pr(pr):
    """Ruta y estado de cada archivo del pull request, paginado."""
    salida = subprocess.run(
        ["gh", "api", "--paginate",
         f"repos/{os.environ['GITHUB_REPOSITORY']}/pulls/{pr}/files",
         "--jq", ".[] | {path: .filename, status: .status}"],
        capture_output=True, text=True, check=True,
    ).stdout
    return [json.loads(l) for l in salida.splitlines() if l.strip()]


def es_basura(ruta):
    if ruta.endswith(BASURA_SUFIJOS):
        return True
    partes = ruta.split("/")
    for patron in BASURA:
        nombre = patron.rstrip("/")
        if patron.endswith("/"):
            if nombre in partes[:-1]:
                return True
        elif partes[-1] == nombre:
            return True
    return False


def main():
    autor = os.environ["AUTOR"]
    rama = os.environ["RAMA"]
    mantenedores = {m.strip().lower() for m in os.environ.get("MANTENEDORES", "").split(",") if m.strip()}

    if autor.lower() in mantenedores:
        print(f"{autor} es mantenedor del curso: sin restricciones. OK.")
        return 0

    archivos = archivos_del_pr(os.environ["PR"])
    mio = f"{RAIZ_ESTUDIANTES}{autor}/"
    fallos = []

    # 1. La branch. Va primero porque invalida la entrega entera.
    if rama == "main":
        fallos.append(
            "BRANCH: este pull request sale de tu main.\n"
            "  Cada tarea se entrega desde su propia branch.\n"
            f"  Arreglo: git switch main && git switch -c tarea-NN-nombre, vuelve a\n"
            "  commitear ahi, haz push y abre otro pull request desde esa branch."
        )

    fuera, mal_nombre, basura = [], [], []
    for a in archivos:
        ruta, estado = a["path"], a["status"]

        # 2. Ubicacion y 3. nombre de la carpeta.
        if not ruta.startswith(RAIZ_ESTUDIANTES):
            fuera.append(ruta)
        elif not ruta.startswith(mio):
            duenio = ruta.split("/")[1] if len(ruta.split("/")) > 1 else "?"
            if duenio.lower() == autor.lower():
                mal_nombre.append((ruta, duenio))
            else:
                fuera.append(ruta)

        # 4. Basura. Los borrados no cuentan: borrar un .DS_Store es lo correcto.
        if estado != "removed" and es_basura(ruta):
            basura.append(ruta)

    if fuera:
        fallos.append(
            "UBICACION: tocaste archivos fuera de tu carpeta.\n"
            f"  Solo puedes escribir dentro de {mio}\n"
            + "".join(f"    - {r}\n" for r in sorted(fuera)[:20])
            + "  Arreglo: git restore <archivo> para los de la zona roja, o mueve tu\n"
            "  trabajo a tu carpeta con git mv. Despues commit y push a esta misma branch."
        )

    if mal_nombre:
        malo = mal_nombre[0][1]
        fallos.append(
            "NOMBRE: tu carpeta no se llama exactamente como tu login.\n"
            f"  Esperaba: estudiantes/{autor}/\n"
            f"  Encontre: estudiantes/{malo}/\n"
            "  Las mayusculas cuentan. Arreglo, desde la raiz del repositorio:\n"
            f"    U=$(gh api user --jq .login)\n"
            f"    git mv estudiantes/{malo} estudiantes/$U\n"
            "  Despues commit y push a esta misma branch."
        )

    if basura:
        fallos.append(
            "BASURA: agregaste archivos que nunca se suben.\n"
            + "".join(f"    - {r}\n" for r in sorted(basura)[:20])
            + "  Arreglo: git rm --cached <archivo>, agregalo a .gitignore, commit y push."
        )

    if fallos:
        print("La entrega no paso la revision.\n")
        for f in fallos:
            print(f"- {f}\n")
        print(
            "Corrige y haz push a ESTA MISMA branch: el pull request se actualiza\n"
            "solo y la revision se vuelve a correr. No abras otro."
        )
        return 1

    print(f"Entrega correcta: {len(archivos)} archivo(s), todos dentro de {mio}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
