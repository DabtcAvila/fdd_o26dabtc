---
id: el-gil
title: "El GIL"
nav_title: "El GIL"
summary: "Dentro de un intérprete (normalmente hay uno por proceso), un solo hilo a la vez ejecuta código Python. Por eso los hilos aceleran un programa que espera, pero casi no a uno que calcula."
status: ready
estimated_time: 15m
tags: [gil, hilos, procesos, concurrencia, free-threading, multiprocessing]
prerequisites: [nombres-y-objetos]
---

# El GIL

**Página 3 de 5 · Python por dentro**

Meta: saber cuándo los hilos aceleran tu programa y cuándo no.

**En `revisa_esto.py`:** esto explica el síntoma 3.

| Término | Qué es | Lo ves con |
|---|---|---|
| **proceso** | Un programa corriendo, con su propia memoria | `ps` |
| **hilo** | Una línea de ejecución dentro de un proceso; comparte la memoria del proceso | el `ThreadPoolExecutor` de `gil.py` |
| **CPU lógica** | Cada unidad que el sistema puede poner a ejecutar algo al mismo tiempo; con *hyperthreading* hay dos por núcleo físico | `nproc` (en macOS, `sysctl -n hw.ncpu`) |

## En corto

- **Dentro de un intérprete (normalmente hay uno por proceso), un solo hilo a la vez ejecuta código Python**: eso es el GIL (*Global Interpreter Lock*, el candado global del intérprete).
- **Si tu programa calcula en Python, usa procesos; si espera, hilos.**
- **Desde 3.14 (2025) hay un Python sin GIL**, soportado y opcional: `3.14t`.

## Cuatro hilos que calculan tardan casi lo mismo que uno

Primero, cuántas CPUs lógicas tienes. El lab lanza 4 trabajos a la vez. Si `nproc` da menos de 4, tus cifras de "4 procesos" saldrán más lentas; la lección no cambia.

**Haz (terminal, en por_dentro/):**

```bash
nproc
```

**Qué hace cada pieza:**

- `nproc` — imprime cuántas CPUs lógicas puede usar tu programa. En macOS no existe: usa `sysctl -n hw.ncpu`.

**Deberías ver:** un número; en la máquina del profesor,

```text
8
```

Ahora el lab. `gil.py` suma 10 millones de números cuatro veces, de tres formas, y luego hace cuatro esperas de 1 s con hilos. Tarda unos 8 s en la máquina del profesor: no lo interrumpas.

**Haz (terminal, en por_dentro/):**

```bash
uv run gil.py
```

**Qué hace cada pieza:**

- `uv run` — corre el archivo con el Python del `.venv/` de `por_dentro/`, el 3.14 que fija `.python-version` (lo viste en [[ambientes-python]]).
- `gil.py` — el lab: mide «uno tras otro», «4 hilos» y «4 procesos» para un trabajo que calcula, y «4 hilos» para uno que espera.

**Deberías ver:** la salida real en la máquina del profesor (8 CPUs lógicas; en `3.14.0`, el último número puede ser otro).

```text
Python 3.14.0 · GIL activo
calcula, uno tras otro    3.02 s
calcula, 4 hilos          2.63 s
calcula, 4 procesos       1.44 s
espera, 4 hilos           1.00 s
```

- **4 hilos calculando: 2.63 s contra 3.02 s.** Casi lo mismo que uno tras otro: los hilos se turnan el GIL.
- 4 procesos: 1.44 s. Cada proceso tiene su propio GIL y corre en otra CPU.
- **Cuatro esperas de 1 s tardan 1.00 s**, no 4: mientras un hilo espera, suelta el GIL.

Tus cifras cambian con la carga de tu máquina y entre corridas: lo que no cambia es que 4 hilos no bajan a un cuarto y 4 procesos sí bajan (aquí, a menos de la mitad).

**Éste es el síntoma 3** de `revisa_esto.py`: "con hilos" tarda casi lo mismo que "sin hilos", aunque el comentario promete 4× más rápido.

¿Por qué se turnan los hilos? Por esto:

Cada objeto lleva un **contador de referencias**: cuántos nombres, elementos de listas o atributos lo apuntan. Cuando llega a cero, CPython borra el objeto. Si dos hilos cambian ese contador a la vez, queda mal: un objeto se borra en uso o nunca se borra.

El GIL protege ese contador y el resto del estado interno de CPython. Mientras un hilo espera al sistema operativo (red, disco, `time.sleep`), otro hilo puede ejecutar Python.

