---
id: el-fork
title: "El fork y tus dos remotes"
nav_title: "El fork"
summary: "Qué es un fork y por qué existe, cómo dejar tu máquina hablando con dos repositorios distintos, y qué hace exactamente cada comando que lo logra."
status: ready
estimated_time: 20m
tags: [github, fork, remote, upstream, origin, fetch, merge, pull]
prerequisites: [github-en-corto]
---

# El fork y tus dos remotes

**GitHub · página 2 de 6** · 20 min

Meta: tu máquina hablando con dos repositorios, y saber cuál es cuál sin pensarlo.

## En corto

- Un **fork** es una copia del repositorio del curso, en tu cuenta, donde sí puedes escribir.
- Al clonar quedaste apuntando al del curso, donde **no** puedes. Se arregla hoy.
- Terminas con dos apodos: **`upstream` para bajar**, **`origin` para subir**.
- Esto es **una vez en el semestre**. Después nunca más.

## Toda la página, en un bloque

```bash
#  0. En el navegador: github.com/raya-lucaria/fdd_o26 → botón Fork

cd ~/fdd/fdd_o26
U=$(gh api user --jq .login) && echo "$U"    # tu login EXACTO, no lo teclees
git remote -v                                # ahora: 2 líneas, las dos del curso
git remote rename origin upstream            # el del curso: de aquí BAJAS
git remote add origin git@github.com:$U/fdd_o26.git   # el tuyo: aquí SUBES
git remote -v                                # ahora: 4 líneas, 2 nombres

git switch main            # párate en main
git fetch upstream         # BAJA del curso. NO toca tus archivos
git merge upstream/main    # lo mete a tu main. AQUÍ sí cambian
git push origin main       # deja tu fork igual que el curso

mkdir -p estudiantes/$U && touch estudiantes/$U/.gitkeep   # tu carpeta
```

> [!NOTE]
> **¿Ya lo hiciste en otra sesión?** Este comando te deja saltar la página:
> ```bash
> git remote -v | grep -q upstream && echo "LISTO" || echo "FALTA"
> ```

