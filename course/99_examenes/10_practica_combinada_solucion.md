---
id: practica-combinada-solucion
title: "Práctica combinada: clave"
nav_title: "Combinada · clave"
summary: "Las respuestas de la práctica combinada, fila por fila y comprobadas corriendo todo: fast-forward contra commit de merge, el conflicto, un script con marcadores dentro de una imagen, y lo que el build copia de tu disco aunque no esté commiteado."
status: ready
estimated_time: 20m
tags: [practica, solucion, git, merge, conflictos, bash, docker, anexo]
prerequisites: [practica-combinada]
---

# Práctica combinada: clave

**Anexo · Exámenes** · el ejercicio está en [[practica-combinada]]. Resuélvelo antes de leer esto.

Todo se comprobó creando el repo, las tres ramas y corriendo cada fila con Git 2.34, bash 5.2 y Docker 29.6.

La idea que atraviesa el ejercicio: **Git, bash y Docker no se avisan entre sí**. Git guarda commits, `docker build` copia lo que hay en tu disco, y bash corre lo que le den. Cada respuesta difícil sale de preguntarte cuál de los tres está mirando qué.

## Parte 1 · Antes de mezclar nada

**a)** `filas: 4`. El archivo tiene cuatro renglones, y `wc -l < "$archivo"` los cuenta.

**b)** Imprime `no existe: datos/mayo.csv` y luego `1`. La prueba `[[ ! -f … ]]` es verdadera porque el archivo no existe. El mensaje va a stderr (`>&2`) y `exit 1` termina el script con código 1. `echo $?` imprime el código de salida del último comando, y 1 significa «algo falló».

**c)** `no existe: datos/ventas.csv`. El archivo existe **en tu carpeta**, pero el Dockerfile de B sólo copia `contar.sh`: dentro de la imagen no hay `datos/`. El contenedor sólo ve lo que la imagen trae o lo que le montes. El código de salida del contenedor también es 1: `docker run` lo devuelve tal cual.

**d)** `docker run --rm -v "$(pwd)/datos":/r/datos rep:0` imprime `filas: 4`. El montaje pone tu carpeta en `/r/datos`, justo donde el `CMD` busca `datos/ventas.csv`, porque el `WORKDIR` es `/r`.

**Repasa:** [[variables-comillas-y-salida]] y [[lab-con-volumen]].

## Parte 2 · La secuencia

### Fila 1 · Fast-forward

`main` sigue en B, y `filtro` es B más un commit. No hay nada que mezclar: Git sólo **adelanta** la etiqueta `main` hasta F. No crea ningún commit nuevo. Git lo dice con la palabra `Fast-forward`.

### Fila 2 · Commit de merge

Ahora `main` está en F, e `imagen` nació en B: las dos ramas ya se separaron, y cada una tiene un commit que la otra no. Git tiene que **juntarlas**, y para eso crea un commit nuevo con dos padres (`Merge made by the 'ort' strategy`). No hay conflicto: F tocó `contar.sh` e I tocó el `Dockerfile`.

### Fila 3 · `filas: 2`

`main` ya tiene las dos cosas: el `grep -c MX` de F y el `COPY datos/ datos/` de I. La imagen trae los datos, y hay dos renglones con `MX`. Todavía dice `filas:`, porque `titulo` no se ha mezclado.

### Fila 4 · `filas: 2` · `filas: 3`

- **Primer run:** la imagen guardó los datos **del momento del build**. Agregar un renglón a tu disco no cambia la imagen.
- **Segundo run:** el montaje tapa el `/r/datos` de la imagen con tu carpeta, que ya tiene el tercer `MX`.

### Fila 5 · Conflicto

Git responde:

```text
Auto-merging contar.sh
CONFLICT (content): Merge conflict in contar.sh
Automatic merge failed; fix conflicts and then commit the result.
```

F y T cambiaron **la misma línea 6** de forma distinta desde B, y Git no puede elegir por ti.

**Sí te deja intentarlo** con `datos/ventas.csv` modificado sin commit, porque `titulo` no toca ese archivo: el merge no tiene que pisarlo. Si `titulo` lo cambiara, Git se negaría, igual que con `git switch`.

`git status --short` muestra ahora `UU contar.sh` (en conflicto) y ` M datos/ventas.csv` (tu cambio, intacto).

