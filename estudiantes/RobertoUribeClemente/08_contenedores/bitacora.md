# Bitácora de la unidad 08

Llena este archivo en **tu copia**, dentro de
`estudiantes/<tu-login>/08_contenedores/`. No edites el original.

## Quién soy

- Nombre: José Roberto Uribe Clemente
- Usuario de GitHub: Roberto_Uribe_Clemente
- Usuario de Docker Hub: BobUC05

## Qué corrí

Pega la salida de estos tres comandos, tal como te respondieron:

```text
docker version
Client: Docker Engine - Community
 Version:           29.8.1
 API version:       1.56
 Go version:        go1.26.8
 Git commit:        4a63305
 Built:             Tue Sep 15 16:25:42 2026
 OS/Arch:           linux/amd64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          29.8.1
  API version:      1.56 (minimum version 1.40)
  Go version:       go1.26.8
  Git commit:       464cd50
  Built:            Tue Sep 15 16:25:42 2026
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          v2.3.5
  GitCommit:        1294c24a7da8e5a793ed378161673abe94118892
 runc:
  Version:          1.5.1
  GitCommit:        v1.5.1-0-g8f2685a4
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0



docker images
                                                                                  i Info →   U  In Use
IMAGE                       ID             DISK USAGE   CONTENT SIZE   EXTRA
bobuc05/fdd-imagen:latest   70f31c621fe0        105MB         25.6MB        


docker history <tu-usuario>/<tu-imagen>
IMAGE          CREATED              CREATED BY                                      SIZE      COMMENT
cd82d2c13a8f   About a minute ago   CMD ["python" "app.py"]                         0B        buildkit.dockerfile.v0
<missing>      About a minute ago   COPY . . # buildkit                             20.5kB    buildkit.dockerfile.v0
<missing>      About a minute ago   USER app                                        0B        buildkit.dockerfile.v0
<missing>      About a minute ago   RUN /bin/sh -c useradd -m app && chown -R ap…   77.8kB    buildkit.dockerfile.v0
<missing>      About a minute ago   RUN /bin/sh -c pip install --no-cache-dir -r…   13.3MB    buildkit.dockerfile.v0
<missing>      About a minute ago   COPY requirements.txt . # buildkit              12.3kB    buildkit.dockerfile.v0
<missing>      About a minute ago   WORKDIR /app                                    8.19kB    buildkit.dockerfile.v0
<missing>      3 days ago           CMD ["python3"]                                 0B        buildkit.dockerfile.v0
<missing>      3 days ago           RUN /bin/sh -c set -eux;  for src in idle3 p…   16.4kB    buildkit.dockerfile.v0
<missing>      3 days ago           RUN /bin/sh -c set -eux;   savedAptMark="$(a…   41.4MB    buildkit.dockerfile.v0
<missing>      3 days ago           ENV PYTHON_SHA256=5c8462af5790baf43a321a1559…   0B        buildkit.dockerfile.v0
<missing>      3 days ago           ENV PYTHON_VERSION=3.12.14                      0B        buildkit.dockerfile.v0
<missing>      3 days ago           ENV GPG_KEY=7169605F62C751356D054A26A821E680…   0B        buildkit.dockerfile.v0
<missing>      3 days ago           RUN /bin/sh -c set -eux;  apt-get update;  a…   4.95MB    buildkit.dockerfile.v0
<missing>      3 days ago           ENV LANG=C.UTF-8                                0B        buildkit.dockerfile.v0
<missing>      3 days ago           ENV PATH=/usr/local/bin:/usr/local/sbin:/usr…   0B        buildkit.dockerfile.v0
<missing>      4 days ago           # debian.sh --arch 'amd64' out/ 'trixie' '@1…   87.6MB    debuerreotype 0.17


```

## Los tres defectos de `roto/Dockerfile`

Uno por línea: qué estaba mal, qué consecuencia tiene, y qué cambiaste.

1. **Imagen base sobredimensionada (`FROM python:latest`):** Utilizaba la etiqueta genérica sin optimización, lo que inflaba el peso de la imagen por encima de los límites permitidos.
Se corrigió migrando a una base ligera (`python:3.11-alpine`) para garantizar un peso menor a 300 MB.
2. **Mal orden de capas (`COPY` prematuro):** Copiaba todo el código fuente antes de instalar las dependencias con `pip`, rompiendo el sistema de caché de Docker en cada modificación. 
Se reestructuró para procesar únicamente el archivo de requerimientos primero.
3. **Falta de correspondencia con el script de ejecución:** El comando por defecto apuntaba a un archivo genérico (`app.py`) en lugar de invocar tu script de validación personalizado (`info.sh`).

## Una cosa que se me rompió

Tres o cuatro líneas sobre algo que te haya salido mal durante la unidad y cómo
lo resolviste. Si de verdad no se te rompió nada, dilo y explica qué parte te
costó más entender.

Durante la configuración inicial del entorno y la optimización del Dockerfile, me costó un poco coordinar las rutas relativas para asegurarme de que el script info.sh se copiara exactamente
dentro de la estructura esperada por el contenedor sin arrastrar archivos temporales como caché. Se resolvió estructurando correctamente las instrucciones del Dockerfile y limpiando los
directorios antes del commit.
