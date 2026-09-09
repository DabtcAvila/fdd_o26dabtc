#!/usr/bin/env python3
"""Revision automatica de las entregas del curso.

Cuatro reglas, todas bloqueantes. El mensaje de cada fallo dice que archivo y
que hacer, porque el punto es que el estudiante se corrija solo en treinta
segundos y no que adivine.

Las cuentas listadas en MANTENEDORES quedan exentas: son quienes publican
material en la zona roja.

Corre bajo `pull_request_target`, asi que este script y su workflow salen
siempre de la rama base: un fork no puede reemplazarlos. A cambio, aqui NO se
lee ni se ejecuta nada del arbol de trabajo del pull request; todo lo que se
juzga viene de la API.
"""
import json
import os
import subprocess
import sys

# Nombres que son basura por si mismos, como ultimo componente de la ruta.
BASURA_EXACTA = (
    ".DS_Store", "Thumbs.db", "desktop.ini",
    "id_rsa", "id_dsa", "id_ecdsa", "credentials.json",
)
# Basura tanto si es carpeta intermedia como si es el ultimo componente.
BASURA_COMPONENTE = (
    "__pycache__", "node_modules", ".ipynb_checkpoints", ".venv", ".aws", ".ssh",
)
# Todo lo que empieza asi: .env, .env.local, .env.production, .envrc...
# En un repositorio publico, .env.local con una llave dentro es el caso grave,
# y es mas probable que un .env a secas.
BASURA_PREFIJOS = (".env",)
BASURA_SUFIJOS = (".pyc", ".pyo", ".class", ".o", ".pem")

RAIZ_ESTUDIANTES = "estudiantes/"
TOPE_LISTA = 20


def _gh(*args):
    return subprocess.run(
        ["gh", "api", *args], capture_output=True, text=True, check=True
    ).stdout


def archivos_del_pr(pr):
    """Ruta actual, ruta previa y estado de cada archivo del pull request.

    `previous_filename` es obligatorio: en un rename la API sólo pone la ruta
    destino en `filename`, asi que sin la previa un `git mv` saca archivos de la
    zona roja sin que nadie lo note.
    """
    repo = os.environ["GITHUB_REPOSITORY"]
    salida = _gh(
        "--paginate", f"repos/{repo}/pulls/{pr}/files?per_page=100",
        "--jq", ".[] | {path: .filename, previa: (.previous_filename // \"\"), "
                "status: .status}",
    )
    return [json.loads(l) for l in salida.splitlines() if l.strip()]


def total_declarado(pr):
    repo = os.environ["GITHUB_REPOSITORY"]
    return int(_gh(f"repos/{repo}/pulls/{pr}", "--jq", ".changed_files").strip())


def es_basura(ruta):
    partes = ruta.split("/")
    nombre = partes[-1]
    if nombre in BASURA_EXACTA or nombre.endswith(BASURA_SUFIJOS):
        return True
    if nombre.startswith(BASURA_PREFIJOS):
        return True
    return any(p in BASURA_COMPONENTE for p in partes)


def ruta_sospechosa(ruta):
    """Rutas que Git normalmente rechaza. Defensa en profundidad, no puerta."""
    return (
        ruta.startswith("/")
        or "\\" in ruta
        or ".." in ruta.split("/")
    )


def _lista(rutas):
    filas = "".join(f"    - {r}\n" for r in sorted(rutas)[:TOPE_LISTA])
    if len(rutas) > TOPE_LISTA:
        filas += f"    ... y {len(rutas) - TOPE_LISTA} mas.\n"
    return filas


