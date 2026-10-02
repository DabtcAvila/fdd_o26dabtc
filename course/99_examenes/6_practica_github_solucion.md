---
id: practica-github-solucion
title: "Práctica de GitHub: clave"
nav_title: "GitHub · clave de práctica"
summary: "Las respuestas de la práctica de GitHub con una explicación corta de cada una: qué pasa, por qué, y qué otra respuesta también es correcta."
status: ready
estimated_time: 20m
tags: [practica, solucion, git, github, ritual, branches, errores, anexo]
prerequisites: [practica-github]
---

# Práctica de GitHub: clave

**Anexo · Exámenes** · los ejercicios están en [[practica-github]]. Resuélvelos antes de leer esto.

Casi todo sale de una sola idea: **un pull request muestra la diferencia entre tu rama y el punto donde se separó del `main` del curso**. Si una respuesta no te cuadra, vuelve a esa frase.

## Ejercicio 1 · Lee el árbol

### Árbol 1 · Trabajó en main

**a)** Muestra M1 y M2: sólo su carpeta. Los archivos están bien, pero el pull request sale **desde `main`**, y el curso lo rechaza porque la rama es parte de la entrega. Tu `main` tiene que ser una copia limpia del curso: es el punto de partida de todas tus tareas.

**b)** El merge del bloque A no puede avanzar en línea recta, porque `main` y `upstream/main` ya se separaron. Crea un **commit de merge** que une P con M2. Su `main` queda con todo lo del curso **más** M1 y M2. Ya no es una copia del curso, y no lo será mientras M1 y M2 no lleguen al curso.

**c)** Arrastra M1 y M2. La rama nueva nace de un `main` que los contiene, y el curso todavía no los tiene: es el mismo problema que la versión A del examen, sólo que aquí la herencia viene de `main`.

**d)** Primero se pone a salvo el trabajo y después se limpia `main`:

1. Parada en `main` (que apunta a M2), crea la rama de la tarea. La rama nace en M2 y se lleva M1 y M2.
2. Sube esa rama y abre el pull request **desde ella**. Cierra el que salía de `main`.
3. Regresa `main` a donde está `upstream/main`, para que vuelva a ser copia del curso.

**También vale:** para el paso 3, `git reset --hard upstream/main` parada en `main`. Mueve la rama, y `--hard` además pisa los archivos de tu disco, así que sólo es seguro después de que el trabajo ya vive en la otra rama. Otra salida válida: copiar sus archivos a una rama nueva nacida de un `main` sano.

**Repasa:** [[deshacer-en-git]] y [[el-ritual-del-curso]].

### Árbol 2 · Dos ramas hermanas

**a)** Sólo D y E: la carpeta `docker/`. La 08 se separó de `main` en el último `o`, y entre ese punto y E sólo está lo suyo.

**b)** No perdió nada. `git switch` pone en tu disco los archivos **de la rama a la que llegas**. `tarea-08-datacamp-intro` nunca tuvo `07_git/`, así que esa carpeta desaparece del disco al entrar, y reaparece al volver a `tarea-07-git`. La tarea 07 vive en su rama, en su fork y en su pull request.

**c)** No. La base de la 08 sigue siendo el último `o`, y entre ese punto y E siguen estando sólo D y E. Que `main` avance no le agrega nada a una rama que no carga commits ajenos.

**d)** En la versión A la rama de la 08 **cargaba** A, B y C, porque nació en C. Al mergear la 07 esos commits pasaban a ser parte de la base, y dejaban de aparecer. Aquí la 08 nunca cargó A y B, así que no hay nada que deje de aparecer.

**Repasa:** [[branches-en-serio]].

### Árbol 3 · Editó el archivo del curso

**a)** **Rojo.** El pull request toca un archivo fuera de `estudiantes/carla/`. La revisión lo bloquea para proteger lo que todos leen: si se mergeara, el cambio de Carla quedaría en la plantilla de todo el grupo.

**b)** **Conflicto.** Git compara las dos versiones contra el ancestro común. Si sólo una cambió una línea, se queda con esa sola. Aquí **las dos** cambiaron la línea 3 de distinta forma, y Git no tiene manera de saber cuál es la buena.

**c)** No. Serían dos archivos distintos, en dos rutas distintas. R toca uno y X el otro: Git los mezcla solo.

**d)** **La regla del espejo**: copia la plantilla a `estudiantes/<login>/` con la misma ruta, y trabaja sólo ahí. Cada quien escribe en una carpeta que nadie más toca, y nadie edita `codigo/`. Treinta pull requests no comparten ni una línea, así que ninguno choca con otro ni con las correcciones del curso.

**Repasa:** [[el-flujo-del-curso]] y [[branches-y-merge]].

## Ejercicio 2 · Lee el error

