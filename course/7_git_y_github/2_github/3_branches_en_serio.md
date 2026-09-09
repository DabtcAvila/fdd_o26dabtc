---
id: branches-en-serio
title: "Branches, en serio"
nav_title: "Branches"
summary: "Por qué el curso pide una branch por tarea: qué le hace switch a tus archivos, qué pasa cuando dos branches tocan lo mismo, y cómo se rescata una branch que nació atrasada."
status: ready
estimated_time: 35m
tags: [git, branch, switch, merge, conflicto, flujo]
prerequisites: [el-fork]
---

# Branches, en serio

**GitHub · página 3 de 6** · 35 min

Meta: que crear, cambiar y borrar branches deje de dar miedo, porque el resto del curso se entrega desde una.

## En corto

- Ya sabes que una branch es **una etiqueta que apunta a un commit**. Aquí ves qué te hace *en el disco*.
- `git switch` **reescribe los archivos de tu carpeta** para que coincidan con la branch a la que llegas.
- Una branch por tarea no es burocracia: mantiene tu `main` limpio para la semana siguiente.
- Una branch nacida de un `main` atrasado arrastra basura a tu pull request. Se rescata con un comando.
- Y resolver un conflicto es **editar el archivo y borrar los marcadores**. Git no comprueba que lo hayas hecho.

Todo lo de esta página se hace en el repositorio de verdad, dentro de tu carpeta. Al final se limpia.

---

## 1 · La branch cambia lo que ves

