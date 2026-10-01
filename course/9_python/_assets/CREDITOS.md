# Créditos de materiales de la unidad

Procedencia, ruta y condición de uso de cada material del directorio.

Los SVG salen de `tools/gen_python.py`, que es su única fuente de verdad. No se
editan a mano, se regeneran. La guarda `tools/test_gen_python.py` falla si un
archivo del disco deja de coincidir con lo que produce el generador.

| Archivo | Descripción y prompt resumido | Autor / origen | Fecha | Licencia |
|---|---|---|---|---|
| py-mapa.svg | Ruta: `course/9_python/_assets/py-mapa.svg`. Qué produce qué en un proyecto uv: `pyproject.toml` → `uv lock` → `uv.lock` → `uv sync` → `.venv/` → `uv run`, con PyPI, `uv python install` y la franja de qué va a git y qué no. | Generado por `tools/gen_python.py`; obra propia | 2026-10-01 | Uso docente del curso |
| py-choque.svg | Ruta: `course/9_python/_assets/py-choque.svg`. Dos proyectos que piden versiones distintas de pandas: sin ambientes comparten un solo `site-packages/` y el último que instala gana; con un `.venv/` por proyecto cada uno guarda la suya. | Generado por `tools/gen_python.py`; obra propia | 2026-10-01 | Uso docente del curso |
| py-path.svg | Ruta: `course/9_python/_assets/py-path.svg`. Las carpetas del `PATH` en el orden en que la shell busca `python`, sin activar y después de `source .venv/bin/activate`. | Generado por `tools/gen_python.py`; obra propia | 2026-10-01 | Uso docente del curso |
| py-venv-arbol.svg | Ruta: `course/9_python/_assets/py-venv-arbol.svg`. El árbol de `.venv/` (`bin/python`, `bin/activate`, `site-packages/`, `pyvenv.cfg`) con qué es cada rama. | Generado por `tools/gen_python.py`; obra propia | 2026-10-01 | Uso docente del curso |