### Fila 6 · Los marcadores

```text
<<<<<<< HEAD
printf 'filas: %s\n' "$(grep -c MX "$archivo")"
=======
printf 'total: %s\n' "$(wc -l < "$archivo")"
>>>>>>> titulo
```

`HEAD` es **la rama donde estás parado**: `main`, que ya traía el `grep` de F. Lo de abajo del `=======` es lo que viene de `titulo`. Las líneas 1 a 5 no aparecen en conflicto, porque nadie las cambió.

**Repasa:** [[branches-y-merge]].

### Fila 7 · El build sí, el script no, código 2

- **El build termina bien.** `COPY` copia bytes y no sabe que el archivo tiene marcadores.
- **El run** imprime:

  ```text
  contar.sh: line 6: syntax error near unexpected token `<<<'
  contar.sh: line 6: `<<<<<<< HEAD'
  ```

- **`echo $?` da `2`**, el código con que bash señala un error de sintaxis.

Ni Git ni Docker te impiden empaquetar un archivo a medio resolver: el único que se queja es bash, y sólo cuando lo corre.

### Fila 8 · Los dos cambios

```bash
printf 'total: %s\n' "$(grep -c MX "$archivo")"
```

El texto `total:` de T con el conteo `grep -c MX` de F. Se borran **las tres líneas de marcadores** y se deja una sola línea 6. `git add` le dice a Git «ya lo resolví», y `git commit` crea el commit de merge.

`git status --short` muestra sólo ` M datos/ventas.csv`: el conflicto quedó guardado, y tu renglón extra sigue sin commit.

**También vale** cualquier forma que deje una sola línea correcta. Por ejemplo, editar en VS Code con *Accept Both Changes* y luego borrar la línea sobrante.

### Fila 9 · Caché

| Paso | Resultado | Por qué |
|---|---|---|
| `FROM`, `WORKDIR /r` | caché | No cambiaron |
| `COPY contar.sh .` | **se rehace** | `contar.sh` cambió: ahora dice `total:` |
| `COPY datos/ datos/` | **se rehace** | Viene después de una capa que cambió, y además `datos/` cambió en la fila 4 |

### Fila 10 · `total: 3`

`docker build` copia **lo que hay en tu disco**, no lo que hay en el último commit. El renglón `MX,1` de la fila 4 nunca se commiteó, pero estaba en `datos/ventas.csv` al construir, así que entró a la imagen.

Ésta es la trampa del ejercicio: una imagen puede contener cambios que nadie más tiene. Si otra persona clona el repo y construye, obtiene `total: 2`.

**Repasa:** [[capas-y-cache]] y [[rutas-en-docker]].

### Fila 11 · Dos commits de merge

```text
*   Merge branch 'titulo'
|\
| * titulo total
* |   Merge branch 'imagen'
|\ \
| * | datos en la imagen
| |/
* / solo MX
|/
* base
```

Hay **dos** commits de merge, el de `imagen` y el de `titulo`. `filtro` entró por fast-forward: F quedó en la línea de `main` sin commit de merge, porque no había nada que juntar.

## Parte 3 · Las comillas

**a)** Imprime:

```text
grep: datos/ventas: No such file or directory
grep: mayo.csv: No such file or directory
total:
```

`echo $?` da **`0`**.

Sin comillas, bash parte el valor de `$archivo` en el espacio, y `grep` recibe **dos** nombres que no existen. La prueba de la línea 2 sí tenía comillas y pasó, porque el archivo existe. El `printf` de la línea 6 funciona y es el último comando, así que el script termina con 0.

**Es peligroso** porque cualquier cosa que revise el código de salida, un `&&` o un pipeline de datos, cree que todo salió bien y sigue con un `total:` vacío.

**b)** `no existe: datos/ventas`. Sin comillas al llamarlo, `$1` es `datos/ventas` y `$2` es `mayo.csv`; el script sólo mira `$1`. Las comillas importan en los dos lados: al llamar y adentro del script.

**c)** **Git**, desde la fila 5: el mensaje `CONFLICT`, y después `git status`, que marca el archivo con `UU` (*both modified*). Docker no lo detecta, y bash sólo cuando ya es tarde, al correr.

**Repasa:** [[variables-comillas-y-salida]] y [[como-lee-bash]].
