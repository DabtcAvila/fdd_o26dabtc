---
id: github-en-corto
title: "GitHub, en corto"
nav_title: "GitHub, en corto"
summary: "Qué le agrega GitHub a Git, dicho en una tabla, y las tres comprobaciones que te dicen si ya puedes seguir o te falta setup."
status: ready
estimated_time: 10m
tags: [github, git, remote, setup, comprobacion]
prerequisites: [seccion-github]
---

# GitHub, en corto

**GitHub · página 1 de 6** · 10 min

Meta: comprobar en tres comandos que tu máquina está lista.

## En corto

- Git corre en tu máquina. **GitHub es un servidor donde se guardan repositorios de Git**, con cosas encima que Git no tiene.
- La sección pasada fue sin conexión. Ésta es toda red.
- Hoy no se instala nada: se comprueba y se trabaja.
- Dos comprobaciones obligatorias y una opcional.

## Corre esto antes de leer nada más

```bash
# 1. ¿GitHub me reconoce?
ssh -T git@github.com

# 2. ¿tengo el repositorio del curso en el disco?
cd ~/fdd/fdd_o26 && git log --oneline -3

# 3. opcional: ¿tengo gh? no se instala en este curso
gh api user --jq .login
```

Las dos primeras son obligatorias. **La tercera no**: `gh` es el programa de GitHub para la terminal, es cómodo y no lo necesitas. Si responde `command not found`, sigue igual — la página 2 te da la alternativa.

::: table {#git-compuertas title="Qué hacer con cada resultado"}

| Comando | Bien si | Si falla, ve a |
|---|---|---|
| `ssh -T` | dice `Hi <tu-usuario>!` | [[cuenta-y-llave|Apéndice: cuenta y llave]] |
| `git log` | te muestra tres commits | [[clonar-y-actualizar|Apéndice: clonar]] |
| `gh api user` | imprime una palabra | nada, es opcional; la página 2 da la alternativa |

:::

> [!NOTE]
> El mensaje de `ssh -T` **también** dice que GitHub no da acceso a una shell. Eso es parte de la respuesta correcta, no un error.

## Git vs GitHub, de una vez

Git es un programa, de 2005. GitHub es una empresa, de 2008, que Microsoft compró en 2018.

::: table {#git-vs-github title="Qué es de cada uno"}

| Es de Git | Es de GitHub |
|---|---|
| `commit`, `branch`, `merge`, `stash` | El **fork** |
| `push`, `pull`, `fetch`, `remote` | El **pull request** |
| El hash, la historia, la carpeta `.git` | Los issues y la revisión de código |
| Funciona sin internet | Actions y Pages |

:::

La columna izquierda existiría igual si GitHub cerrara mañana. La derecha no.

Y el matiz que más confunde: **Git sí sabe clonar.** Lo que agrega GitHub es hacer ese clone *en su servidor, dentro de tu cuenta*, y **recordar de dónde vino**. Ese recuerdo es lo que hace posible el pull request.

## El orden de la clase

```text
  1. GitHub, en corto   ← estás aquí
  2. El fork            → tu copia y tus dos remotes
  3. Branches           → practicarlas hasta que no den miedo
  4. Tu espejo          → dónde va cada archivo, y por qué
  5. El ritual          → los cuatro bloques del flujo
  6. El pull request    → la entrega de verdad
```

Al final de la página 6 vas a tener un pull request abierto. **Ése es el formato de todas las entregas de aquí a diciembre.**

> [!NOTE]
> **Si sólo recuerdas una cosa:** Git es el programa, GitHub es el servidor. El fork y el pull request son de GitHub; todo lo demás que aprendiste es de Git.

## Cierre

Con las tres comprobaciones en verde, sigue con [[el-fork|El fork y tus dos remotes]].
