---
id: el-fork
title: "El fork y tus dos remotes"
nav_title: "El fork"
summary: "Qué es un fork y por qué existe, cómo dejar tu máquina hablando con dos repositorios distintos, y qué hace exactamente cada comando que lo logra."
status: ready
estimated_time: 25m
tags: [github, fork, remote, upstream, origin, fetch, merge, pull]
prerequisites: [github-en-corto]
---

# El fork y tus dos remotes

**GitHub · página 2 de 6** · 25 min

Meta: tu máquina hablando con dos repositorios, y saber cuál es cuál sin pensarlo.

## En corto

- Un **fork** es una copia del repositorio del curso **en tu cuenta de GitHub**, donde sí puedes escribir.
- Al clonar quedaste apuntando al del curso, donde **no** puedes. Se arregla hoy.
- Terminas con dos apodos: **`upstream` para bajar**, **`origin` para subir**.
- Son **dos pasos**: el fork en el navegador, y el resto en la terminal.
- Esto es **una vez en el semestre**. Después nunca más.

> [!NOTE]
> **¿Ya lo hiciste en otra sesión?** Este comando te deja saltar la página:
> ```bash
> cd ~/fdd/fdd_o26
> git remote -v | grep -q upstream \
>   && echo "LISTO" || echo "FALTA"
> ```

## Paso 1 · El fork, en el navegador

**Empieza por aquí.** Nada de lo demás funciona sin esto, y no hay comando de Git que lo haga: el fork no es de Git, es de GitHub.

> [!IMPORTANT]
> El fork ocurre **en los servidores de GitHub**, no en tu computadora. Presionar el botón no cambia ni un archivo de tu disco. Son dos cosas separadas, y confundirlas es la causa del error del ejercicio del final de esta página.

**Haz:** entra a `https://github.com/raya-lucaria/fdd_o26`.

Arriba a la derecha, en la fila de botones del repositorio, está **Fork**. Es el de en medio de los tres:

```text
  raya-lucaria / fdd_o26                         Public

              ┌──────────┐ ┌────────┐ ┌────────┐
              │ ⊙ Watch  │ │ ⑂ Fork │ │ ☆ Star │
              └──────────┘ └───┬────┘ └────────┘
                               │
                          presiona éste
```

**Haz:** presiónalo. Se abre un formulario. **Déjalo todo como viene** y presiona *Create fork*:

```text
  Create a new fork

  Owner *                 Repository name *
  ┌──────────────────┐    ┌──────────────────────┐
  │ tu-login       ▾ │  / │ fdd_o26_tu-login     │
  └──────────────────┘    └──────────────────────┘
    ↑ tu cuenta             ↑ AQUÍ SÍ: guion bajo
                              y tu login

  Description  (opcional, déjalo vacío)

  ☑ Copy the main branch only
    ↑ déjala palomeada: es lo único que necesitas

               ┌───────────────┐
               │  Create fork  │
               └───────────────┘
```

Los dos campos que importan:

- **Owner** tiene que ser tu cuenta, no una organización.
- **Repository name**: bórralo y escribe `fdd_o26_` seguido de tu login. Si tu login es `butronand-png`, queda `fdd_o26_butronand-png`.

Ese sufijo es para ti: en tu lista de repositorios vas a tener el del curso y el tuyo, y con el nombre a secas cuesta distinguirlos. Todos los comandos de esta unidad ya cuentan con él.

**Deberías ver**, unos segundos después, el mismo repositorio bajo tu cuenta, y debajo del título una línea pequeña:

```text
  tu-login / fdd_o26_tu-login                    Public

  forked from raya-lucaria/fdd_o26
  ↑ ESTA línea es el fork. Sin ella es sólo una copia suelta
```

Esa línea es el "recuerdo" del que hablaba la página 1: es lo que le permite a GitHub ofrecerte después el botón de pull request. Si no aparece, no hiciste un fork.

**Compruébalo sin salir del navegador:** si la línea `forked from` está ahí, ya está.

> [!NOTE]
> **¿Ya lo habías forkeado antes?** Pasa cada semestre: alguien lo forkeó por curiosidad en agosto, o repite la materia. No lo forkees otra vez —GitHub no te deja tener dos con el mismo nombre—, actualízalo. En tu fork, GitHub te muestra `This branch is 47 commits behind raya-lucaria:main` y junto un botón **Sync fork → Update branch**. Presiónalo antes de seguir. El bloque A del ritual hace exactamente eso mismo, pero desde la terminal.

## Paso 2 · El resto, en un bloque

Con el fork ya hecho, lo demás es terminal. Todo lo que falta de esta página cabe aquí, y abajo se explica comando por comando.

```bash
# El fork del paso 1 tiene que estar hecho ANTES de esto.
cd ~/fdd/fdd_o26

# tu login EXACTO. No lo teclees
GHUSER=$(gh api user --jq .login) && echo "$GHUSER"

git remote -v                     # ahora: 2 líneas del curso
git remote rename origin upstream # el del curso: aquí BAJAS

# y origin pasa a ser TU fork: aquí SUBES
git remote add origin \
  git@github.com:$GHUSER/fdd_o26_$GHUSER.git

git remote -v                     # ahora: 4 líneas, 2 nombres

git switch main                   # párate en main
git fetch upstream                # baja. NO toca tus archivos
git merge upstream/main           # mételo. AQUÍ sí cambian
git push origin main              # tu fork, al día

# tu carpeta: el único lugar donde puedes escribir
mkdir -p estudiantes/$GHUSER
touch estudiantes/$GHUSER/.gitkeep
```