::: figure {#git-tres-repos title="Tres repositorios, y sólo en dos puedes escribir"}
![Tres repositorios y las flechas entre ellos: arriba a la izquierda el del curso llamado upstream que sólo se lee, arriba a la derecha tu fork llamado origin donde sí escribes, y abajo tu copia en el disco. Una flecha baja lo nuevo con git fetch, otra sube tu trabajo con git push, y una punteada representa el pull request](../_assets/git-tres-repos.svg)
:::

## Por qué existe el fork

Somos treinta personas y un repositorio. Si todos pudiéramos escribir en `raya-lucaria/fdd_o26`, cualquiera rompería la clase sin querer.

La solución no es repartir permisos: es que **nadie escriba ahí**. Cada quien trabaja en su copia y *propone* sus cambios. El fork es la copia; el pull request es la propuesta.

## Los comandos, uno por uno

### `U=$(gh api user --jq .login)`

Tu **login** no es tu nombre de perfil. Cada semestre alguien crea su carpeta con el nombre equivocado.

```text
U=$(gh api user --jq .login)
│  ││  │   │    │
│  ││  │   │    └── de toda la respuesta, quédate con el campo "login"
│  ││  │   └─────── el recurso "quién soy yo"
│  ││  └─────────── hazle una pregunta a la API de GitHub
│  │└────────────── el programa oficial de GitHub para la terminal
│  └─────────────── $( ): corre esto y quédate con lo que imprima
└────────────────── la variable donde se guarda
```

**Sin `gh`:** tu login es el campo *Username* de `https://github.com/settings/profile`. Entonces `U=tu-login-exacto`.

> [!WARNING]
> `$U` **muere al cerrar la terminal.** Cada vez que un comando diga `$U`, tiene que haber un `echo "$U"` correcto antes, o vas a crear carpetas llamadas `estudiantes//07_git`.

### `git remote rename` y `git remote add`

Un `remote` **es sólo un apodo para una URL**. `origin` no es palabra reservada de Git: es convención. Por eso se puede renombrar.

```text
git remote add origin git@github.com:$U/fdd_o26.git
              │  │     │   │          │   └── el repositorio
              │  │     │   │          └────── tu cuenta
              │  │     │   └───────────────── el servidor
              │  │     └───────────────────── el usuario de SSH: siempre "git"
              │  └─────────────────────────── el apodo que le pones tú
              └────────────────────────────── agrega un remote nuevo
```

**Deberías ver**, al final:

```text
origin    git@github.com:tu-login/fdd_o26.git (fetch)
origin    git@github.com:tu-login/fdd_o26.git (push)
upstream  git@github.com:raya-lucaria/fdd_o26.git (fetch)
upstream  git@github.com:raya-lucaria/fdd_o26.git (push)
```

> [!NOTE]
> **Salida de rescate.** Si algo salió raro, borra y clona tu fork, que ya viene con el `origin` correcto:
> ```bash
> cd ~/fdd && rm -rf fdd_o26
> git clone git@github.com:$U/fdd_o26.git
> cd fdd_o26 && git remote add upstream git@github.com:raya-lucaria/fdd_o26.git
> ```

### `fetch`, `merge` y `pull`

::: table {#git-fetch-merge-pull title="Bajar es dos cosas, no una"}

| Comando | Qué hace | ¿Puede romper algo? |
|---|---|---|
| `git fetch upstream` | Baja los commits del curso a `upstream/main`, aparte | **Nunca.** Siempre seguro |
| `git merge upstream/main` | Los junta con la branch donde estás | Sí: aquí puede haber conflicto |
| `git pull` | Los dos de un jalón | Sí, y no sabes cuál falló |

:::

`git pull` funciona. Pero mientras aprendes conviene separarlos, porque cuando algo falla necesitas saber **cuál de las dos mitades** falló.

## Quién es quién

::: table {#git-tres-nombres title="Los tres repositorios"}

| Nombre | Qué es | Escribes | Cómo llegas |
|---|---|---|---|
| `upstream` | `raya-lucaria/fdd_o26`, el del curso | No, y no lo necesitas | `git fetch upstream` |
| `origin` | Tu fork, en tu cuenta | Sí | `git push origin` |
| Tu disco | `~/fdd/fdd_o26` | Sí, es donde trabajas | Ahí estás parado |

:::

`upstream` es metáfora de río: el material fluye **de arriba hacia abajo**, del curso hacia ti. Río arriba nunca empujas con un comando. Para eso está el pull request.

> [!WARNING]
> Tu carpeta tiene que llamarse **idéntico** a tu login: mismas mayúsculas, mismos guiones. Por eso se usa `$U` y no el teclado. El semestre pasado alguien la creó con guion bajo, y los logins de GitHub no admiten guion bajo.

::: problem {#git-p10-remote title="Permission denied al hacer push"}
Un compañero hizo su fork, clonó el repositorio del curso la semana pasada, y hoy corre `git push origin main`. GitHub le responde con un error de permisos y un 403. Insiste en que su llave SSH funciona, y tiene razón: `ssh -T` lo saluda por su nombre.

¿Qué está pasando y qué comando lo diagnostica?
:::

::: hint {of="git-p10-remote"}
La llave dice quién eres, no a dónde estás mandando. El error no es de identidad, es de destino.
:::

::: answer {of="git-p10-remote"}
Su `origin` **sigue apuntando al repositorio del curso**. Clonó de `raya-lucaria/fdd_o26` y Git guardó esa dirección como `origin`. Hacer el fork en el navegador no cambia nada en su máquina: son dos cosas separadas, una en el servidor y otra en su disco.

Así que el push va contra `raya-lucaria/fdd_o26`, donde no tiene permiso. GitHub lo reconoce perfectamente por su llave, y justo por eso puede decirle que **esa** persona no tiene permiso **ahí**.

Se diagnostica con `git remote -v`: si las cuatro líneas dicen `raya-lucaria`, ése es el problema. Se arregla con `git remote rename origin upstream` y `git remote add origin` con la URL de su fork.
:::

> [!NOTE]
> **Si sólo recuerdas una cosa:** `upstream` es de donde bajas, `origin` es a donde subes. Si `git remote -v` no muestra los dos, nada del flujo funciona.

## Cierre

Repositorios conectados y carpeta creada. Ahora la pieza que sostiene todo el flujo: [[branches-en-serio|Branches, en serio]].
