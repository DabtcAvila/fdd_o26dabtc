#!/usr/bin/env python3
"""Revision automatica de las entregas del curso.

Seis reglas, todas bloqueantes. El mensaje de cada fallo dice que archivo y
que hacer, porque el punto es que el estudiante se corrija solo en treinta
segundos y no que adivine.

1. La branch: un pull request no puede salir de la rama default del fork.
2. Ubicacion: solo se puede escribir dentro de la carpeta propia.
3. Nombre de la carpeta: tiene que coincidir con el login exacto, mayusculas
   incluidas.
4. Basura: nada de archivos que nunca se suben (.env, __pycache__, llaves).
5. El nombre de la branch tiene que ser tarea-NN-nombre.
6. Una entrega, una carpeta: un pull request no puede tocar mas de una
   carpeta de entrega, ni una que no corresponda a su branch.

Las cuentas listadas en MANTENEDORES quedan exentas: son quienes publican
material en la zona roja.

Corre bajo `pull_request_target`, asi que este script y su workflow salen
siempre de la rama base: un fork no puede reemplazarlos. A cambio, aqui NO se
lee ni se ejecuta nada del arbol de trabajo del pull request; todo lo que se
juzga viene de la API.
"""
import datetime
import json
import os
import re
import subprocess
import sys

# Basura: si el nombre aparece como archivo o como carpeta de la ruta.
BASURA = (
    ".DS_Store", "Thumbs.db", "desktop.ini", "id_rsa",
    "__pycache__", "node_modules", ".ipynb_checkpoints", ".venv",
)
# Y todo lo que empieza con .env — .env.local con una llave dentro, en un
# repositorio publico, es mas probable que un .env a secas.
BASURA_PREFIJOS = (".env",)
BASURA_SUFIJOS = (".pyc", ".pyo", ".pem")

# Las branches de entrega se llaman tarea-NN-nombre. El nombre exacto de cada
# una esta escrito en su tarea; aqui solo se comprueba la forma y, si el mapa
# esta disponible, que la carpeta corresponda.
PATRON_RAMA = re.compile(r"^tarea-\d{2}-[a-z0-9-]+$")


def _mapa_tareas():
    """branch -> subcarpeta esperada, tal como lo declara el workflow."""
    mapa = {}
    for par in os.environ.get("TAREAS", "").split(","):
        par = par.strip()
        if "=" in par:
            rama, carpeta = par.split("=", 1)
            mapa[rama.strip()] = carpeta.strip().strip("/")
    return mapa


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
    return (
        nombre.endswith(BASURA_SUFIJOS)
        or nombre.startswith(BASURA_PREFIJOS)
        or any(p in BASURA for p in partes)
    )


def subcarpeta(ruta, mio):
    """La carpeta de la entrega dentro de la del estudiante.

    `estudiantes/ana/docker/certificaciones.md` -> `docker`.
    Un archivo suelto en `estudiantes/ana/` devuelve "" y no cuenta: el
    .gitkeep de la primera entrega no puede invalidar la segunda.
    """
    resto = ruta[len(mio):]
    partes = resto.split("/")
    return partes[0] if len(partes) > 1 else ""


def _estricto_en_branch():
    """La regla de la branch rechaza a partir de la fecha de corte."""
    desde = os.environ.get("BRANCH_ESTRICTA_DESDE", "").strip()
    if not desde:
        return True
    return datetime.date.today() >= datetime.date.fromisoformat(desde)


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
    mapa = _mapa_tareas()
    fallos, avisos = [], []

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
    #
    # Durante las primeras entregas esto solo avisa: el grupo ya tenia pull
    # requests abiertos desde main cuando la regla entro. A partir de la fecha
    # de corte rechaza. Para endurecerlo antes o despues, mueve
    # BRANCH_ESTRICTA_DESDE en entregas.yml; para hacerlo estricto ya, borra
    # esa variable.
    if rama == rama_default:
        texto = (
            f"BRANCH: este pull request sale de '{rama}', la branch default de\n"
            "  tu fork. Cada tarea se entrega desde su propia branch, porque\n"
            "  desde main solo puedes tener un pull request abierto a la vez.\n"
            "  Arreglo: git switch -c tarea-NN-nombre, vuelve a commitear ahi,\n"
            "  haz push y abre otro pull request desde esa branch."
        )
        if _estricto_en_branch():
            fallos.append(texto)
        else:
            avisos.append(
                texto + "\n"
                f"  POR AHORA ESTO SOLO ES UN AVISO. A partir del "
                f"{os.environ.get('BRANCH_ESTRICTA_DESDE')} rechaza la entrega."
            )

    # 5. El nombre de la branch. Se salta si el pull request sale de la rama
    # default, porque la regla 1 ya lo reporto y dos mensajes confunden.
    if rama != rama_default and not PATRON_RAMA.match(rama):
        nombres = ", ".join(sorted(mapa)) or "tarea-NN-nombre"
        fallos.append(
            f"BRANCH: '{rama}' no es el nombre de una entrega.\n"
            "  Cada tarea se entrega desde su propia branch, y el nombre exacto\n"
            "  esta escrito en la tarea. Los validos ahora mismo son:\n"
            f"    {nombres}\n"
            "  Arreglo: git switch -c <el nombre de tu tarea>, vuelve a\n"
            "  commitear ahi, haz push y abre el pull request desde esa branch."
        )

    fuera, mal_nombre, basura, mias = [], [], [], []
    for a in archivos:
        estado = a["status"]
        # En un rename hay que juzgar las DOS rutas: de donde salio y a donde
        # llego. Si sólo se mira el destino, un git mv de la zona roja a la
        # propia carpeta pasa en verde y el merge borra el archivo del curso.
        rutas = [a["path"]] + ([a["previa"]] if a.get("previa") else [])

        for ruta in rutas:
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
            else:
                mias.append(ruta)

        # 4. Basura. Los borrados no cuentan: borrar un .DS_Store es lo correcto.
        if estado != "removed" and es_basura(a["path"]):
            basura.append(a["path"])

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

    # 6. Una entrega, una carpeta. Cierra tres cosas de un golpe: dos entregas
    # metidas en el mismo pull request, el conflicto add/add cuando las dos
    # agregan el mismo archivo, y el alumno que llena el certificaciones.md de
    # la unidad pasada.
    carpetas = {subcarpeta(r, mio) for r in mias}
    carpetas.discard("")
    esperada = mapa.get(rama)
    if esperada and carpetas and carpetas != {esperada}:
        fallos.append(
            f"CARPETA: la branch '{rama}' entrega en {mio}{esperada}/\n"
            f"  y este pull request toca: {', '.join(sorted(carpetas))}\n"
            "  Cada entrega vive en una sola carpeta. Si juntaste dos tareas,\n"
            "  separalas: una branch y un pull request por cada una, las dos\n"
            "  nacidas de main y no una de la otra."
        )
    elif len(carpetas) > 1:
        fallos.append(
            "CARPETA: este pull request toca mas de una carpeta de entrega.\n"
            f"  Encontre: {', '.join(sorted(carpetas))}\n"
            "  Cada entrega vive en una sola carpeta. Separalas en dos branches\n"
            "  y dos pull requests, las dos nacidas de main."
        )

    for a in avisos:
        print(f"AVISO\n- {a}\n")

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