::: figure {#git-tres-repos title="Tres repositorios, y sólo en dos puedes escribir"}
![Tres repositorios y las flechas entre ellos: arriba a la izquierda el del curso llamado upstream que sólo se lee, arriba a la derecha tu fork llamado origin donde sí escribes, y abajo tu copia en el disco. Una flecha baja lo nuevo con git fetch, otra sube tu trabajo con git push, y una punteada representa el pull request](../_assets/git-tres-repos.svg)
:::

## Por qué existe el fork

Somos treinta personas y un repositorio. Si todos pudiéramos escribir en `raya-lucaria/fdd_o26`, cualquiera rompería la clase sin querer.

La solución no es repartir permisos: es que **nadie escriba ahí**. Cada quien trabaja en su copia y *propone* sus cambios. El fork es la copia; el pull request es la propuesta.

## Los comandos, uno por uno

### `$GHUSER`, tu login, guardado para siempre

Tu **login** es lo único de todo el flujo que cambia de persona a persona. Y no cambia nunca durante el semestre, así que **se guarda una vez y ya**.

Está en la barra de direcciones del fork que acabas de crear:

```text
  github.com/butronand-png/fdd_o26_butronand-png
             └────┬──────┘
              tu login, tal cual. Cópialo de ahí
```

Guárdalo en la configuración de tu shell, para que exista en toda terminal que abras de aquí a diciembre:

```bash
echo $SHELL      # ¿zsh o bash? esto te lo dice

# macOS suele traer zsh; Linux y WSL2 suelen traer bash.
# Corre SÓLO la línea de tu shell, con tu login de verdad:
echo 'export GHUSER=tu-login' >> ~/.zshrc
echo 'export GHUSER=tu-login' >> ~/.bashrc
```

Cierra la terminal, abre otra, y compruébalo:

```bash
echo "$GHUSER"   # tiene que imprimir tu login, no vacío
```

**Por qué en el perfil y no a secas:** una variable escrita en la terminal muere al cerrarla. Tu login no cambia en todo el semestre, así que no tiene por qué morirse. Puesto ahí, ningún comando de esta unidad te va a fallar por una variable vacía.

> [!NOTE]
> **¿Y si lo tecleo mal?** No se queda callado. Si el login está mal, la URL de tu fork está mal y `git push` responde `Repository not found` al primer intento. Y si tu carpeta queda con otro nombre, la revisión automática te lo dice **con el nombre exacto que esperaba**. Los dos errores se detectan solos, así que teclearlo es seguro.

Si tienes `gh` instalado te lo dice sin buscarlo. Es cómodo, no es obligatorio, y **`gh` no se instala en este curso**:

```bash
gh api user --jq .login
```


### `git remote rename` y `git remote add`

`git remote -v` **lista los repositorios remotos que tu copia conoce**: el apodo de cada uno y su URL. La `-v` es de *verbose*, y es lo que hace que muestre las URLs y no sólo los nombres. Cada remote aparece dos veces, una para bajar (`fetch`) y otra para subir (`push`).

Y un `remote` **es sólo un apodo para una URL**. `origin` no es palabra reservada de Git: es convención. Por eso se puede renombrar.

```text
git remote add origin \
  git@github.com:$GHUSER/fdd_o26_$GHUSER.git
           │     │     │   │          │   └── el repositorio
           │     │     │   │          └────── tu cuenta
           │     │     │   └───────────────── el servidor
           │     │     └──────────────── usuario SSH: "git"
           │     └────────────────────── el apodo, lo pones tú
           └──────────────────────────── agrega un remote
```

**Deberías ver**, al final:

```text
origin    git@github.com:tu-login/fdd_o26_tu-login.git (fetch)
origin    git@github.com:tu-login/fdd_o26_tu-login.git (push)
upstream  git@github.com:raya-lucaria/fdd_o26.git (fetch)
upstream  git@github.com:raya-lucaria/fdd_o26.git (push)
```

> [!NOTE]
> **Salida de rescate.** Si algo salió raro, borra y clona tu fork, que ya viene con el `origin` correcto:
> ```bash
> # PRIMERO comprueba que la variable no esté vacía. Si sale
> # vacía, NO sigas: el clone fallaría y ya borraste todo.
> echo "$GHUSER"
>
> cd ~/fdd && rm -rf fdd_o26
> git clone git@github.com:$GHUSER/fdd_o26_$GHUSER.git fdd_o26
> cd fdd_o26
> git remote add upstream \
>   git@github.com:raya-lucaria/fdd_o26.git
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
> Tu carpeta tiene que llamarse **idéntico** a tu login: mismas mayúsculas, mismos guiones. Por eso todos los comandos usan `$GHUSER` y no el teclado. El semestre pasado alguien la creó con guion bajo, y los logins de GitHub no admiten guion bajo.

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
