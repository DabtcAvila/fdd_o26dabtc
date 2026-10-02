---
id: examen-github-solucion
title: "Examen de GitHub: solución"
nav_title: "GitHub · solución"
summary: "La solución del examen de GitHub, versiones A y B, inciso por inciso: la respuesta, por qué es ésa, qué otras respuestas también valían y qué página repasar."
status: ready
estimated_time: 20m
tags: [examen, solucion, git, github, ritual, branches, anexo]
prerequisites: [examen-github-enunciado]
---

# Examen de GitHub: solución

**Anexo · Exámenes** · el enunciado está en [[examen-github-enunciado]]. Contéstalo antes de leer esto.

## Cómo se calificó

- **Pregunta 1**: 3 puntos, cuatro incisos de 0.75. Los incisos son independientes: equivocarse en a) no arrastra a b), c) ni d). No pide comandos; una respuesta hecha sólo de comandos, sin explicar el mecanismo, no pasa de la mitad del inciso.
- **Pregunta 2**: 7 puntos, repartidos por columna: el **orden** vale 2 (0.25 por renglón), la **explicación** 2 (0.25 por renglón) y los **comandos** 3 (0.375 por renglón). Las tres columnas se califican por separado: un renglón mal numerado conserva sus puntos de explicación y de comandos.
- Es a mano: no se descuenta por acentos, comillas ni espacios. Se descuenta cuando el comando haría otra cosa.
- `git checkout -b` vale lo mismo que `git switch -c`, y `git checkout <rama>` lo mismo que `git switch <rama>`. Tu login literal vale lo mismo que `$GHUSER`.

## Versión A · 1. La rama que nació de otra rama

El compañero creó `tarea-08-datacamp-intro` parado en `tarea-07-git`, cuyo pull request sigue abierto. D y E cuelgan de C, y C no está en `main`.

### a) ¿Qué lista el pull request de la 08?

**Respuesta.** Lista los **cinco** commits, A, B, C, D y E, y por lo tanto las **dos** carpetas: `estudiantes/<login>/07_git/…` (de la tarea 07) y `estudiantes/<login>/docker/…` (de la 08).

**Por qué.** Un pull request no muestra «lo que hiciste en tu rama»: muestra la diferencia entre tu rama y el punto donde se separó de `main`. Ese punto es el último `o`. Todo lo que hay entre ese `o` y E entra, y eso incluye A, B y C. No aparecen porque los haya vuelto a tocar, sino porque la rama los **hereda** del commit donde nació. De paso, A, B y C aparecen a la vez en dos pull requests abiertos.

**También valía.** Describirlo en commits en vez de carpetas, si dice de dónde salen. Listar las dos carpetas sin explicar la herencia valía la mitad. «Sólo lo de la tarea 08» valía cero.

**Repasa:** [[branches-y-merge]] y [[branches-en-serio]].

### b) Una cosa bien y una mal

**Respuesta.**

- **Bien** (cualquiera de éstas): trabajó en una rama y no en `main`, así que su `main` sigue siendo copia del curso; puso cada tarea en su carpeta del espejo; el nombre de la rama tiene la forma `tarea-NN-nombre`.
- **Mal**: la rama de la 08 nació de `tarea-07-git` y no de `main`.

**Por qué.** Una rama arranca con **todo** el estado del commit donde nace. Si nace en C, su punto cero ya trae A, B y C, y todo eso pasa a ser parte de lo que propone. Lo que una rama carga no depende de lo que tocaste después, sino de dónde nació. La revisión automática lo rechaza por la regla de «una sola carpeta»: el pull request toca `07_git/` y `docker/`.

**También valía.** Cualquier «bien» de la lista. Si el «mal» no hablaba de dónde nació la rama («subió archivos de más», «se equivocó de carpeta»), valía la mitad.

### c) ¿Cómo se evita?

**Respuesta.** Volviendo a `main`, y a un `main` **al día** (el bloque A completo del ritual), antes de crear la rama de cada tarea. Las ramas de las tareas son hermanas que cuelgan de `main`, nunca una encadenada a otra.

