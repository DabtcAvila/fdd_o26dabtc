# 09_python

Todo se trabaja en **tu carpeta de estudiante**, como el resto del curso.
Esta carpeta se copia completa, respetando el mirror:

| Carpeta | Para qué | En tu carpeta |
|---|---|---|
| `ambientes/` | Los laboratorios de clase | `estudiantes/$GHUSER/09_python/ambientes/` |
| `uv_docker/` | La entrega `tarea-09-uv-docker` | `estudiantes/$GHUSER/09_python/uv_docker/` |

Los labs y la entrega viajan **juntos**, en el pull request de
`tarea-09-uv-docker`: los dos viven en `09_python/`.

## El ritual, una sola vez

Abre tu fork en VS Code y, en su terminal:

```bash
cd {tu_fork_de_la_clase}     # la carpeta donde clonaste tu fork, sin llaves
git switch main && git fetch upstream && git merge upstream/main
git switch -c tarea-09-uv-docker
mkdir -p estudiantes/$GHUSER/09_python
cp -r codigo/09_python/. estudiantes/$GHUSER/09_python/
cd estudiantes/$GHUSER/09_python && ls
```

Fíjate en la barra y el punto al final del origen: sin ellos, `cp` copia la
carpeta en vez de su contenido.

Los labs crean `.venv/` dentro de tu carpeta. No pasa nada: el `.gitignore`
del curso lo deja fuera de git, y lo que sí se sube (`pyproject.toml`,
`uv.lock`, tu código) es justo lo que debe quedar.

## Lo que hay en ambientes/

- `quien_soy.py` — dice qué Python corre y si estás en un ambiente. Sólo
  biblioteca estándar: corre en cualquier situación.
- `hola.py` — hola mundo con `rich`. Si `rich` no está, truena: así se nota.
- `script_autonomo.py` — un script con sus dependencias escritas dentro.
- `requirements.txt` — para el lab clásico de `venv` + `pip`.

## La entrega: uv_docker/

Cuando termines los labs y la entrega, desde la raíz del repo:

```bash
cd {tu_fork_de_la_clase}     # la carpeta donde clonaste tu fork, sin llaves
git add estudiantes/$GHUSER/09_python
git status        # .venv/ NO debe aparecer
git commit -m "unidad 09: labs de ambientes y mi ambiente uv en Docker"
git push -u origin tarea-09-uv-docker
```

Lo que tiene cada archivo y los pasos, en el tablero:
https://rayalucaria.org/fdd_o26/python/ambientes/b-entregas/
