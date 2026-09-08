"""Guardas de la revision automatica de entregas.

El script vive en .github/scripts/ y decide si un pull request de estudiante se
acepta. Un falso positivo aqui bloquea a alguien que hizo todo bien, asi que
las cuatro reglas se prueban en las dos direcciones.
"""
import importlib.util
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
SCRIPT = RAIZ / ".github/scripts/revisa_entrega.py"
WORKFLOW = RAIZ / ".github/workflows/entregas.yml"


def _cargar():
    assert SCRIPT.is_file(), "falta .github/scripts/revisa_entrega.py"
    spec = importlib.util.spec_from_file_location("revisa_entrega", SCRIPT)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture(scope="module")
def mod():
    return _cargar()


def _correr(mod, monkeypatch, archivos, autor="ana", rama="tarea-07-git",
            mantenedores="uumami"):
    monkeypatch.setenv("AUTOR", autor)
    monkeypatch.setenv("RAMA", rama)
    monkeypatch.setenv("PR", "1")
    monkeypatch.setenv("MANTENEDORES", mantenedores)
    monkeypatch.setenv("GITHUB_REPOSITORY", "raya-lucaria/fdd_o26")
    monkeypatch.setattr(mod, "archivos_del_pr", lambda pr: archivos)
    return mod.main()


def _f(path, status="added"):
    return {"path": path, "status": status}


def test_entrega_correcta_pasa(mod, monkeypatch):
    archivos = [_f("estudiantes/ana/07_git/bitacora.md"),
                _f("estudiantes/ana/07_git/ejemplo.sh")]
    assert _correr(mod, monkeypatch, archivos) == 0


def test_tocar_la_zona_roja_falla(mod, monkeypatch):
    archivos = [_f("estudiantes/ana/07_git/bitacora.md"),
                _f("codigo/07_git/ejemplo.sh", "modified")]
    assert _correr(mod, monkeypatch, archivos) == 1


def test_tocar_la_carpeta_de_otro_falla(mod, monkeypatch):
    assert _correr(mod, monkeypatch, [_f("estudiantes/beto/07_git/a.md")]) == 1


def test_carpeta_con_mayusculas_distintas_falla(mod, monkeypatch):
    """Los logins de GitHub no distinguen mayusculas; las rutas si."""
    assert _correr(mod, monkeypatch, [_f("estudiantes/Ana/07_git/a.md")]) == 1


def test_basura_agregada_falla(mod, monkeypatch):
    for ruta in ("estudiantes/ana/07_git/.DS_Store",
                 "estudiantes/ana/07_git/__pycache__/x.pyc",
                 "estudiantes/ana/.env"):
        assert _correr(mod, monkeypatch, [_f(ruta)]) == 1, ruta


def test_borrar_basura_no_falla(mod, monkeypatch):
    """El falso positivo clasico: borrar un .DS_Store es la accion correcta."""
    archivos = [_f("estudiantes/ana/07_git/.DS_Store", "removed"),
                _f("estudiantes/ana/07_git/bitacora.md", "modified")]
    assert _correr(mod, monkeypatch, archivos) == 0


def test_pull_request_desde_main_falla(mod, monkeypatch):
    archivos = [_f("estudiantes/ana/07_git/bitacora.md")]
    assert _correr(mod, monkeypatch, archivos, rama="main") == 1


def test_el_mantenedor_queda_exento(mod, monkeypatch):
    archivos = [_f("course/7_git_y_github/2_github/1_github_en_corto.md", "modified"),
                _f("codigo/07_git/ejemplo.sh", "modified")]
    assert _correr(mod, monkeypatch, archivos, autor="uumami", rama="main") == 0


def test_un_archivo_llamado_env_no_es_dotenv(mod, monkeypatch):
    """`.env` es basura; `entorno.md` o `env.md` no lo son."""
    assert _correr(mod, monkeypatch, [_f("estudiantes/ana/07_git/env.md")]) == 0


def test_el_workflow_pasa_las_variables_que_el_script_lee(mod, monkeypatch):
    texto = WORKFLOW.read_text(encoding="utf-8")
    for clave in ("AUTOR", "RAMA", "PR", "MANTENEDORES", "GH_TOKEN"):
        assert f"{clave}:" in texto, f"el workflow no exporta {clave}"
    assert "pull_request:" in texto
    assert "revisa_entrega.py" in texto