**Por qué lo resuelve.** Si la rama nace en la punta de `main`, el punto de separación con el curso es esa punta. Entre ese punto y tu rama sólo queda lo que escribiste para la tarea 08, y es lo único que el pull request lista.

**También valía.** Para arreglarlo hoy: crear otra vez la rama desde `main` y llevar ahí sólo el trabajo de la 08. «Que nazca de `main`» sin decir por qué eso cambia lo que muestra el pull request valía la mitad.

**Repasa:** [[el-ritual-del-curso]].

### d) Si le mergean la 07 antes, ¿cambia el pull request?

**Respuesta.** **Sí.** Ahora lista sólo D y E, es decir, sólo la carpeta de la tarea 08.

**Por qué.** Al mergear la 07, A, B y C pasan a estar en `upstream/main`. El punto donde las dos historias se separan deja de ser el `o` viejo y se vuelve C (o el commit de merge que lo contiene). La rama de la 08 no se movió ni un bit. Lo que se movió es **la base** contra la que se compara. Un pull request es una diferencia contra una base, y la base depende de lo que pase del otro lado.

**Matiz.** Esto funciona porque el curso mergea con un commit de merge, que conserva A, B y C con sus hashes. Si se mergeara con *Squash and merge*, a `main` llegaría un commit **nuevo** con otro hash. A, B y C no serían ancestros de `main`, la base no se movería, y el pull request seguiría mostrando todo, ahora quizá con conflictos.

**También valía.** «Sí» sin explicar que se movió la base valía la mitad. «No» valía cero.

**Repasa:** [[trabajo-en-paralelo]].

## Versión B · 1. La rama que nació vieja

El compañero creó su rama el primer día, en el cuarto commit. Después el curso publicó P, Q y R, y la sección nueva de `codigo/docker/certificaciones.md` vive en R. Su `main` y su `origin/main` siguen en el cuarto commit.

### a) ¿Por qué le falta la sección?

**Respuesta.** Porque **nunca la tuvo**. Su rama nació en el cuarto commit, **antes** de R.

**Por qué.** Lo que hay en una rama es el estado del commit donde nació más lo que pusiste encima. La sección nueva vive en R, que está después de ese punto, así que nunca entró a su rama. Además copió la plantilla el primer día: su copia es la versión vieja. No le falta porque la haya quitado; le falta porque nunca llegó.

**También valía.** «No actualizó», sin ligarlo a dónde nació la rama, valía la mitad. «La borró» o «se perdió al hacer commit» valía cero.

**Repasa:** [[branches-y-merge]].

### b) Dos cosas que hizo bien

**Respuesta.** Cualquier par de éstas:

1. Trabajó en una rama y no en `main`: su `main` sigue siendo copia exacta del curso, y por eso arreglarlo es barato.
2. Respetó la regla del espejo: copió la plantilla a su carpeta en vez de editar `codigo/`.
3. Hizo el fork y el paso 0 desde el primer día.
4. El nombre de la rama es el que la tarea asignó.

**Por qué se pregunta.** Para diagnosticar hay que saber qué no tocar. Quien sólo busca errores propone «borra todo y empieza de nuevo», que es más caro de lo necesario.

**También valía.** Con una sola cosa, la mitad. «Nada» valía cero: el enunciado avisa que sí las hay.

### c) ¿Se puede mergear? ¿Qué problema trae?

**Respuesta.**

- **Sí se puede**, y casi seguro sin conflicto.
- **El problema no es de Git, es de contenido.** Entregó trabajo hecho sobre una plantilla vieja: le falta lo que la sección nueva pide, y pierde puntos aunque la revisión automática salga en verde.
- **Se evita** haciendo el bloque A antes de crear la rama, y volviendo a copiar el espejo desde `codigo/` cuando el curso publica una corrección.

**Por qué se puede mergear.** X e Y sólo tocan `estudiantes/<login>/`, que no toca nadie más, y P, Q y R sólo tocan `codigo/`. Nadie cambió las mismas líneas, así que Git no tiene nada que decidir. La regla del espejo existe precisamente para eso. El verde dice «no rompiste las reglas del repositorio»; no dice «tu tarea está completa».

**También valía.** Cada una de las tres partes valía un tercio.

