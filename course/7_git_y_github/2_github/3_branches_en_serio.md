---
id: branches-en-serio
title: "Branches, en serio"
nav_title: "Branches"
summary: "Por qué el curso pide una branch por tarea: qué le hace switch a tus archivos, qué pasa cuando dos branches tocan lo mismo, y cómo se rescata una branch que nació atrasada."
status: ready
estimated_time: 30m
tags: [git, branch, switch, merge, conflicto, flujo]
prerequisites: [el-fork]
---

# Branches, en serio

**GitHub · página 3 de 6** · 30 min

Meta: que crear, cambiar y borrar branches deje de dar miedo, porque el resto del curso se entrega desde una.

## En corto

- Ya sabes que una branch es **una etiqueta que apunta a un commit**. Aquí ves qué te hace *en el disco*.
- `git switch` **reescribe los archivos de tu carpeta** para que coincidan con la branch a la que llegas.
- Una branch por tarea no es burocracia: mantiene tu `main` limpio para la semana siguiente.
- Una branch nacida de un `main` atrasado arrastra basura a tu pull request. Se rescata con un comando.

Todo lo de esta página se hace en el repositorio de verdad, dentro de tu carpeta. Al final se limpia.

---

## 1 · La branch cambia lo que ves

::: figure {#git-branch-disco title="Cambiar de branch reescribe tu carpeta"}
![La misma carpeta vista desde dos branches: parado en la branch de tarea el archivo de trabajo aparece en el listado, y al cambiarse a main el mismo listado ya no lo muestra, aunque el archivo no se borró de la historia](../_assets/git-branch-disco.svg)
:::

```bash
cd ~/fdd/fdd_o26
echo "$U"                       # si sale vacío: U=$(gh api user --jq .login)
git switch main                 # arranca siempre desde main
git switch -c practica-a        # -c = create: créala Y muévete a ella
git branch --show-current       # → practica-a

echo "escrito en practica-a" > estudiantes/$U/nota.txt
git add estudiantes/$U/nota.txt   # por ruta, nunca "git add ."
git commit -m "practica: nota en la branch a"
ls estudiantes/$U                 # nota.txt está

git switch main
ls estudiantes/$U                 # nota.txt NO está      ← la parte que importa

git switch practica-a
ls estudiantes/$U                 # volvió
```

```text
git switch -c practica-a
       │    │      └── el nombre que le pones tú
       │    └───────── -c: créala si no existe
       └────────────── cámbiate de branch (y ajusta los archivos del disco)
```

**No se borró.** Sigue guardado en el commit de `practica-a`. Lo que hizo `switch` fue poner en tu carpeta el contenido que corresponde a `main`, y en `main` ese archivo nunca existió.

> Una branch no es una carpeta ni una copia. Es un punto de la historia, y `git switch` **sincroniza tu carpeta con ese punto**.

> [!WARNING]
> Con cambios sin commitear, Git se niega a cambiar de branch: `Your local changes would be overwritten`. No te regaña, te avisa de que el switch los borraría. Salidas: `git commit` o `git stash`.

---

## 2 · Dos branches, el mismo archivo

```bash
git switch main            # las dos branches nacen del MISMO punto
git switch -c practica-b
echo "escrito en practica-b" > estudiantes/$U/nota.txt
git add estudiantes/$U/nota.txt
git commit -m "practica: nota en la branch b"

git merge practica-a       # trae practica-a a la branch donde estás
```

**Deberías ver:**

```text
CONFLICT (content): Merge conflict in estudiantes/tu-login/nota.txt
Automatic merge failed; fix conflicts and then commit the result.
```

```text
<<<<<<< HEAD
escrito en practica-b        ← lo que hay en la branch donde ESTÁS
=======
escrito en practica-a        ← lo que trae la branch que MERGEASTE
>>>>>>> practica-a
```

Resolver son tres pasos. Salir sin resolver, uno:

```bash
echo "me quedo con las dos" > estudiantes/$U/nota.txt  # 1. edita: cero marcadores
git add estudiantes/$U/nota.txt                        # 2. add = "ya lo resolví"
git commit -m "practica: resuelvo el conflicto"        # 3. cierra el merge

# o, para dejar todo como antes del merge:
git merge --abort
```

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
git switch -c practica-atrasada          # nace del main de ahorita
git switch main
echo "avance del curso" > estudiantes/$U/simulacion.txt
git add estudiantes/$U/simulacion.txt
git commit -m "practica: simulo que el curso avanzó"

git switch practica-atrasada
git log --oneline practica-atrasada..main   # ← el comando que lo diagnostica
git merge main                              # ← el rescate, un solo comando
git log --oneline practica-atrasada..main   # ahora sale vacío
```

```text
git log --oneline practica-atrasada..main
                   │                  └── ...hasta este otro
                   └───────────────────── qué le falta a este punto...
```

**Si esa lista no está vacía, tu branch nació atrasada.**

Por qué importa: el pull request **no compara tu branch contra el curso de hoy**, sino contra el punto donde las dos historias se separaron.

Si tu branch nació de un `main` de hace dos semanas, GitHub muestra como diferencia tuya todo lo que publiqué en esas dos semanas. Tú no lo escribiste. Pero desde fuera tu propuesta dice *"revierte esos nueve archivos"*.

Por eso el flujo empieza por ponerse al día, y no a la mitad.

---

## Limpieza

```bash
git switch main
git fetch upstream
git reset --hard upstream/main     # tira los commits de práctica de tu main
git branch -D practica-a practica-b practica-atrasada
git branch                         # sólo main
git status                         # limpio
```

> [!WARNING]
> `git reset --hard` **descarta trabajo sin preguntar**. Aquí es seguro porque tu `main` local sólo tiene los commits de práctica. Fuera de este contexto, léelo dos veces.

## El ciclo de vida de una branch

::: table {#git-branch-cuando title="Cuándo se crea, cuándo se borra"}

| Momento | Comando | Qué hace |
|---|---|---|
| Empiezas una tarea | `git switch -c tarea-07-git` | La crea desde donde estás. **Párate en `main` actualizado** |
| Te mueves | `git switch <nombre>` | Reescribe tu carpeta con el contenido de esa branch |
| No sabes dónde estás | `git branch --show-current` | Imprime el nombre. Cuesta cero, úsalo |
| Nació atrasada | `git merge main` | Le trae lo que le faltaba |
| Ya te mergearon el PR | `git branch -d tarea-07-git` | La borra **sólo si ya está mergeada** |
| Era práctica, tírala | `git branch -D practica-a` | La borra aunque tenga trabajo sin mergear |

:::

`-d` **se niega** si la branch tiene commits que no están en ningún lado. Esa negativa es una protección: cuando aparece hay que leerla, no escalarla a `-D`.

## Cómo se llaman en este curso

```text
tarea-07-git      tarea-08-python      tarea-09-sql
```

Sin espacios, sin acentos, en minúsculas. Y **nunca se entrega desde `main`**: un pull request que sale de tu `main` se rechaza automáticamente.

::: problem {#git-p9-branch title="Cambié de branch y mi archivo desapareció"}
Una compañera trabajó toda la tarde en `tarea-07-git`, dejó el archivo terminado, y sin hacer commit se cambió a `main` para revisar una cosa. Git no la dejó: le dijo `Your local changes would be overwritten by checkout`.

Ella entendió que su trabajo estaba en peligro, así que borró el archivo para poder cambiarse. Después regresó a `tarea-07-git` y el archivo, obviamente, ya no estaba.

¿Qué debió haber hecho, y qué le habría pasado si el mensaje no hubiera aparecido?
:::

::: hint {of="git-p9-branch"}
El mensaje no era una advertencia sobre el pasado. Era una advertencia sobre lo que estaba a punto de ocurrir.
:::

::: answer {of="git-p9-branch"}
Debió hacer `git commit`, si el trabajo estaba listo, o `git stash`, si quería apartarlo y recuperarlo con `git stash pop` al volver.

Lo importante es leer el mensaje al derecho. `Your local changes would be overwritten` no dice "tu trabajo está en peligro": dice **"si me dejas cambiar de branch, voy a sobrescribir esto"**. Git se niega justamente para no perderlo, igual que `git branch -d`.

Si hubiera hecho commit antes, el cambio de branch habría hecho lo de la primera parte de esta página: el archivo habría desaparecido del listado en `main` y habría vuelto al regresar. **Desaparecer del `ls` y desaparecer de la historia son cosas distintas**, y confundirlas es lo que la llevó a borrarlo.

Moraleja doble: commit antes de cambiar de branch, y cuando Git se niegue a algo, la respuesta casi nunca es forzarlo.
:::

> [!NOTE]
> **Si sólo recuerdas una cosa:** una branch por tarea, nacida de un `main` recién actualizado. Si `git log --oneline tu-branch..main` no sale vacío, tu pull request va a incluir cosas que no son tuyas.

## Cierre

Ya sabes moverte entre branches. Falta **dónde** van tus archivos: [[el-flujo-del-curso|La zona roja y tu espejo]].