::: figure {#git-branch-disco title="Cambiar de branch reescribe tu carpeta"}
![La misma carpeta vista desde dos branches: parado en la branch de tarea el archivo de trabajo aparece en el listado, y al cambiarse a main el mismo listado ya no lo muestra, aunque el archivo no se borró de la historia](../_assets/git-branch-disco.svg)
:::

```bash
cd ~/fdd/fdd_o26
echo "$GHUSER"                    # si sale vacío, redefínela
git switch main              # arranca siempre desde main
git switch -c practica-a     # -c = create: créala Y muévete
git branch --show-current    # → practica-a

echo "escrito en practica-a" > estudiantes/$GHUSER/nota.txt
git add estudiantes/$GHUSER/nota.txt   # por ruta, nunca "."
git commit -m "practica: nota en la branch a"
ls estudiantes/$GHUSER            # nota.txt está

git switch main
ls estudiantes/$GHUSER            # NO está  ← lo importante

git switch practica-a
ls estudiantes/$GHUSER            # volvió
```

```text
git switch -c practica-a
       │    │      └── el nombre, lo pones tú
       │    └───────── -c: créala si no existe
       └────────────── cámbiate de branch, y ajusta el disco
```

**No se borró.** Sigue guardado en el commit de `practica-a`. Lo que hizo `switch` fue poner en tu carpeta el contenido que corresponde a `main`, y en `main` ese archivo nunca existió.

> Una branch no es una carpeta ni una copia. Es un punto de la historia, y `git switch` **sincroniza tu carpeta con ese punto**.

> [!WARNING]
> Con cambios sin commitear, Git **puede** negarse a cambiar de branch:
> ```text
> error: Your local changes to the following files
> would be overwritten by checkout:
> ```
> Sólo se niega si ese archivo **difiere** entre las dos branches; si es igual, te deja pasar y se lleva la edición contigo. No te regaña: te avisa de que el switch la borraría. Salidas: `git commit` o `git stash`.

---

## 2 · Dos branches, el mismo archivo

```bash
git switch main          # las dos nacen del MISMO punto
git switch -c practica-b
echo "escrito en practica-b" > estudiantes/$GHUSER/nota.txt
git add estudiantes/$GHUSER/nota.txt
git commit -m "practica: nota en la branch b"

git merge practica-a     # tráela a la branch donde estás
```

**Deberías ver:**

```text
Auto-merging estudiantes/tu-login/nota.txt
CONFLICT (add/add): Merge conflict in
  estudiantes/tu-login/nota.txt
Automatic merge failed; fix conflicts and then
commit the result.
```

### Qué le pasó a tu archivo

```bash
git status                      # both added: nota.txt
cat estudiantes/$GHUSER/nota.txt
```

Git **no borró nada**: metió las dos versiones en el mismo archivo, separadas por tres líneas marcadoras.

```text
<<<<<<< HEAD
escrito en practica-b
=======
escrito en practica-a
>>>>>>> practica-a
```

::: table {#git-marcadores title="Las tres líneas que Git inserta"}

| Línea | Qué marca |
|---|---|
| `<<<<<<< HEAD` | aquí empieza **tu** versión, la de la branch donde estás |
| `=======` | aquí acaba la tuya y empieza la otra |
| `>>>>>>> practica-a` | aquí acaba la de la branch que mergeaste, y dice cuál es |

:::

> **Resolver el conflicto son dos cosas, y las dos son obligatorias:**
> 1. Dejar el archivo con el contenido que quieres.
> 2. **Borrar las tres líneas marcadoras.**

Nadie te obliga a escoger un lado. Puedes quedarte con una mitad, con la otra, con las dos, o escribir algo nuevo. Git no opina: sólo se niega a decidir por ti.

### Paso 1: edítalo con un editor

Aquí **no** sirve `echo` ni `printf`: sobrescriben el archivo entero, y en un archivo de verdad tienes que conservar todo lo que no está en conflicto. Ábrelo:

```bash
nano estudiantes/$GHUSER/nota.txt
```

Digamos que quieres quedarte con las dos frases. **Borra las tres líneas marcadoras** y deja el archivo exactamente así:

```text
escrito en practica-b
escrito en practica-a
```

En `nano`, que es el editor que viste en la unidad de terminal:

| Para | Teclas |
|---|---|
| **Borrar la línea donde está el cursor** | `Ctrl+K` |
| Moverte | las flechas |
| Guardar | `Ctrl+O`, luego Enter |
| Salir | `Ctrl+X` |

Son tres `Ctrl+K`, uno por cada marcador. Si prefieres VS Code, `code estudiantes/$GHUSER/nota.txt` te muestra botones de *Accept Current* / *Accept Incoming* que hacen lo mismo por ti.

### Paso 2: comprueba que no quedó ningún marcador

Éste es el paso que casi nadie hace, y el que evita el error de la advertencia de abajo.

**Para qué sirve:** los marcadores son fáciles de dejar a medias, sobre todo en un archivo largo donde el conflicto está en la línea 200. Este comando **los cuenta por ti**, en vez de que los busques con la vista.

```bash
cat estudiantes/$GHUSER/nota.txt   # míralo con tus ojos
grep -c '^[<=>]\{7\}' estudiantes/$GHUSER/nota.txt
```

Qué hace, pieza por pieza:

```text
grep -c '^[<=>]\{7\}' nota.txt
     │    ││    │
     │    ││    └── ...siete veces seguidas
     │    │└─────── uno de estos tres caracteres...
     │    └──────── al principio de la línea...
     └───────────── -c: no me las muestres, cuéntalas
```

Es decir: **cuenta las líneas que empiezan con `<<<<<<<`, `=======` o `>>>>>>>`**. El patrón es de la [[expresiones-regulares|unidad de expresiones regulares]].

Cada conflicto mete tres líneas, así que con dos conflictos en el mismo archivo el resultado es `6`. Por eso la regla es «cero», no «menos de tres». Y ojo con un falso positivo honesto: en Markdown, una línea de `=======` bajo un título es un subrayado legítimo y también cuenta. Si el número no baja a cero y no ves marcadores, mira si es eso.

::: table {#git-grep-marcadores title="Qué hacer con el número que te responde"}

| Si dice | Qué significa | Qué haces |
|---|---|---|
| `0` | No queda ningún marcador | Sigue al paso 3 |
| **cualquier otro número** | Todavía hay marcadores dentro | Vuelve al editor y bórralos |

:::

> [!WARNING]
> **Si dejas un marcador, Git lo commitea sin decirte nada.** No hay advertencia, no hay error: tu archivo se queda con un `<<<<<<< HEAD` dentro para siempre, y lo descubres semanas después cuando el código no corre. Por eso se comprueba, y no se confía.

### Paso 3: cierra el merge

```bash
# add = "ya lo revisé, ésta es la buena"
git add estudiantes/$GHUSER/nota.txt
git status                        # All conflicts fixed
git commit -m "practica: resuelvo el conflicto"
```

Aquí `git add` significa algo distinto de lo habitual: no es "apartar para el próximo commit", es **"ya lo resolví"**. Por eso el conflicto se cierra con el mismo comando que usas para todo lo demás.

### Si te arrepientes: la salida de emergencia

```bash
git merge --abort
```

Deja todo exactamente como estaba antes de intentar el merge, marcadores incluidos. **Sólo funciona mientras el merge sigue abierto**: una vez que hiciste el `commit` del paso 3, ya no hay nada que abortar.

![Ciudad densa bajo lluvia intensa en teal frío y concreto húmedo, vista desde lo alto entre dos torres enfrentadas: tras una ventana iluminada de cada torre trabaja una figura pequeña de espaldas, y un solo cable tenso une las dos ventanas con una gota de luz ámbar suspendida en el centro exacto, sin avanzar hacia ningún lado.](../_assets/ilus-git-colaboracion.jpg)

Lo que acabas de provocarte a solas es exactamente lo que pasa cuando dos personas tocan el mismo archivo. La mecánica es idéntica; lo único que cambia es que del otro lado hay alguien más. Por eso conviene romperlo aquí primero.

> [!NOTE]
> Un conflicto no es un error. Es Git negándose a inventar. La única forma de que nunca aparezca es que dos personas no toquen las mismas líneas, y de ahí sale la regla de la página 4.

---

## 3 · La branch atrasada, que es la que rompe entregas

::: figure {#git-branch-atrasada title="Una branch nacida de un main viejo"}
![Dos escenarios comparados: arriba la branch nace de un main atrasado y el pull request muestra como diferencia propia todos los commits del curso que faltaban; abajo la misma branch después de traer main con un merge, y el pull request muestra sólo los archivos del estudiante](../_assets/git-branch-atrasada.svg)
:::

Éste es el error más caro del semestre y **no da ningún mensaje**. Simúlalo:

```bash
git switch main
git switch -c practica-atrasada   # nace del main de ahorita

# haz algo en tu branch, como en una tarea de verdad
echo "mi trabajo" > estudiantes/$GHUSER/tarea.txt
git add estudiantes/$GHUSER/tarea.txt
git commit -m "practica: mi trabajo de la tarea"

# ahora simulamos que el curso avanzó mientras tú trabajabas.
# El avance va en su propia branch: tu main no se toca en toda
# la práctica, y por eso la limpieza del final es indolora.
git switch -c curso-simulado main
echo "avance del curso" > estudiantes/$GHUSER/simulacion.txt
git add estudiantes/$GHUSER/simulacion.txt
git commit -m "practica: simulo que el curso avanzó"

git switch practica-atrasada

# el comando que lo DIAGNOSTICA: qué le falta a tu branch
git log --oneline practica-atrasada..curso-simulado

# el RESCATE, un solo comando
git merge curso-simulado

# ahora la lista sale vacía
git log --oneline practica-atrasada..curso-simulado
```

```text
git log --oneline practica-atrasada..curso-simulado
                  │                  └── ...hasta este otro
                  └──────────────── qué le falta a éste...
```

**Si esa lista no está vacía, tu branch nació atrasada.**

Aquí se compara contra `curso-simulado` porque ahí pusimos el avance. **En la vida real se compara contra `upstream/main`**, que es donde de verdad avanza el curso: tu `main` local puede estar tan atrasado como tu branch, y entonces `..main` te sale vacío y te miente.

Por qué importa: el pull request **no compara tu branch contra el curso de hoy**, sino contra el punto donde las dos historias se separaron.

Si tu branch nació de un `main` de hace dos semanas, GitHub muestra como diferencia tuya todo lo que publiqué en esas dos semanas. Tú no lo escribiste. Pero desde fuera tu propuesta dice *"revierte esos nueve archivos"*.

Por eso el flujo empieza por ponerse al día, y no a la mitad.

---

## Limpieza

```bash
git switch main
git branch -D practica-a practica-b \
              practica-atrasada curso-simulado
git branch                      # sólo main
git status                      # sólo tu carpeta, untracked
```

Todo lo que creaste vivía en branches, así que borrarlas basta: **tu `main` nunca se tocó**, y por eso aquí no hace falta ningún comando destructivo. Ésa es justamente la ventaja de trabajar en branches, vivida en carne propia.

> [!NOTE]
> `-D` con mayúscula borra aunque la branch tenga commits sin mergear. Aquí es lo que queremos, porque era práctica. En una branch de tarea de verdad se usa `-d`, que se niega si hay trabajo sin guardar en ningún lado.

## El ciclo de vida de una branch

::: table {#git-branch-cuando title="Cuándo se crea, cuándo se borra"}

| Momento | Comando | Qué hace |
|---|---|---|
| Empiezas una tarea | `git switch -c tarea-07-git` | La crea desde donde estás. **Párate en `main` actualizado** |
| Te mueves | `git switch <nombre>` | Reescribe tu carpeta con el contenido de esa branch |
| No sabes dónde estás | `git branch --show-current` | Imprime el nombre. Cuesta cero, úsalo |
| Nació atrasada | `git merge main` | Le trae lo que le faltaba |
| ¿Nació atrasada? | `git log --oneline <branch>..upstream/main` | Si no sale vacío, sí |
| Ya te mergearon el PR | `git branch -d tarea-07-git` | La borra **sólo si ya está mergeada** |
| Era práctica, tírala | `git branch -D practica-a` | La borra aunque tenga trabajo sin mergear |

:::

`-d` **se niega** si la branch tiene commits que no están en ningún lado. Esa negativa es una protección: cuando aparece hay que leerla, no escalarla a `-D`.

## Cómo se llaman en este curso

```text
tarea-07-git      tarea-08-python      tarea-09-sql
```

Sin espacios, sin acentos, en minúsculas. Y **nunca se entrega desde `main`**: un pull request que sale de tu `main` se rechaza automáticamente.

::: problem {#git-p9-marcadores title="Commiteé con los marcadores dentro"}
Un compañero resuelve su conflicto con prisa. Borra dos de las tres líneas marcadoras, deja el archivo como quiere, y hace `git add` y `git commit`.

Git no le dice nada. El commit se crea, `git status` queda limpio, y él sigue con su vida. Dos semanas después su script no corre y el error apunta a una línea que dice `>>>>>>> practica-a`.

¿Por qué Git no le avisó, y qué debió haber hecho?
:::

::: hint {of="git-p9-marcadores"}
Piensa qué significa exactamente `git add` durante un merge, y qué es lo que Git sabe comprobar y qué no.
:::

::: answer {of="git-p9-marcadores"}
Git **no lee el contenido de tus archivos**. Los marcadores no son sintaxis de Git: son texto que Git escribió dentro del archivo para que tú decidieras. Una vez escritos, para Git son caracteres como cualquier otro.

Y `git add`, durante un merge, significa una sola cosa: **"ya lo revisé, esta versión es la buena"**. Es una afirmación tuya, no una comprobación suya. Cuando le dices eso, Git te cree. Por eso el commit se crea sin una advertencia, sin un warning, sin nada.

Ésa es la única parte de todo el flujo donde Git no te protege. En todo lo demás —un push atrasado, una branch sin mergear, un switch con trabajo sin guardar— hay un mensaje que te detiene. Aquí no.

Debió haber corrido la comprobación del paso 2 antes del `add`:

```bash
grep -c '^[<=>]\{7\}' <archivo>   # tiene que decir 0
```

Y para arreglarlo ahora: editar el archivo, borrar lo que quedó, y commitear la corrección. El commit viejo se queda en la historia con la basura dentro, que es el costo de no haber mirado.
:::

> [!NOTE]
> **Si sólo recuerdas una cosa:** una branch por tarea, nacida de un `main` recién actualizado. Si `git log --oneline tu-branch..upstream/main` no sale vacío, tu pull request va a incluir cosas que no son tuyas.

## Cierre

Ya sabes moverte entre branches. Falta **dónde** van tus archivos: [[el-flujo-del-curso|La zona roja y tu espejo]].