**Repasa:** [[el-flujo-del-curso]].

### d) `git merge upstream/main` dentro de su rama

Son dos preguntas, y las dos respuestas van contra la intuición.

**¿Se actualiza su copia del archivo? No.** El merge trae P, Q y R, así que `codigo/docker/certificaciones.md` sí queda al día. Pero **su** copia es `estudiantes/<login>/docker/certificaciones.md`: otro archivo, en otra ruta, que él creó copiando la versión vieja. Git no sabe que uno es espejo del otro y no lo toca. Hay que volver a copiarlo.

**¿Cambia lo que muestra el pull request? No cambia la lista de archivos.** Antes del merge la base era el cuarto commit, y el pull request ya mostraba sólo su carpeta. Después la base es R y sigue mostrando sólo su carpeta: su rama nunca tuvo archivos del curso, así que mover la base no le quita nada. Lo único que cambia es que la rama deja de estar atrasada respecto de `main`.

**Contraste con la versión A.** Allá mover la base **sí** cambiaba el pull request, porque la rama cargaba commits de otra tarea. Aquí no carga nada ajeno.

**También valía.** Cada mitad valía la mitad del inciso. Quien contestó «sí se actualiza» confundió el archivo del curso con su copia.

**Repasa:** [[branches-en-serio]].

## Las dos versiones · 2. El ritual, en orden

Los ocho pasos son los mismos en A y en B; sólo cambia el desorden en que se imprimieron. Leyendo la tabla del examen de arriba abajo, el orden correcto es:

- **Versión A:** 5 · 8 · 2 · 1 · 6 · 7 · 3 · 4
- **Versión B:** 6 · 3 · 7 · 5 · 8 · 4 · 2 · 1

O sea: en la A, el primer renglón impreso es el paso 5, el segundo el 8, y así. No uses la clave de una versión para la otra.

Abajo, los pasos ya en orden, con lo que se esperaba en cada columna. Repasa todo en [[el-ritual-del-curso]].

### Paso 1 · Conectar tu copia con el curso (una sola vez)

**Qué hace y por qué.** Deja tu copia hablando con los dos repositorios: `upstream` es de donde **bajas** (el del curso) y `origin` es a donde **subes** (tu fork). Sin esto no hay de dónde ponerte al día ni a dónde empujar. Se hace una vez en el semestre. Si ya está hecho, el comando de comprobación de [[el-ritual-del-curso]] imprime `SALTA`.

**Comandos.**

```bash
# en el navegador: fork de github.com/raya-lucaria/fdd_o26 (sin comando)
git remote rename origin upstream
git remote add origin git@github.com:$GHUSER/fdd_o26_$GHUSER.git
echo 'export GHUSER=tu-login' >> ~/.zshrc     # o ~/.bashrc
exec $SHELL
git remote -v                                  # comprobación
```

**También valía.** La URL `https://` en lugar de la de ssh. Escribir el `export` a mano en el perfil. `rename` y `add` en cualquier orden. Lo que tenía que aparecer: el fork, los dos remotes con su nombre correcto y `GHUSER` en el perfil.

### Paso 2 · Traerte lo que el curso publicó (bloque A)

**Qué hace y por qué.** `git switch main` te para en `main` vengas de donde vengas: por eso el bloque A también limpia lo de la semana pasada. `git fetch upstream` baja los commits del curso y los deja **aparte**: no toca ni un archivo tuyo.

**Comandos.**

```bash
git switch main
git fetch upstream
```

**También valía.** `git checkout main`. `git pull upstream main` valía como este paso y el siguiente juntos, sin darle el punto dos veces.

### Paso 3 · Incorporarlo a tu main y dejar tu fork al día (bloque A)

**Qué hace y por qué.** El merge es donde **sí** cambian tus archivos. El push deja el `main` de tu fork igual al del curso: los tres `main` iguales. Si falta, tu rama nace atrasada, y el pull request arrastra cambios que no escribiste o le falta lo nuevo, como en la versión B.

**Comandos.**

```bash
git merge upstream/main
git push origin main
```

**También valía.** `git merge --ff-only upstream/main`. Omitir el push explicando que sólo afecta a tu fork valía con medio descuento.

