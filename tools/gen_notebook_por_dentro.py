"""Genera codigo/09_python/por_dentro/por_dentro.ipynb.

Un titulo por cada Haz de las paginas 1, 2 y 4 de la seccion 9.2, y una celda
de codigo vacia debajo: el alumno pega el codigo de la pagina. El notebook
nunca se edita a mano (tools/test_python_por_dentro.py lo compara).
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "codigo/09_python/por_dentro/por_dentro.ipynb"

CELDAS = [
    ("1.0", "Una función en 30 segundos"),
    ("1.1", "precio_final"),
    ("1.2", "Con descuento"),
    ("1.3", "Con descuento 0"),
    ("1.4", "Un except que no hace nada"),
    ("1.5", "Qué Python corre (lectura)"),
    ("1.6", "dis (lectura)"),
    ("1.7", "suma con números y con textos (lectura)"),
    ("2.1", "= no copia"),
    ("2.2", "Copiar es explícito, y de un nivel"),
    ("2.3", "La función recibe el mismo objeto"),
    ("2.4", "El argumento por defecto mutable"),
    ("4.1", "Qué cuenta como falso"),
    ("4.2", "edad = 0"),
    ("4.3", "0.1 + 0.2"),
    ("4.4", "Decimal"),
    ("4.5", "Comprehension (lectura)"),
    ("4.6", "zip (lectura)"),
    ("4.7", "Encoding (lectura)"),
]


def _md(texto):
    return {"cell_type": "markdown", "metadata": {}, "source": [texto]}


def _codigo():
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": []}


def notebook():
    celdas = [_md("# Python por dentro\n\nPega en cada celda el código del "
                  "**Haz** con el mismo número en la página, y córrela "
                  "(Shift+Enter). Antes de entregar: *Clear All Outputs*.")]
    for numero, titulo in CELDAS:
        celdas += [_md(f"## {numero} · {titulo}"), _codigo()]
    nb = {"cells": celdas, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 4}
    return json.dumps(nb, ensure_ascii=False, indent=1) + "\n"


if __name__ == "__main__":
    DESTINO.write_text(notebook(), encoding="utf-8")
    print(f"escrito {DESTINO.relative_to(RAIZ)}")
    sys.exit(0)