| # | Qué pasó | Siguiente paso |
|---|---|---|
| 1 | La rama existe en su máquina pero nunca se ha subido, y `git push` a secas no sabe a dónde mandarla. | `git push -u origin tarea-09-uv-docker`. Con el `-u`, los siguientes basta con `git push`. |
| 2 | Su fork tiene un commit (la edición del README en la web) que su máquina no tiene. Git no sube para no borrarlo. | Traer ese commit y mezclarlo: `git pull origin main`, o `git fetch origin` y `git merge origin/main`. Luego `git push origin main`. **Nunca** `--force`: borraría el commit de la web. |
| 3 | `origin` apunta al repositorio del curso, donde nadie del grupo puede escribir. Le faltó el paso 0. | `git remote -v` para confirmarlo, y terminar el paso 0: `git remote rename origin upstream` y `git remote add origin` con la URL de su fork. |
| 4 | Tiene un cambio sin guardar en un archivo que es distinto en `main`. Cambiar de rama lo pisaría, y Git se niega a perderlo. | `git commit` si el cambio ya está listo, o `git stash` y, de regreso en la rama, `git stash pop`. |
| 5 | Nada malo: el `.gitignore` del curso excluye `.venv/`, así que Git ni lo mira. El ambiente sigue en el disco. | Ninguno. Así debe ser: `.venv/` se recrea con `uv sync` y no se sube. |
| 6 | `.DS_Store` es basura de macOS y quedó apartada para el commit. | `git restore --staged estudiantes/ana/09_python/.DS_Store`. Sólo la saca del staging area; el archivo sigue en tu disco. |
| 7 | Hay un commit que no sirve, pero sólo existe en su máquina. | `git reset --soft HEAD~1`: deshace el commit y deja los cambios apartados, listos para agregar lo que faltaba y repetir el commit con el mensaje correcto. |

**Por qué el 7 sólo funciona antes del push:** reescribir un commit que ya subiste obliga a forzar el push, y eso borra historia en tu fork. Después del push, lo honesto es un commit nuevo que corrija.

**También vale:**

- En el 3, editar la URL con `git remote set-url origin …`.
- En el 6, `git rm --cached` sobre el archivo, que hace lo mismo.

Para que no vuelva a pasar, la ruta de esa basura va al `.gitignore`.

**Repasa:** [[deshacer-en-git]], [[lo-que-no-se-sube]] y la tabla de errores de [[cheatsheet-git]].

## Ejercicio 3 · Encuentra los errores

### a) Los cinco problemas

| Línea | Qué se rompe | Por qué |
|---|---|---|
| 1 | La rama nace de un `main` **sin actualizar**, y además la línea 2 la saca de ella: todo lo que sigue pasa en `main` | Crear la rama va **después** del bloque A (líneas 2 a 5). En ese orden nace de un `main` al día y te quedas parada en ella |
| 7 | La plantilla queda anidada: `09_python/09_python/…` | Sin el `/.` final, `cp -r` copia **la carpeta**, y como el destino ya existe (lo creó la línea 6) la mete adentro |
| 9 | Aparta **todo** lo que cambió en el repo, incluida basura como `.DS_Store` | El curso aparta por ruta: `git add estudiantes/$GHUSER/09_python` |
| falta, después del 9 | Nadie mira qué se va a guardar antes de guardarlo | El segundo `git status` es la última oportunidad de ver la basura o la carpeta anidada |
| 11 | Sube `main`, no la rama de la tarea | El pull request debe salir de `tarea-09-uv-docker`. Desde `main` la revisión lo rechaza, y su `main` deja de ser copia del curso |

### b) ¿En qué rama quedaron sus commits?

En `main`. La línea 2 la cambió a `main` y nunca volvió a la rama: `tarea-09-uv-docker` existe, pero vacía, atrasada y sin subir. A su fork subió `main` (línea 11), con su trabajo adentro: el árbol 1 de este mismo ejercicio.

### c) ¿Dónde quedó `hola.py`?

En `estudiantes/<login>/09_python/09_python/ambientes/hola.py`, con un `09_python` de más. Así no es espejo de `codigo/09_python/ambientes/hola.py`, y la revisión no encuentra los archivos donde los busca.

### d) El ritual corregido

```bash
git switch main
git fetch upstream
git merge upstream/main
git push origin main
git switch -c tarea-09-uv-docker
mkdir -p estudiantes/$GHUSER/09_python
cp -r codigo/09_python/. estudiantes/$GHUSER/09_python/
git status
git add estudiantes/$GHUSER/09_python
git status
git commit -m "unidad 09: labs y mi ambiente uv en Docker"
git push -u origin tarea-09-uv-docker
```

Y al final, el pull request en el navegador: base `raya-lucaria/fdd_o26` · `main`, compare `tarea-09-uv-docker`.

**También vale:** `git checkout -b` en lugar de `git switch -c`; `cp -r codigo/09_python/* …`; cualquier mensaje de commit razonable.

**Repasa:** [[el-ritual-del-curso]].