### Paso 4 · Crear la rama de esta tarea (bloque B)

**Qué hace y por qué.** Una rama nace del commit donde estás parado; por eso tiene que nacer de un `main` recién actualizado (la versión A del ejercicio 1 es lo que pasa si no). Y nunca se entrega desde `main`: tu `main` es tu copia del curso, y si le metes tu trabajo deja de serlo.

**Comandos.**

```bash
git switch -c tarea-08-imagen
```

**También valía.** `git checkout -b tarea-08-imagen`, o `git branch tarea-08-imagen` seguido de `git switch tarea-08-imagen`. El nombre tiene que tener la forma `tarea-NN-nombre`, en minúsculas y con guiones.

### Paso 5 · Tu carpeta y el espejo (bloque B)

**Qué hace y por qué.** La regla del espejo: misma ruta, mismo nombre, dentro de tu carpeta. Con una carpeta por persona nadie toca las líneas de nadie, y treinta pull requests se mergean sin conflicto. El `/.` final copia el **contenido** de la carpeta y no la carpeta misma.

**Comandos.**

```bash
mkdir -p estudiantes/$GHUSER/08_contenedores
cp -r codigo/08_contenedores/. estudiantes/$GHUSER/08_contenedores/
```

**También valía.** El login literal en vez de `$GHUSER`. `cp -r codigo/08_contenedores/* …`. Sin el `/.`, si el destino ya existe la carpeta queda anidada dentro de sí misma (`08_contenedores/08_contenedores/`): perdía una fracción.

### Paso 6 · Mirar, apartar por ruta, volver a mirar (bloque C)

**Qué hace y por qué.** Los dos `git status` no son adorno. El primero dice qué cambió antes de apartar, y el segundo qué vas a guardar exactamente. El `add` **por ruta** es lo que evita subir basura y lo que deja verde la revisión automática.

**Comandos.**

```bash
git status
git add estudiantes/$GHUSER/08_contenedores
git status
```

**También valía.** Una ruta más fina, archivo por archivo. **No valía** `git add .` ni `git add -A`, en ningún renglón: el curso los prohíbe, y son los que meten basura. Omitir uno de los dos `status` perdía una fracción; omitir los dos, el punto de comandos del paso.

### Paso 7 · Guardar y subir tu rama (bloque C)

**Qué hace y por qué.** El commit guarda lo que apartaste, con su mensaje. El push sube **la rama**, no `main`. El `-u` la empareja con la de tu fork, para que después baste `git push`.

**Comandos.**

```bash
git commit -m "unidad 08: mi imagen"
git push -u origin tarea-08-imagen
```

**También valía.** `--set-upstream` en lugar de `-u`. Cualquier mensaje razonable. Sin `-u`, una fracción de descuento.

### Paso 8 · Abrir el pull request (bloque C)

**Qué hace y por qué.** Es el paso que **no tiene comando**: se hace en el navegador. El pull request es tu propuesta al curso. El error clásico es dejar *base repository* apuntando a tu propio fork: el pull request se crea, se ve bien, y no le llega al profesor.

**Qué se hace.** Botón *Compare & pull request*, y revisar las cuatro casillas:

| Casilla | Valor |
|---|---|
| base repository | `raya-lucaria/fdd_o26` |
| base | `main` |
| head repository | `tu-login/fdd_o26_tu-login` |
| compare | `tarea-08-imagen` |

**También valía.** Decir que no hay comando y nombrar al menos que la base es el repositorio del curso y que *compare* es la rama de la tarea.

### Lo que no se descontaba, y lo que siempre

- **No se descontaba:** llamar «bloques» a los pasos; usar como ejemplo otra rama de la unidad 8 (`tarea-08-datacamp-intro`, por ejemplo) o la carpeta `docker/`. El examen pedía un ejemplo, no el mapa de tareas.
- **Siempre se descontaba:** poner la conexión con el curso (el «paso 0» del ritual) en otro lugar que no fuera el 1; entregar desde `main`; `git add .`; y poner el bloque A después del B o del C, que es justo lo que produce la rama atrasada de la versión B.
