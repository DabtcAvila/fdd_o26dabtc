---
id: el-ritual-del-curso
title: "El ritual"
nav_title: "El ritual"
summary: "Los cuatro bloques del flujo, en orden y con sus comandos comentados: la tarjeta para copiar, qué hace cada línea, y por qué existe cada bloque."
status: ready
estimated_time: 25m
tags: [flujo, ritual, pull-request, branch, examen, disciplina]
prerequisites: [el-flujo-del-curso]
---

# El ritual

**GitHub · página 5 de 6** · 25 min

Meta: que esto salga sin pensar, siempre en el mismo orden.

## En corto

- **Cuatro bloques con nombre**, no quince comandos sueltos. Memoriza los bloques.
- El paso 0 es **una vez en el semestre**; los cuatro bloques, **en cada entrega**.
- Siempre en este orden, siempre desde la raíz del repositorio.
- Los dos `git status` del bloque C no son adorno.

## La tarjeta

Si no vas a leer nada más, lee esto.

```bash
# ═══ PASO 0 · UNA VEZ EN EL SEMESTRE ══════════════════
# Primero el fork, en el navegador:
#   github.com/raya-lucaria/fdd_o26

cd ~/fdd/fdd_o26                 # el paso 0 va aquí dentro
# ¿ya lo hice?  si imprime SALTA, brinca al bloque A
git remote -v | grep -q upstream && echo SALTA

GHUSER=$(gh api user --jq .login)     # tu login EXACTO
echo "$GHUSER"                        # NO lo teclees a mano
git remote rename origin upstream   # el curso: aquí BAJAS
git remote add origin \
  git@github.com:$GHUSER/fdd_o26_$GHUSER.git
git remote -v                    # 4 líneas, 2 nombres


# ═══ CADA VEZ QUE ENTREGAS ════════════════════════════
cd ~/fdd/fdd_o26                 # siempre desde la raíz
echo "$GHUSER"                   # tu login, del perfil


# ─── A · PONTE AL DÍA ──────────────────────────────────
git switch main                  # párate en main
git fetch upstream               # baja. NO toca tus archivos
git merge upstream/main          # mételo. Aquí SÍ cambian
git push origin main             # tu fork, al día


# ─── B · ABRE TU ESPACIO ───────────────────────────────
git switch -c tarea-07-git       # nace del main al día
mkdir -p estudiantes/$GHUSER/07_git   # tu mitad del espejo
cp -r codigo/07_git/. estudiantes/$GHUSER/07_git/
#   ... trabajas SÓLO dentro de estudiantes/$GHUSER/ ...


# ─── C · ENTREGA ───────────────────────────────────────
git status                       # ¿qué cambió? míralo
git add estudiantes/$GHUSER/07_git    # por ruta, nunca "."
git status                       # eso, y nada más
git commit -m "unidad 07: mi copia de trabajo"
git push -u origin tarea-07-git  # sube LA BRANCH al fork
#   → navegador: Compare & pull request
#     revisa las 4 casillas de arriba


# ─── D · CIERRA · ya te lo mergearon ───────────────────
git switch main
git fetch upstream && git merge upstream/main
git push origin main
git branch -d tarea-07-git       # se niega si falta mergear
git branch                       # sólo main. Listo
```

