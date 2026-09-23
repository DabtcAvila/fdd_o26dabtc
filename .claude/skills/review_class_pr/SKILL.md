---
name: review_class_pr
description: Revisa las entregas abiertas de los alumnos en este repositorio de curso. Corre las dos revisiones automáticas, juzga el contenido contra los objetos oficiales, mergea lo correcto y comenta lo que no — explicando el error y su consecuencia, nunca dando los comandos. Úsala cuando el profesor pida revisar, calificar, aceptar o rechazar pull requests de entregas.
---

# Revisar las entregas del curso

Las entregas llegan como pull requests contra `raya-lucaria/fdd_o26`. Cada una
la juzgan tres cosas, en este orden: dos revisiones automáticas y una persona.
Esta skill es la parte de la persona.

**El objetivo no es filtrar.** Es que el alumno entienda qué rompió, para que
la próxima entrega salga bien sola. Un rechazo que no enseña nada cuesta lo
mismo que uno que sí.

## 1 · Reúne el estado

```bash
gh pr list -L 40 --json number,author,headRefName,title,labels \
  --jq '.[] | "\(.number)\t\(.author.login)\t\(.headRefName)\t\(.labels|map(.name)|join(","))"'
```

Corre las **dos** revisiones automáticas localmente contra cada PR. Son el
mismo código que corre en CI, así que su veredicto es el que el alumno ya vio:

```bash
unset GH_TOKEN                      # `gh auth token` no existe en este gh;
                                    # exportarlo rompe la autenticación
export GITHUB_REPOSITORY=raya-lucaria/fdd_o26 MANTENEDORES=uumami
export TAREAS="$(grep -A5 'TAREAS:' .github/workflows/entregas.yml \
  | grep 'tarea-' | tr -d ' \n' )"
export BRANCH_ESTRICTA_DESDE=2026-09-18 BRANCH_NOMBRE_ESTRICTO_DESDE=2026-09-22

read -r autor rama < <(gh pr view $N --json author,headRefName --jq '[.author.login,.headRefName]|@tsv')
def=$(gh api repos/$autor/fdd_o26 --jq .default_branch 2>/dev/null || echo main)
PR=$N AUTOR=$autor RAMA=$rama RAMA_DEFAULT=$def python3 .github/scripts/revisa_entrega.py
PR=$N AUTOR=$autor RAMA=$rama                      python3 .github/scripts/revisa_contenido.py
```

**Verde automático no es aprobado.** Las dos revisiones sólo ven forma y
presencia de archivos. Un `certificaciones.md` con la plantilla intacta, una
carpeta inventada o una bitácora vacía pasan en verde.

**Y rojo automático no siempre es culpa del alumno.** Antes de rechazar, lee
qué le dijimos nosotros: ya pasó dos veces que un alumno siguió una
instrucción mal escrita del curso y la revisión lo frenó por obedecerla.

## 2 · Juzga el contenido

Lee los contratos **enteros** antes de juzgar. Son la autoridad, no la memoria:

- `course/<unidad>/_official/assignments/*.yaml` y `tasks/*.yaml`
- Las plantillas que el alumno copia: `codigo/<carpeta>/`

Para leer un archivo de la entrega —el fork suele estar renombrado:

```bash
read -r repo sha <<< "$(gh api repos/raya-lucaria/fdd_o26/pulls/$N --jq '[.head.repo.full_name,.head.sha]|@tsv')"
gh api "repos/$repo/contents/<ruta>?ref=$sha" --jq .content | base64 -d
```

### Lo que ya nos costó equivocarnos

Estas cuatro salieron de rechazar mal a un alumno. No las vuelvas a fallar:

- **La plantilla es la autoridad sobre qué es «lleno».** Si ella no pide la URL
  del certificado, no la exijas. La de la unidad 7 pide sólo fecha y captura;
  la de la unidad 8 pide URL en dos de sus tres secciones. Compruébalo leyendo
  el archivo.
- **Un PDF del Statement of Accomplishment es evidencia válida.** El contrato
  rechaza un certificado «sin contexto», y un SoA trae nombre y curso. Lo que
  sí es defecto es que el documento y el archivo no coincidan: un `.md` que
  enlaza `foo.png` cuando se subió `foo.pdf` deja la evidencia invisible.
- **Sólo las tareas que nombran su branch la exigen.** Las de la unidad 7 nunca
  asignaron nombre; ahí cualquiera razonable vale.
- **No puedes ver las capturas.** Reporta nombre y tamaño y **di que su
  contenido no se verificó**. Nunca afirmes que se ve el 100 % o el nombre.

### Antes de mergear varias del mismo alumno

Dos ramas hermanas que **crean** el mismo archivo con contenido distinto dan
`CONFLICT (add/add)`. Compruébalo con un merge de prueba en un clon
desechable antes de decidir el orden. Si una contiene a la otra, mergea la que
contiene y cierra la otra diciendo que su entrega **sí cuenta**.

## 3 · Decide

