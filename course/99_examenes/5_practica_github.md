---
id: practica-github
title: "Práctica de GitHub"
nav_title: "GitHub · práctica"
summary: "Ejercicios nuevos con la forma del examen de GitHub: tres árboles de commits para diagnosticar, siete errores reales de Git para leer, y un ritual con errores para corregir."
status: ready
estimated_time: 40m
tags: [practica, git, github, ritual, branches, errores, anexo]
prerequisites: [examen-github-enunciado]
---

# Práctica de GitHub

**Anexo · Exámenes** · ejercicios nuevos, parecidos al examen. La clave está en [[practica-github-solucion]].

**[Descargar el PDF](_assets/practica-github.pdf)** para resolverla en papel.

Contesta como en el examen: sin apuntes y sin computadora. Donde se pide «con tus palabras», no escribas comandos: se mide si entiendes qué pasa, no si recuerdas la sintaxis. En `<login>` imagina el tuyo.

## Ejercicio 1 · Lee el árbol

Cada árbol se lee de izquierda a derecha: a la izquierda los commits viejos, a la derecha los nuevos. Las letras son commits, y los nombres a la derecha son ramas.

### Árbol 1 · Trabajó en main

Ana no creó rama: hizo sus commits M1 y M2 directamente en `main`, los subió a su fork y abrió el pull request desde `main`.

```text
o---o---o                  upstream/main
         \
          M1---M2          main, origin/main   (pull request abierto desde main)
```

**a)** ¿Qué archivos muestra su pull request? Si todos están dentro de `estudiantes/ana/`, ¿por qué la revisión automática lo marca en rojo?

**b)** La semana siguiente el curso publica un commit P, y Ana hace el bloque A completo. Describe cómo queda su `main`. ¿Sigue siendo una copia del curso?

**c)** Después crea, desde ese `main`, la rama de la tarea siguiente. Si el primer pull request todavía no se ha mergeado, ¿qué arrastra el nuevo?

**d)** ¿Cómo lo arreglarías sin perder el trabajo de M1 y M2? Con tus palabras.

### Árbol 2 · Dos ramas hermanas

Beto hizo las cosas bien: actualizó `main` y desde ahí creó las dos ramas, una para cada tarea. El pull request de la 07 sigue abierto.

```text
          A---B            tarea-07-git              (pull request abierto)
         /
o---o---o                  main = upstream/main
         \
          D---E            tarea-08-datacamp-intro
```

**a)** ¿Qué archivos muestra el pull request de `tarea-08-datacamp-intro`?

**b)** Parado en `tarea-08-datacamp-intro`, Beto lista `estudiantes/beto/` y **no ve** la carpeta `07_git/`. ¿Perdió su tarea 07? Explica qué hizo `git switch` con esos archivos.

**c)** Se mergea la tarea 07. ¿Cambia lo que muestra el pull request de la 08?

**d)** Compáralo con la versión A del examen, donde la 08 nació de la 07: ¿por qué allá mergear la 07 sí cambiaba el pull request y aquí no?

### Árbol 3 · Editó el archivo del curso

Carla no copió la plantilla a su carpeta: editó directo `codigo/docker/certificaciones.md`, en su commit X. Mientras tanto el profesor corrigió ese mismo archivo, **en la misma línea**, en el commit R.

```text
o---o---R                  upstream/main   (R cambia la línea 3 de codigo/docker/certificaciones.md)
     \
      X                    tarea-08-datacamp-intro   (X cambia esa misma línea 3)
```

**a)** ¿Qué dice la revisión automática de su pull request, y por qué?

**b)** Si alguien intentara mergearlo, ¿Git lo mezcla solo o hay conflicto? ¿Por qué?

**c)** Si hubiera escrito en su copia, `estudiantes/carla/docker/certificaciones.md`, ¿habría conflicto con R?

**d)** ¿Qué regla del curso evita esto, y por qué funciona aunque treinta personas entreguen la misma tarea?

## Ejercicio 2 · Lee el error

Cada caso trae lo que la persona corrió y lo que Git le contestó, tal cual. Escribe **qué pasó** en una línea y **cuál es el siguiente paso**: un comando o una acción.

**1.** Acaba de crear su rama y hacer su primer commit.

```text
$ git push
fatal: The current branch tarea-09-uv-docker has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin tarea-09-uv-docker
```

**2.** El día anterior editó el README de su fork **desde la página de GitHub**. Hoy, en su máquina:

```text
$ git push origin main
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'github.com:ana/fdd_o26_ana.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally.
```

**3.** Primer push del semestre, en una máquina recién configurada: clonó el repositorio del curso y dejó el paso 0 para después.

```text
$ git push -u origin tarea-08-imagen
ERROR: Permission to raya-lucaria/fdd_o26.git denied to ana.
fatal: Could not read from remote repository.
```

**4.** Editó su `notas.md` en la rama de la tarea, no hizo commit, y quiere volver a `main` para ponerse al día.

```text
$ git switch main
error: Your local changes to the following files would be overwritten by checkout:
	estudiantes/ana/09_python/notas.md
Please commit your changes or stash them before you switch branches.
Aborting
```

**5.** Corrió `uv sync`, que creó `estudiantes/ana/09_python/uv_docker/.venv/` con cientos de archivos. Luego:

```text
$ git status --short
$
```

No sale nada. ¿Se perdió el ambiente? ¿Es un problema?

**6.** Apartó su carpeta y al revisar ve esto. Quiere sacar `.DS_Store` de lo que va a guardar **sin borrarlo** de su disco.

```text
$ git status
On branch tarea-09-uv-docker
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   estudiantes/ana/09_python/.DS_Store
	new file:   estudiantes/ana/09_python/uv_docker/pyproject.toml
```

**7.** Hizo commit y se dio cuenta de que le faltó un archivo y de que el mensaje está mal. **Todavía no hace push.** Quiere deshacer el commit pero conservar los cambios, para volver a hacerlo bien.

## Ejercicio 3 · Encuentra los errores

Dani escribió este ritual para entregar `tarea-09-uv-docker`, cuya carpeta es `09_python/`. Lo corrió completo y **ningún comando falló**, pero la entrega salió mal. Ya tenía hecho el paso 0.

```text
 1   git switch -c tarea-09-uv-docker
 2   git switch main
 3   git fetch upstream
 4   git merge upstream/main
 5   git push origin main
 6   mkdir -p estudiantes/$GHUSER/09_python
 7   cp -r codigo/09_python estudiantes/$GHUSER/09_python/
 8   git status
 9   git add .
10   git commit -m "tarea 9"
11   git push -u origin main
```

**a)** Hay **cinco** problemas: cuatro líneas mal y una que falta. Para cada uno, di el número de línea, qué se rompe y por qué.

**b)** Después de correr todo esto, ¿en qué rama quedaron sus commits? ¿Qué rama subió a su fork?

**c)** ¿Dónde quedaron los archivos de la plantilla? Escribe la ruta de `hola.py`, que en el curso está en `codigo/09_python/ambientes/hola.py`.

**d)** Escribe el ritual corregido, completo y en orden.

Cuando termines, califícate con [[practica-github-solucion]].
