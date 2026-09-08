---
id: el-ritual-del-curso
title: "El ritual"
nav_title: "El ritual"
summary: "Los cuatro bloques del flujo, en orden y con sus comandos comentados: la tarjeta para copiar, qué hace cada línea, y por qué existe cada bloque."
status: ready
estimated_time: 20m
tags: [flujo, ritual, pull-request, branch, examen, disciplina]
prerequisites: [el-flujo-del-curso]
---

# El ritual

**GitHub · página 5 de 6** · 20 min

Meta: que esto salga sin pensar, siempre en el mismo orden.

## En corto

- **Cuatro bloques con nombre**, no quince comandos sueltos. Memoriza los bloques.
- El paso 0 es **una vez en el semestre**; los cuatro bloques, **en cada entrega**.
- Siempre en este orden, siempre desde la raíz del repositorio.
- Los dos `git status` del bloque C no son adorno.

## La tarjeta

Si no vas a leer nada más, lee esto.

```bash
# ══ PASO 0 · UNA VEZ EN EL SEMESTRE ══════════════════════════════════
#    ¿ya lo hice?  git remote -v | grep -q upstream && echo SALTA
#    Primero el fork, en el navegador: github.com/raya-lucaria/fdd_o26
U=$(gh api user --jq .login) && echo "$U"    # tu login EXACTO, no lo teclees
git remote rename origin upstream            # el del curso: de aquí BAJAS
git remote add origin git@github.com:$U/fdd_o26.git   # el tuyo: aquí SUBES
git remote -v                                # comprueba: 4 líneas, 2 nombres

# ══ CADA VEZ QUE ENTREGAS ════════════════════════════════════════════
cd ~/fdd/fdd_o26                             # siempre desde la raíz
echo "$U"                                    # si está vacía, redefínela

# A · PONTE AL DÍA ───────────────────────────────────────────────────
git switch main                              # párate en main
git fetch upstream                           # baja del curso, sin tocar tus archivos
git merge upstream/main                      # mételo. Aquí SÍ cambian
git push origin main                         # deja tu fork igual que el curso

# B · ABRE TU ESPACIO ────────────────────────────────────────────────
git switch -c tarea-07-git                   # branch nueva, desde el main al día
mkdir -p estudiantes/$U/07_git               # tu mitad del espejo
cp -r codigo/07_git/. estudiantes/$U/07_git/ # el "/." copia el CONTENIDO
#   ... trabajas SÓLO dentro de estudiantes/$U/ ...

# C · ENTREGA ────────────────────────────────────────────────────────
git status                                   # ¿qué cambió? míralo de verdad
git add estudiantes/$U/07_git                # por ruta. NUNCA "git add ."
git status                                   # ¿qué se guarda? eso y nada más
git commit -m "unidad 07: mi copia de trabajo"
git push -u origin tarea-07-git              # sube LA BRANCH a tu fork
#   → navegador: Compare & pull request. Revisa las 4 casillas

# D · CIERRA · cuando ya te lo mergearon ─────────────────────────────
git switch main
git fetch upstream && git merge upstream/main
git push origin main
git branch -d tarea-07-git                   # se niega si no está mergeada: te protege
git branch                                   # sólo main. Listo para la próxima
```

::: figure {#git-el-ritual title="Cuatro bloques, siempre en este orden"}
![Cuatro carriles verticales con el flujo completo: ponte al día sincroniza main con el repositorio del curso y actualiza el fork; abre tu espacio crea la branch de la tarea y copia el código a tu carpeta; entrega revisa el estado, agrega por ruta, commitea, sube la branch y abre el pull request; y cierra regresa a main, sincroniza y borra la branch](../_assets/git-el-ritual.svg)
:::

## Qué hace cada bloque, y por qué existe

::: table {#git-ritual-resumen title="Los cuatro bloques"}

| Bloque | Termina cuando | Por qué existe |
|---|---|---|
| **A. Ponte al día** | Los tres `main` son idénticos: el del curso, el de tu fork y el tuyo | Una branch nacida de un `main` atrasado arrastra al PR archivos que no escribiste |
| **B. Abre tu espacio** | Estás en tu branch, con tu carpeta ya como espejo | La branch mantiene tu `main` limpio, que es lo que A necesita la próxima semana |
| **C. Entrega** | Pull request abierto y con la revisión en verde | Los dos `git status` son el hábito que separa una entrega limpia de una con basura |
| **D. Cierra** | `git branch` muestra sólo `main`, y estás ahí | Sin él, la próxima semana empiezas parado en la branch equivocada |

:::

Tres detalles que valen la pena:

```text
git push -u origin tarea-07-git
         │    │        └── qué branch subes
         │    └─────────── a qué remote: origin, tu fork
         └──────────────── -u: recuerda la pareja. Después basta "git push"
```

- **Los dos `git status` del bloque C.** El primero te dice qué hay antes de agregar; el segundo, qué vas a guardar exactamente. Míralos de verdad.
- **Si `git branch -d` se niega**, léelo: esa branch tiene commits que no están en ningún lado. Casi siempre significa que se te olvidó un `push`, no que haya que escalar a `-D`.
- **Si abriste terminal nueva, `$U` está vacía.** Compruébalo, o vas a crear `estudiantes//07_git`.

## El pull request: las cuatro casillas

Aquí es donde más gente se equivoca.

```text
   base repository: raya-lucaria/fdd_o26  ←  base: main
                    ▲ el del CURSO, no el tuyo
   head repository: tu-login/fdd_o26      ←  compare: tarea-07-git
                                                      ▲ tu BRANCH, no main
```

::: table {#git-pr-casillas title="La barra de selección del pull request"}

| Casilla | Debe decir |
|---|---|
| base repository | `raya-lucaria/fdd_o26` |
| base | `main` |
| head repository | `tu-login/fdd_o26` |
| compare | `tarea-07-git` |

:::

El error clásico es dejar `base repository` en tu propio fork. El pull request se crea, se ve bien, y **no me llega**.

## El ensayo

Antes de la entrega de verdad, corre el flujo completo con una branch desechable. Tres minutos, y te ahorra el susto.

```bash
git switch main && git fetch upstream && git merge upstream/main   # bloque A
git switch -c ensayo                                               # bloque B
touch estudiantes/$U/.gitkeep
git status && git add estudiantes/$U/.gitkeep && git status        # bloque C
git commit -m "ensayo"
git push -u origin ensayo                                          # sube, pero NO abras PR
git switch main && git branch -D ensayo                            # bloque D, versión rápida
git push origin --delete ensayo                                    # bórrala también del fork
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
git log --oneline tarea-07-git..upstream/main   # si no sale vacío, naciste atrasado

git switch main
git fetch upstream && git merge upstream/main
git push origin main
git switch tarea-07-git
git merge main            # trae mis commits a TU branch
git push                  # el -u de antes hace que esto baste
```

El pull request se actualiza solo: ahora sólo muestra tus dos archivos. Si el merge da conflicto, se resuelve como en la página 3.

Por eso el bloque A va primero y no en medio. Hacerlo después funciona, pero cuesta más y da más miedo.
:::

> [!NOTE]
> **Si sólo recuerdas una cosa:** A, B, C, D. Ponte al día, abre tu espacio, entrega, cierra. Nunca en otro orden.

## Cierre

Ya tienes el flujo. Ahora hazlo de verdad: [[tu-primer-pull-request|Tu primer pull request]].
