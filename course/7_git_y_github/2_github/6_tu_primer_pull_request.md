---
id: tu-primer-pull-request
title: "Tu primer pull request"
nav_title: "Tu primer PR"
summary: "La entrega de verdad, guiada de principio a fin: tu carpeta, el espejo, la bitácora, el pull request contra el repositorio del curso, y qué hacer si la revisión sale roja."
status: ready
estimated_time: 15m
tags: [github, pull-request, entrega, branch, mirror, flujo]
prerequisites: [el-ritual-del-curso]
---

# Tu primer pull request

**GitHub · página 6 de 6** · 15 min

Meta: terminar la unidad con un pull request abierto y en verde.

## En corto

- Esto no es lectura: es **la entrega** de la unidad, hecha paso a paso.
- No hay contenido difícil. Todo el peso está en que el flujo salga exacto.
- **Entregado** = pull request abierto antes de la fecha, con la revisión en verde.
- A partir de hoy **no hay Canvas**: todo el curso se entrega por GitHub.

## Todo, en un bloque

```bash
cd ~/fdd/fdd_o26
echo "$U" || U=$(gh api user --jq .login)
git remote -v | grep -q upstream || echo "te falta el paso 0"

# ─── A · PONTE AL DÍA
git switch main
git fetch upstream && git merge upstream/main
git push origin main

# ─── B · ABRE TU ESPACIO
git switch -c tarea-07-git
mkdir -p estudiantes/$U/07_git
cp -r codigo/07_git/. estudiantes/$U/07_git/
ls -R estudiantes/$U/07_git

#   ... llena la bitácora y corre el script (abajo) ...

# ─── C · ENTREGA
git status
git add estudiantes/$U/07_git
git status
git commit -m "unidad 07: mi carpeta y mi bitacora"
git push -u origin tarea-07-git
#   → navegador: Compare & pull request
```

Después del `ls -R` **deberías ver** exactamente esto, con tu login:

```text
estudiantes/tu-login/07_git/
├── bitacora.md
└── ejemplo.sh
```

Si ves `07_git/07_git/`, se te fue el `/.`:

```bash
rm -rf estudiantes/$U/07_git && mkdir -p estudiantes/$U/07_git
cp -r codigo/07_git/. estudiantes/$U/07_git/
```

## Qué hay que llenar

Abre **tu copia** —`estudiantes/$U/07_git/bitacora.md`, nunca la de `codigo/`—:

1. Tu nombre y tu usuario de GitHub.
2. La salida literal de `git remote -v` y de `git log --oneline -3`.
3. Tres o cuatro líneas sobre **algo que se te haya roto** en la unidad y cómo lo resolviste. Si de verdad no se rompió nada, dilo y explica qué te costó más entender.

Y corre el script que copiaste, para que la carpeta no sea sólo texto:

```bash
bash estudiantes/$U/07_git/ejemplo.sh tu-nombre
```

> [!NOTE]
> Reportar el pendiente cuenta. Presumir un avance que no ocurrió, no. La bitácora es para que yo sepa dónde se atoró el grupo.

> [!WARNING]
> Mira el segundo `git status` de verdad. Si aparece **cualquier** ruta que no empiece con `estudiantes/`, te van a rechazar. Sácala con `git restore --staged <archivo>` antes de commitear.

## El pull request

Entra a tu fork en GitHub. Aparece una barra amarilla con **Compare & pull request**; si no, pestaña *Pull requests* → *New pull request* → *compare across forks*.

```text
  base repository:  raya-lucaria/fdd_o26   ← el del CURSO
  base:             main
  head repository:  tu-login/fdd_o26       ← el TUYO
  compare:          tarea-07-git           ← no main
```

Título: `unidad 07 · tu-login`. Créalo, y **espera a que la revisión quede en verde**.

> [!NOTE]
> **La primera vez, la revisión no arranca sola.** GitHub me pide autorizar el primer pull request de cada persona antes de correr nada. Si el tuyo dice *waiting for approval*, o simplemente no aparece ningún check, **no hiciste nada mal**: está esperándome a mí. De tu segunda entrega en adelante corre sola y al instante.

::: table {#git-entrega-checklist title="Si la revisión sale roja"}

| Dice | Qué pasó | Qué haces |
|---|---|---|
| Archivo fuera de tu carpeta | Tocaste la zona roja | `git restore codigo/`, commit, push |
| El nombre no coincide | Tu carpeta no se llama como tu login | `git mv estudiantes/<malo> estudiantes/$U` |
| Basura detectada | Se coló un `.DS_Store` o un `__pycache__/` | `git rm --cached <archivo>`, commit, push |
| El PR viene de `main` | Se te olvidó la branch | Crea la branch, muévete y abre otro PR |

:::

```bash
git add <lo que corregiste>
git commit -m "corrijo lo que marcó la revisión"
git push     # a la MISMA branch: el PR se actualiza solo
```

**No abras otro pull request.**

## Y cuando te lo mergee

```bash
# ─── D · CIERRA
git switch main
git fetch upstream && git merge upstream/main
git push origin main
git branch -d tarea-07-git
git branch          # sólo main. Listo para la tarea 8
```

## Qué cuenta como entregado

::: table {#git-entregado title="El criterio, sin ambigüedad"}

| Sí cuenta | No cuenta |
|---|---|
| PR abierto antes de la fecha, revisión en verde | PR abierto contra tu propio fork |
| PR desde una branch de tarea | PR desde tu `main` |
| Tu carpeta con el nombre exacto de tu login | Una carpeta con nombre parecido |
| Corregir con `push` a la misma branch | Abrir un PR nuevo por cada corrección |

:::

Que yo lo mergee es un trámite posterior y **no depende de ti**.

> [!NOTE]
> **Si sólo recuerdas una cosa:** entregado = pull request abierto, contra `raya-lucaria/fdd_o26:main`, desde una branch, con el check en verde.

## Cierre

Este mismo ritual, con otro número de unidad, es cómo se entrega todo el resto del curso. La segunda vez toma cinco minutos; la tercera, dos.

Si algo no sale, anota qué comando corriste, qué esperabas y qué salió, y tráelo a clase. Ten a mano el [[cheatsheet-git|cheatsheet]]: está para consultarlo, con la única excepción de los cuatro bloques de [[el-ritual-del-curso|El ritual]].
