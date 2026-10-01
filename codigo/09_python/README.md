# 09_python

Dos carpetas, con dos destinos distintos:

| Carpeta | Para qué | Se copia a |
|---|---|---|
| `ambientes/` | Los laboratorios de clase | `~/lab-ambientes/` — **fuera** del repo |
| `uv_docker/` | La entrega `tarea-09-uv-docker` | `estudiantes/$GHUSER/09_python/uv_docker/` |

## Los laboratorios: fuera del repo

Los labs crean `.venv/`, `pyproject.toml` y `uv.lock`. Fuera del repo nunca
acaban en un `git add`, y se pueden borrar sin miedo.

```bash
mkdir -p ~/lab-ambientes
cp -r ~/fdd/fdd_o26/codigo/09_python/ambientes/. ~/lab-ambientes/
cd ~/lab-ambientes && ls
```

Fíjate en la barra y el punto al final del origen: sin ellos, `cp` copia la
carpeta en vez de su contenido.

- `quien_soy.py` — dice qué Python corre y si estás en un ambiente. Sólo
  biblioteca estándar: corre en cualquier situación.
- `hola.py` — hola mundo con `rich`. Si `rich` no está, truena: así se nota.
- `script_autonomo.py` — un script con sus dependencias escritas dentro.
- `requirements.txt` — para el lab clásico de `venv` + `pip`.

## La entrega: uv_docker/

Ésta **sí** va en tu carpeta de estudiante, y sólo ella:

```bash
cd ~/fdd/fdd_o26
git switch main && git fetch upstream && git merge upstream/main
git switch -c tarea-09-uv-docker
mkdir -p estudiantes/$GHUSER/09_python/uv_docker
cp -r codigo/09_python/uv_docker/. estudiantes/$GHUSER/09_python/uv_docker/
#   ... trabajas ahí dentro y publicas tu imagen ...
git add estudiantes/$GHUSER/09_python/uv_docker
git status        # .venv/ NO debe aparecer
git commit -m "unidad 09: mi ambiente uv en Docker"
git push -u origin tarea-09-uv-docker
```

Lo que tiene cada archivo y los pasos, en el tablero:
https://rayalucaria.org/fdd_o26/python/ambientes/b-entregas/
