---
id: examen-github-enunciado
title: "Examen de GitHub: enunciado"
nav_title: "GitHub · enunciado"
summary: "El examen parcial de Git y GitHub tal como se repartió, versiones A y B, sin respuestas: leer un árbol de commits y escribir el ritual del curso en orden."
status: ready
estimated_time: 30m
tags: [examen, git, github, ritual, branches, anexo]
---

# Examen de GitHub: enunciado

**Anexo · Exámenes** · sin respuestas. La solución está en [[examen-github-solucion]].

**[Descargar el PDF](_assets/examen-github.pdf)**: las cuatro hojas tal como se imprimieron (A y B, dos caras cada una).

Dura **30 minutos** y vale **10 puntos**. Sin apuntes, formularios ni dispositivos electrónicos: sólo las hojas, pluma o lápiz y goma. Dos preguntas, una por cara.

## Versión A

### 1. Lee el árbol y diagnostica (3 puntos)

Un compañero terminó la tarea 07 y abrió su pull request. **Ese pull request sigue abierto: nadie se lo ha mergeado todavía**. Sin moverse de `tarea-07-git`, creó desde ahí la rama de la tarea 08 y trabajó en ella. Contesta con tus palabras: qué está mal, qué está bien, cómo se evita. No comandos.

```text
                  D---E    tarea-08-datacamp-intro
                 /
         A---B---C         tarea-07-git  (PR abierto)
        /
o---o---o                  main  =  upstream/main
```

**a)** ¿Qué archivos va a listar el pull request de `tarea-08-datacamp-intro`? Describe qué aparece y por qué aparece. No escribas comandos.

**b)** Di **una cosa que hizo bien** y **una que hizo mal**. La que hizo mal, explícala en términos de **dónde nació la rama**.

**c)** ¿Cómo se evita? Explica por qué eso lo resuelve.

**d)** Si le mergean la tarea 07 **antes** de que abra el segundo pull request, ¿cambia lo que ese pull request contiene? Justifica.

### 2. El ritual, en orden (7 puntos)

Los ocho pasos están **desordenados**. Uno ocurre una sola vez en el semestre; los otros siete, en cada entrega. Para cada renglón escribe:

- **Orden**: el número que le toca (1 a 8);
- **Qué hace y por qué**: qué logra, y qué se rompe si falta;
- **Comandos**: los comandos exactos, en orden. Si no hay comando, dilo y describe qué se hace.

Usa la rama `tarea-08-imagen` y su carpeta `08_contenedores/` como ejemplo.

| Orden | Paso | Qué hace y por qué | Comandos |
|---|---|---|---|
|   | Crear tu carpeta de la unidad y copiar ahí el material del curso. |   |   |
|   | Proponerle tu trabajo al curso desde el navegador. |   |   |
|   | Traerte lo que el curso publicó, sin tocar todavía tus archivos. |   |   |
|   | Conectar tu copia con el repositorio del curso. (Una sola vez en el semestre.) |   |   |
|   | Revisar qué cambió y apartar sólo lo tuyo, por ruta. |   |   |
|   | Guardar lo apartado y subir tu rama a tu fork. |   |   |
|   | Incorporar eso a tu main y dejar tu fork al día. |   |   |
|   | Crear la rama de esta tarea y moverte a ella. |   |   |

## Versión B

### 1. Lee el árbol y diagnostica (3 puntos)

Un compañero hizo su fork el primer día y creó de inmediato la rama de la tarea. Mientras él trabajaba, yo corregí `codigo/docker/certificaciones.md` y le agregué una sección: ése es el commit **R**. Él copió la plantilla el primer día y no volvió a sincronizar. Contesta con tus palabras: qué está mal, qué está bien, cómo se evita. No comandos.

```text
o---o---o---o---P---Q---R      upstream/main
            |
            +---X---Y          tarea-08-datacamp-intro
            |
            main, origin/main
```

**a)** Su `certificaciones.md` no tiene la sección nueva, y él nunca la borró. Explica por qué, en términos de **dónde nació su rama**.

**b)** Di **dos cosas que hizo bien**. Sí las hay: quien sólo busque errores se va a quedar corto.

**c)** Entrega así. ¿Se puede mergear su pull request? ¿Qué problema trae aunque se pueda? ¿Cómo se evita?

**d)** En vez de haber sincronizado antes, corre `git merge upstream/main` **dentro** de su rama de entrega. ¿Se actualiza su copia del archivo? ¿Cambia lo que el pull request me muestra? Justifica las dos.

### 2. El ritual, en orden (7 puntos)

Las mismas instrucciones que en la versión A; los pasos vienen en otro desorden.

| Orden | Paso | Qué hace y por qué | Comandos |
|---|---|---|---|
|   | Revisar qué cambió y apartar sólo lo tuyo, por ruta. |   |   |
|   | Incorporar eso a tu main y dejar tu fork al día. |   |   |
|   | Guardar lo apartado y subir tu rama a tu fork. |   |   |
|   | Crear tu carpeta de la unidad y copiar ahí el material del curso. |   |   |
|   | Proponerle tu trabajo al curso desde el navegador. |   |   |
|   | Crear la rama de esta tarea y moverte a ella. |   |   |
|   | Traerte lo que el curso publicó, sin tocar todavía tus archivos. |   |   |
|   | Conectar tu copia con el repositorio del curso. (Una sola vez en el semestre.) |   |   |

Cuando termines, califícate con [[examen-github-solucion]].
