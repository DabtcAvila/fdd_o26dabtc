---
id: practica-combinada
title: "Práctica combinada: Git, bash y Docker"
nav_title: "Combinada · práctica"
summary: "Un solo repo con un script de bash, un Dockerfile y datos; tres ramas que se mezclan con fast-forward, con commit de merge y con conflicto; y en medio, builds y corridas cuyo resultado depende de qué se mezcló."
status: ready
estimated_time: 45m
tags: [practica, git, merge, conflictos, bash, docker, anexo]
prerequisites: [practica-github, practica-docker]
---

# Práctica combinada: Git, bash y Docker

**Anexo · Exámenes** · un ejercicio que junta las tres unidades. La clave está en [[practica-combinada-solucion]].

**[Descargar el PDF](_assets/practica-combinada.pdf)** para resolverla en papel.

En los exámenes cada herramienta se preguntó sola. En la práctica se usan juntas: el script vive en Git, el Dockerfile lo copia, y lo que imprime el contenedor depende de qué ramas mezclaste y de qué había en tu disco al construir. Contesta primero sin computadora; después puedes reproducirlo todo y comparar.

## El repo

`reporte/` cuenta ventas. En `main` hay un solo commit, **B**, con esto:

```text
reporte/          ← estás aquí
├── Dockerfile
├── contar.sh
└── datos/
    └── ventas.csv
```

`contar.sh`, con sus números de línea:

```text
1  archivo="$1"
2  if [[ ! -f "$archivo" ]]; then
3      printf 'no existe: %s\n' "$archivo" >&2
4      exit 1
5  fi
6  printf 'filas: %s\n' "$(wc -l < "$archivo")"
```

`Dockerfile` (la imagen `bash:5.2` es Alpine con bash instalado):

```dockerfile
FROM bash:5.2
WORKDIR /r
COPY contar.sh .
CMD ["bash", "contar.sh", "datos/ventas.csv"]
```

`datos/ventas.csv`, cuatro renglones:

```text
MX,10
US,5
MX,7
CA,3
```

Tres personas crearon una rama cada una, todas desde B, con un commit cada una:

```text
   +---F          filtro
   |
   +---T          titulo
   |
   +---I          imagen
   |
   B              main
```

| Rama | Commit | Qué cambia |
|---|---|---|
| `filtro` | F | `contar.sh`, línea 6: `wc -l < "$archivo"` pasa a `grep -c MX "$archivo"` |
| `titulo` | T | `contar.sh`, línea 6: `'filas: %s\n'` pasa a `'total: %s\n'` |
| `imagen` | I | `Dockerfile`: agrega `COPY datos/ datos/` después de `COPY contar.sh .` |

`grep -c MX` cuenta los renglones que contienen `MX`. `wc -l` cuenta todos los renglones.

## Parte 1 · Antes de mezclar nada

Estás en `main`, con B tal cual.

**a)** ¿Qué imprime `bash contar.sh datos/ventas.csv` en tu máquina?

**b)** ¿Qué imprime `bash contar.sh datos/mayo.csv`, y qué imprime justo después `echo $?`? ¿Por qué ese número?

**c)** Corres `docker build -t rep:0 .` y luego `docker run --rm rep:0`. ¿Qué imprime, y por qué, si `datos/ventas.csv` sí existe en tu carpeta?

**d)** Escribe un `docker run` que haga funcionar `rep:0` sin reconstruir la imagen. ¿Qué imprime?

## Parte 2 · La secuencia

Los comandos se corren **en orden**, todos desde `reporte/` y empezando en `main`. Cada fila parte de lo que dejó la anterior. Contesta corto.

| # | Comandos (en orden) | Pregunta |
|---|---|---|
| 1 | `git merge filtro` | ¿Fast-forward o commit de merge? ¿Por qué? |
| 2 | `git merge imagen` | ¿Fast-forward o commit de merge? ¿Por qué ahora es distinto? |
| 3 | `docker build -t rep:1 .` ; `docker run --rm rep:1` | ¿Qué imprime el run? |
| 4 | `echo "MX,1" >> datos/ventas.csv` ; `docker run --rm rep:1` ; `docker run --rm -v "$(pwd)/datos":/r/datos rep:1` | ¿Qué imprime el primer run? ¿Y el segundo? |
| 5 | `git merge titulo` | ¿Qué responde Git? ¿Te deja intentarlo aunque `datos/ventas.csv` tiene un cambio sin commit? |
| 6 | `cat contar.sh` | Escribe cómo se ven ahora las últimas líneas. ¿Cuál de los dos lados es `HEAD`? |
| 7 | `docker build -t rep:2 .` ; `docker run --rm -v "$(pwd)/datos":/r/datos rep:2` ; `echo $?` | ¿El build termina bien? ¿Qué imprime el run, y qué número da `echo $?`? |
| 8 | `# editas contar.sh y resuelves el conflicto` ; `git add contar.sh` ; `git commit` | Te quedas con **los dos cambios**. Escribe la línea 6 resuelta. ¿Qué muestra después `git status --short`? |
| 9 | `docker build -t rep:3 .` | ¿Qué pasos salen de la caché y cuáles se rehacen? |
| 10 | `docker run --rm rep:3` | ¿Imprime `total: 2` o `total: 3`? ¿Por qué, si el cambio de la fila 4 nunca se commiteó? |
| 11 | `git log --oneline --graph` | ¿Cuántos commits de merge tiene `main`? ¿Por qué no hay uno para `filtro`? |

Las filas 4 y 7 tienen más de una casilla.

## Parte 3 · Las comillas

**a)** Alguien «simplifica» la línea 6 del `contar.sh` ya resuelto y le quita las comillas a la variable: `grep -c MX $archivo`. Luego corre, en su máquina, `bash contar.sh "datos/ventas mayo.csv"` sobre un archivo que sí existe con ese nombre. ¿Qué imprime? ¿Qué da `echo $?` justo después? ¿Por qué ese número es peligroso?

**b)** Con el script correcto, con comillas, alguien corre `bash contar.sh datos/ventas mayo.csv`, sin comillas al llamarlo. ¿Qué imprime y por qué?

**c)** En la parte 2, ¿qué herramienta te habría avisado del conflicto antes de construir la imagen de la fila 7: Git, bash o Docker? ¿Qué comando lo muestra?

Cuando termines, califícate con [[practica-combinada-solucion]].