::: figure {#git-el-ritual title="Cuatro bloques, siempre en este orden"}
![Cuatro carriles verticales con el flujo completo: ponte al día sincroniza main con el repositorio del curso y actualiza el fork; abre tu espacio crea la branch de la tarea y copia el código a tu carpeta; entrega revisa el estado, agrega por ruta, commitea, sube la branch y abre el pull request; y cierra regresa a main, sincroniza y borra la branch](../_assets/git-el-ritual.svg)
:::

## La compuerta de arriba, explicada

La primera línea de la tarjeta no es parte del ritual: es la que te dice si el paso 0 ya está hecho y te lo puedes saltar.

```text
git remote -v | grep -q upstream && echo SALTA
    │         │      │  │           │
    │         │      │  │           └── si sí: imprime SALTA
    │         │      │  └────────────── la palabra buscada
    │         │      └───────────────── -q: sólo dime sí o no
    │         └──────────────────────── pasa la lista a grep
    └────────────────────────────────── lista tus remotes
```

En palabras: *lista mis remotes, busca en esa lista la palabra `upstream`, y si la encuentras imprime `SALTA`.* Si no imprime nada, te falta el paso 0.

## Qué hace cada bloque, y por qué existe

::: table {#git-ritual-resumen title="Los cuatro bloques"}

| Bloque | Termina cuando | Por qué existe |
|---|---|---|
| **A. Ponte al día** | Los tres `main` son idénticos: el del curso, el de tu fork y el tuyo | Una branch nacida de un `main` atrasado arrastra al PR archivos que no escribiste |
| **B. Abre tu espacio** | Estás en tu branch, con tu carpeta ya como espejo | La branch mantiene tu `main` limpio, que es lo que A necesita la próxima semana |
| **C. Entrega** | Pull request abierto y con la revisión en verde | Los dos `git status` son el hábito que separa una entrega limpia de una con basura |
| **D. Cierra** | `git branch` muestra sólo `main`, y estás ahí | Sin él, la próxima semana empiezas parado en la branch equivocada |

:::

## Cada comando, en una línea

La tabla de arriba dice qué hace cada **bloque**. Ésta dice qué hace cada **comando**, para que la tarjeta se entienda sin buscar nada.

::: table {#git-ritual-comandos title="Todos los comandos del ritual"}

| Comando | Qué hace | Se explica en |
|---|---|---|
| `git remote -v` | Lista los repositorios remotos que tu copia conoce, con el apodo y la URL de cada uno | [[el-fork|GitHub · 2]] |
| `git remote rename <viejo> <nuevo>` | Le cambia el apodo a un remote. No mueve nada, sólo lo renombra | [[el-fork|GitHub · 2]] |
| `git remote add <apodo> <url>` | Agrega un remote nuevo con ese apodo | [[el-fork|GitHub · 2]] |
| `gh api user --jq .login` | Le pregunta a GitHub cuál es tu login exacto | [[el-fork|GitHub · 2]] |
| `echo "$GHUSER"` | Imprime lo que guardaste en `$GHUSER`, para comprobar que no está vacío | [[el-fork|GitHub · 2]] |
| `git switch <branch>` | Te mueve a esa branch **y reescribe los archivos de tu carpeta** | [[branches-en-serio|GitHub · 3]] |
| `git switch -c <branch>` | La crea desde donde estás parado y te mueve a ella | [[branches-en-serio|GitHub · 3]] |
| `git branch` | Lista tus branches y marca en cuál estás | [[branches-en-serio|GitHub · 3]] |
| `git branch -d <branch>` | La borra, **sólo si ya está mergeada** | [[branches-en-serio|GitHub · 3]] |
| `git fetch upstream` | Baja los commits del curso y los deja aparte. **No toca tus archivos** | [[el-fork|GitHub · 2]] |
| `git merge upstream/main` | Junta lo que bajaste con la branch donde estás. Aquí sí cambian tus archivos | [[el-fork|GitHub · 2]] |
| `git merge main` | Lo mismo, pero trayendo tu `main` a tu branch. El rescate de una branch atrasada | [[branches-en-serio|GitHub · 3]] |
| `git push origin main` | Sube tu `main` a tu fork | [[el-fork|GitHub · 2]] |
| `git push -u origin <branch>` | Sube la branch por primera vez y **recuerda la pareja** | aquí abajo |
| `git push` | Después del `-u`, sube a donde ya quedó apuntada | aquí abajo |
| `mkdir -p <ruta>` | Crea la carpeta, y las de en medio, sin quejarse si ya existían | [[el-flujo-del-curso|GitHub · 4]] |
| `cp -r X/. Y/` | Copia **el contenido** de `X` dentro de `Y`. La barra y el punto no son adorno | [[el-flujo-del-curso|GitHub · 4]] |
| `git status` | Qué cambió, y en qué zona está cada cosa | [[tu-primer-repositorio|Git · 2]] |
| `git add <ruta>` | Aparta esa ruta para el próximo commit. Nunca `git add .` | [[lo-que-no-se-sube|Git · 4]] |
| `git commit -m "..."` | Guarda lo que apartaste, con su mensaje | [[tu-primer-repositorio|Git · 2]] |

:::

Tres detalles que valen la pena:

```text
git push -u origin tarea-07-git
         │    │        └── qué branch subes
         │    └─────────── a qué remote: origin, tu fork
         └──────────────── -u: recuerda la pareja.
                               Después basta "git push"
```

- **Los dos `git status` del bloque C.** El primero te dice qué hay antes de agregar; el segundo, qué vas a guardar exactamente. Míralos de verdad.
- **Si `git branch -d` se niega**, léelo: esa branch tiene commits que no están en ningún lado. Casi siempre significa que se te olvidó un `push`, no que haya que escalar a `-D`.
- **Si abriste terminal nueva, `$GHUSER` está vacía.** Compruébalo, o vas a crear `estudiantes//07_git`.

## El pull request: las cuatro casillas

Aquí es donde más gente se equivoca.

```text
  base repository:  raya-lucaria/fdd_o26   ← el del CURSO
  base:             main
  head repository:  tu-login/fdd_o26_tu-login
  compare:          tarea-07-git           ← no main
```

::: table {#git-pr-casillas title="La barra de selección del pull request"}

| Casilla | Debe decir |
|---|---|
| base repository | `raya-lucaria/fdd_o26` |
| base | `main` |
| head repository | `tu-login/fdd_o26_tu-login` |
| compare | `tarea-07-git` |

:::

El error clásico es dejar `base repository` en tu propio fork. El pull request se crea, se ve bien, y **no me llega**.

## El ensayo

Antes de la entrega de verdad, corre el flujo completo con una branch desechable. Tres minutos, y te ahorra el susto.

```bash
# A
git switch main && git fetch upstream
git merge upstream/main

# B
git switch -c ensayo
mkdir -p estudiantes/$GHUSER
touch estudiantes/$GHUSER/.gitkeep

# C
git status
git add estudiantes/$GHUSER/.gitkeep
git status
git commit -m "ensayo"
git push -u origin ensayo        # sube, pero NO abras PR

# D
git switch main
git branch -D ensayo             # bórrala aquí
git push origin --delete ensayo  # y también en tu fork
```

Si esto salió sin error, el de verdad va a salir.

> [!WARNING]
> **Los cuatro bloques se preguntan de memoria en el examen**: en orden, qué hace cada uno y con qué comandos. Todas las tareas de aquí a diciembre se entregan así, y una desviación del flujo cuenta como entrega no hecha. La forma de aprendérselo no es leerlo: es hacerlo hasta que salga solo.

::: problem {#git-p12-orden title="Se me olvidó el bloque A"}
Trabajaste toda la tarde. Hiciste la branch, copiaste el código, editaste, commiteaste y pusheaste. Al abrir el pull request, GitHub te muestra que tu rama toca **once archivos**, y sólo dos son tuyos: los otros nueve están en `course/` y son cambios que yo publiqué el martes.

¿Qué te saltaste, por qué produce ese resultado, y cómo lo arreglas sin perder tu trabajo?
:::

::: hint {of="git-p12-orden"}
Piensa desde qué punto de la historia nació tu branch, y qué había pasado en el repositorio del curso mientras tanto. Hay un comando en la página 3 que te lo dice.
:::

::: answer {of="git-p12-orden"}
Te saltaste el **bloque A**. Tu branch nació de un `main` atrasado, del último día que sincronizaste.

El pull request no compara tu branch contra el estado actual del curso, sino contra **el punto donde las dos historias se separaron**. Como tu `main` no tenía mis commits del martes, todo lo que publiqué después aparece como diferencia de tu rama. No los escribiste tú, pero desde fuera tu propuesta incluye "revertir esos nueve archivos". La revisión lo rechaza, y con razón: hay cambios fuera de tu carpeta.

Lo confirmas y lo arreglas así:

```bash
# si esto NO sale vacío, naciste atrasado
git log --oneline tarea-07-git..upstream/main

git switch main
git fetch upstream && git merge upstream/main
git push origin main
git switch tarea-07-git
git merge main     # trae mis commits a TU branch
git push           # el -u de antes hace que esto baste
```

El pull request se actualiza solo: ahora sólo muestra tus dos archivos. Si el merge da conflicto, se resuelve como en la página 3.

Por eso el bloque A va primero y no en medio. Hacerlo después funciona, pero cuesta más y da más miedo.
:::

> [!NOTE]
> **Si sólo recuerdas una cosa:** A, B, C, D. Ponte al día, abre tu espacio, entrega, cierra. Nunca en otro orden.

## Cierre

Ya tienes el flujo. Ahora hazlo de verdad: [[tu-primer-pull-request|Tu primer pull request]].