def main():
    autor = os.environ["AUTOR"]
    rama = os.environ["RAMA"]
    rama_default = os.environ.get("RAMA_DEFAULT") or "main"
    mantenedores = {
        m.strip().lower()
        for m in os.environ.get("MANTENEDORES", "").split(",")
        if m.strip()
    }

    if autor.lower() in mantenedores:
        print(f"{autor} es mantenedor del curso: sin restricciones. OK.")
        return 0

    pr = os.environ["PR"]
    archivos = archivos_del_pr(pr)
    mio = f"{RAIZ_ESTUDIANTES}{autor}/"
    fallos = []

    # 0. Un pull request sin archivos no es una entrega.
    if not archivos:
        print(
            "Este pull request no cambia ningun archivo, asi que no hay nada\n"
            "que entregar. Commitea tu trabajo y haz push a esta misma branch."
        )
        return 1

    # La API corta en 3000 archivos. Si lo que bajamos no coincide con lo que
    # el pull request declara, no podemos afirmar que lo revisamos completo.
    declarado = total_declarado(pr)
    if declarado != len(archivos):
        print(
            f"No pude revisar la entrega completa: el pull request declara\n"
            f"{declarado} archivos y la API me devolvio {len(archivos)}.\n"
            "  Casi siempre significa que el pull request es enorme porque\n"
            "  arrastra cambios que no son tuyos. Ponte al dia con el bloque A\n"
            "  y vuelve a intentarlo, o partelo en entregas mas chicas."
        )
        return 1

    # 1. La branch. Va primero porque invalida la entrega entera.
    if rama == rama_default:
        fallos.append(
            f"BRANCH: este pull request sale de '{rama}', la rama default de tu\n"
            "  fork. Cada tarea se entrega desde su propia branch.\n"
            "  Arreglo: git switch -c tarea-NN-nombre, vuelve a commitear ahi,\n"
            "  haz push y abre otro pull request desde esa branch."
        )

    fuera, mal_nombre, basura, raras = [], [], [], []
    for a in archivos:
        estado = a["status"]
        # En un rename hay que juzgar las DOS rutas: de donde salio y a donde
        # llego. Si sólo se mira el destino, un git mv de la zona roja a la
        # propia carpeta pasa en verde y el merge borra el archivo del curso.
        rutas = [a["path"]] + ([a["previa"]] if a.get("previa") else [])

        for ruta in rutas:
            if ruta_sospechosa(ruta):
                raras.append(ruta)
                continue

            # 2. Ubicacion y 3. nombre de la carpeta.
            if not ruta.startswith(RAIZ_ESTUDIANTES):
                fuera.append(ruta)
            elif not ruta.startswith(mio):
                partes = ruta.split("/")
                duenio = partes[1] if len(partes) > 2 else ""
                if duenio and duenio.lower() == autor.lower():
                    mal_nombre.append((ruta, duenio))
                else:
                    fuera.append(ruta)

        # 4. Basura. Los borrados no cuentan: borrar un .DS_Store es lo correcto.
        if estado != "removed" and es_basura(a["path"]):
            basura.append(a["path"])

    if raras:
        fallos.append(
            "RUTA: hay rutas que no deberian existir en un commit.\n"
            + _lista(raras)
            + "  Arreglo: no uses rutas absolutas ni '..'. Trabaja desde la raiz\n"
            "  del repositorio con rutas que empiecen en estudiantes/."
        )

    if fuera:
        fallos.append(
            "UBICACION: tocaste archivos fuera de tu carpeta.\n"
            f"  Solo puedes escribir dentro de {mio}\n"
            + _lista(fuera)
            + "  Arreglo: git restore <archivo> para los de la zona roja, o mueve\n"
            "  tu trabajo a tu carpeta. Despues commit y push a esta misma branch.\n"
            "  Ojo: mover un archivo del curso a tu carpeta tambien cuenta, porque\n"
            "  lo borra de donde estaba."
        )

    if mal_nombre:
        malo = mal_nombre[0][1]
        fallos.append(
            "NOMBRE: tu carpeta no se llama exactamente como tu login.\n"
            f"  Esperaba: estudiantes/{autor}/\n"
            f"  Encontre: estudiantes/{malo}/\n"
            "  Las mayusculas cuentan. Se arregla en dos pasos, porque en macOS y\n"
            "  en Windows un rename que solo cambia mayusculas falla si se hace\n"
            "  de golpe:\n"
            f"    git mv estudiantes/{malo} estudiantes/_tmp_entrega\n"
            f"    git mv estudiantes/_tmp_entrega estudiantes/{autor}\n"
            "  Despues commit y push a esta misma branch."
        )

    if basura:
        fallos.append(
            "BASURA: agregaste archivos que nunca se suben.\n"
            + _lista(basura)
            + "  Arreglo: git rm --cached <archivo>, agregalo a .gitignore,\n"
            "  commit y push. Si es una credencial, cambiala: este repositorio\n"
            "  es publico y ya quedo en la historia."
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