::: figure {#py-gil title="Tres formas de correr cuatro trabajos"}
![Tres carriles sobre un eje de tiempo. Arriba, con GIL: cuatro hilos de un mismo proceso se turnan, sólo uno ejecuta Python en cada instante, y el total dura casi lo mismo que hacer los cuatro trabajos uno tras otro. En medio, sin GIL (3.14t): los cuatro hilos ejecutan al mismo tiempo y el total se acorta. Abajo, cuatro procesos, cada uno con su propio GIL, también ejecutan al mismo tiempo.](../_assets/py-gil.svg)
:::

La columna sin GIL ya está medida, con el mismo `gil.py` en `3.14t` (cómo correrla está en la lectura, abajo):

| | con GIL (3.14) | sin GIL (3.14t) |
|---|---:|---:|
| calcula, uno tras otro | 3.02 s | 2.76 s |
| calcula, 4 hilos | **2.63 s** | **1.22 s** |
| calcula, 4 procesos | 1.44 s | 1.29 s |
| espera, 4 hilos | 1.00 s | 1.00 s |

- Sin GIL, 4 hilos calculando sí bajan a menos de la mitad: el único cambio es el GIL.
- Esperar da lo mismo con o sin GIL: esperar nunca necesitó el GIL.

## Todo script que lanza procesos lleva su guarda

Al final de `gil.py` está la línea `if __name__ == "__main__":`. **Todo script que lanza procesos la lleva**: el bloque debajo de ella sólo corre cuando tú ejecutas este archivo, no cuando otro proceso lo importa. Sin ella, en 3.14 el programa se repite y termina en un `RuntimeError`. Por qué, en la lectura.

— Hasta aquí en clase; lo demás es lectura —

## Lectura · `__name__` a fondo

`__name__` es una variable que Python le pone a cada archivo: vale `"__main__"` en el archivo que corres, y otro valor cuando el archivo se importa. La guarda ejecuta su bloque sólo en el primer caso.

**El método de arranque** es cómo crea Python un proceso nuevo. En Linux, 3.14 cambió el de por defecto de `fork` a `forkserver`; en macOS es `spawn` desde 3.8 (2019). Con esos dos, el proceso nuevo **vuelve a importar tu archivo**, con `__name__` igual a `"__mp_main__"`.

Sin guarda, cada proceso nuevo vuelve a correr todo el script y quiere lanzar sus propios procesos; Python lo detiene. Ésta es la salida real de una copia de `gil.py` con la guarda cambiada por `if True:`, corrida en 3.14 (recortada con `…`; cuántas veces se repite el encabezado varía):

```text
Python 3.14.0 · GIL activo
calcula, uno tras otro    3.10 s
calcula, 4 hilos          3.87 s
Python 3.14.0 · GIL activo
calcula, uno tras otro    6.40 s
calcula, 4 hilos          5.89 s
…
RuntimeError: 
        An attempt has been made to start a new process before the
        current process has finished its bootstrapping phase.
…
concurrent.futures.process.BrokenProcessPool: A process in the process pool was terminated abruptly while the future was running or pending.
```

- El encabezado se repite: cada proceso hijo volvió a correr el script desde arriba.
- El `RuntimeError` sale en el hijo; el padre sólo ve que su grupo de procesos se rompió (`BrokenProcessPool`).
- En 3.13 en Linux no se nota, porque el método por defecto ahí es `fork`, que no reimporta. Pon la guarda igual: tu código también corre en macOS y en 3.14.

## Lectura · Tabla de decisión

| Tu programa… | Usa | Por qué |
|---|---|---|
| calcula en Python puro | procesos | cada proceso trae su GIL |
| calcula con numpy (la librería de cálculo numérico, escrita en C) | numpy, sin hilos extra | una operación vectorizada ya corre en C; sus productos de matrices y su álgebra lineal usan varios núcleos por su cuenta; hilos encima rara vez ayudan |
| espera red, disco o una API | hilos | quien espera suelta el GIL |
| corre en el Python sin GIL (3.14t) y el GIL sigue apagado después de tus imports | hilos, también para calcular | no hay GIL que turnar; una librería que no lo soporta puede volver a encenderlo al importarse |

Con qué se escribe cada fila:

- Procesos: `ProcessPoolExecutor`; hilos: `ThreadPoolExecutor` (los dos de `concurrent.futures`).
- En numpy, el producto de matrices es `@` y el álgebra lineal vive en `np.linalg`.
- `sys._is_gil_enabled()` da `False` si el GIL está apagado.
- Desde 3.14, `InterpreterPoolExecutor` (PEP 734, 2025) corre varios intérpretes en un proceso, cada uno con su GIL.

## Lectura · En casa: la columna sin GIL

**Haz (terminal, en por_dentro/):**

```bash
uv run --no-project --python 3.14t gil.py
```

**Qué hace cada pieza:**

- `--python 3.14t` — pide el Python 3.14 sin GIL; si no lo tienes, uv lo descarga.
- `--no-project` — corre el archivo **sin el proyecto**: no usa ni toca el `.venv/` de `por_dentro/`.

**Sin `--no-project`, uv reemplaza tu `.venv/` por uno sin GIL** y el notebook queda con otro Python. Si te pasó, `uv sync` solo no lo arregla: en `por_dentro/` borra el ambiente con `rm -rf .venv` y luego corre `uv sync`, que lo recrea con el 3.14 de `.python-version`.

**Deberías ver:** la primera línea dice `GIL apagado`, y «calcula, 4 hilos» baja a menos de la mitad de «uno tras otro».

**Al revisar código de IA, busca:**

- `ThreadPoolExecutor(` alrededor de una función que sólo calcula en Python: con GIL, no acelera.
- `ProcessPoolExecutor` sin `if __name__ == "__main__":` al final del archivo.

**Al pedírselo a la IA, dile:**

- «El trabajo calcula» o «el trabajo espera una API»: decide entre procesos e hilos.
- «Uso Python 3.14 con GIL.»

::: problem {#py-dentro-hilos title="Ocho CSV con hilos, y tarda lo mismo"}
Paralelizaste con hilos la limpieza de 8 CSV y tarda lo mismo que uno tras otro. ¿Qué preguntas antes de cambiar nada?
:::

::: hint {of="py-dentro-hilos"}
Mientras corre, ¿tu programa está calculando o esperando?
:::

::: answer {of="py-dentro-hilos"}
- Si calcula en Python y hay GIL, los hilos se turnan: no hay ganancia.
- Arreglo: procesos (`ProcessPoolExecutor`, con su guarda) o `3.14t`.
- Si espera (disco, red), los hilos sí sirven: la lentitud tiene otra causa; búscala.
:::

Sigue con [[lo-que-escribe-la-ia]]: lo que la IA escribe sin avisar, empezando por qué cuenta como falso.

> [!NOTE]
> **Si sólo recuerdas una cosa:** con GIL, los hilos sólo ayudan cuando tu programa espera.