Exactamente uno de tres, y dilo así:

| Veredicto | Cuándo |
|---|---|
| **MERGEAR** | Completa y correcta |
| **MERGEAR CON NOTA** | Aceptable, con algo que debe saber para la próxima |
| **NO MERGEAR** | Falta algo sustantivo |

## 4 · El comentario, cuando algo está mal

**Regla dura: ningún comando.** Ni un bloque para copiar y pegar, ni
`git switch -c <nombre>`. Los dos errores que hemos cometido con alumnos
viajaron dentro de bloques de comandos: sin bloques, no hay comando malo que
copiar, y el alumno tiene que entender el error para poder arreglarlo.

Que infieran los comandos de lo que ya vieron en clase, o que lean el log de
GitHub Actions, que nombra la regla y el archivo.

La forma, fija:

1. **Una línea de estado**: «Estado: no aceptada todavía — etiqueta
   `corregir-y-reenviar`».
2. **Lo que está bien**, en una línea.
3. **Si la revisión automática salió en verde, dilo**: el verde sólo comprueba
   que los archivos estén en su carpeta, con su nombre y sin basura; no lee lo
   que dicen. Si no se aclara, el alumno cree que su entrega pasó.
4. **Qué está mal**, concreto y nombrando el archivo, y debajo **por qué eso
   rompe algo**. Nunca «porque la regla lo dice»: la evidencia queda invisible,
   el archivo no es espejo de nada, la fecha es lo que permite verificar que lo
   hiciste a tiempo.

**No digas cómo arreglarlo** (decisión del profesor, 2026-09-22). Ni comando ni
receta en prosa: «crea un usuario después de instalar y cambia a él antes del
CMD» es la solución dicha con palabras. Basta con señalar qué página del curso
lo explica; que el alumno busque cómo.

**Antes de publicar o editar un comentario, vuelve a mirar la fecha del último
commit del PR.** El 2026-09-22 se reescribió el comentario de un alumno que ya
había corregido media hora antes: el comentario le reprochaba un archivo que
ya estaba lleno. Si hay commits posteriores a tu lectura, vuelve a leer.

Si las salidas pegadas **no cuadran** —fechas imposibles, un digest recortado,
IDs que cambian, un `history` sin las capas del Dockerfile, una prueba con una
imagen que su propio `docker images` no muestra, texto idéntico al de otra
entrega—, **di los hechos y por qué cada uno es un error; no afirmes lo que no
sabes** (decisión del profesor, 2026-09-22). No puedes ver su máquina: no digas
que algo «no existe» ni que «usó un modelo». Cierra con la condicional: si usó
alguna herramienta para redactar, que revise cada línea contra lo que corrió,
porque tiene que entender y poder defender lo que entrega. Nunca digas que
«copió» de otro alumno.

Y dos hábitos que valen más que el formato:

- **Empieza por lo que hizo bien**, si hizo algo bien. No es cortesía: un
  alumno que cree que entregó basura no vuelve a leer el comentario.
- **Cuando el error es nuestro, dilo en la primera línea.** Un alumno que cree
  que le cambiaron el criterio deja de confiar en la revisión, y entonces la
  revisión deja de servir.

Cierra pidiendo que suba **a esa misma rama**: el pull request se actualiza
solo y no hay que abrir otro.

## 5 · Ejecuta

Etiquetas del curso — créalas si no existen:

| Etiqueta | Para |
|---|---|
| `entrega-aceptada` | Mergeadas |
| `corregir-y-reenviar` | Falta algo; el comentario dice qué |
| `ya-entregada` | Su contenido ya está en `main`; se cierra sin penalización |
| `fuera-de-alcance` | No pertenece a este repositorio ni a ninguna entrega |

```bash
# Etiquetar. OJO: `-f 'labels[]=x'` falla —zsh lo expande y la API lo rechaza.
gh api -X POST "repos/raya-lucaria/fdd_o26/issues/$N/labels" \
  --input - <<< '{"labels":["entrega-aceptada"]}'

gh pr comment $N --body-file <archivo>
gh pr merge   $N --merge --delete-branch=false
gh pr close   $N
```

`gh pr merge` no imprime nada al tener éxito: **verifica con
`gh pr view $N --json state`**, no supongas.

Un check en `UNSTABLE` suele ser el workflow de Pages esperando aprobación de
fork, no un fallo. Mira `revision` antes de alarmarte.

## 6 · Cierra y reporta

Al terminar, **ningún PR abierto sin etiqueta**. Reporta al profesor: cuántas
mergeadas, cuántas cerradas y por qué, cuántas esperando corrección, y
**cualquier error del curso que hayas encontrado** — una página que contradice
al workflow, una instrucción nuestra mal escrita. Eso vale más que el conteo:
un alumno equivocado es un alumno; una instrucción equivocada son todos.

## Lo que esta skill no hace

No califica con puntos. No decide si una captura prueba lo que dice probar.
No responde preguntas del alumno fuera del pull request. Eso es del profesor.
