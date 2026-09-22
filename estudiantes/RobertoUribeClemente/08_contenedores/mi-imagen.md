# Mi imagen en Docker Hub

Llena este archivo en **tu copia**, dentro de
`estudiantes/<tu-login>/08_contenedores/`.

## Quién soy, en los dos lados

- Usuario de GitHub: RobertoUribeClemente
- Usuario de Docker Hub: bobuc05

No tienen por qué ser el mismo, y los nombres de imagen **van en minúsculas
siempre**.

## La URL pública

La que sirve es `https://hub.docker.com/r/<tu-usuario>/<tu-imagen>`. La que te
da el navegador cuando estás con tu sesión abierta empieza con
`hub.docker.com/repository/docker/` y **da 404 a todos los demás, incluido yo**.
Ábrela en una ventana privada antes de entregar.

URL: https://hub.docker.com/r/bobuc05/fdd-imagen

## El digest

```text
docker inspect --format '{{index .RepoDigests 0}}' <tu-usuario>/<tu-imagen>
sha256:cd82d2c13a8f84da5c77b509b69701b7be324053658eacbcc42d4cfd83863af2

```

## Cómo la corro yo

Comando exacto:

```text

sha256:cd82d2c13a8f84da5c77b509b69701b7be324053658eacbcc42d4cfd83863af2
```




Salida que debo esperar:

```text
Corriendo como: app
requests 2.32.3



```

## La prueba de que se baja del registro

Pega la salida **completa**, con sus líneas `Unable to find image locally` y
`Pulling from`:

```text
docker logout
docker rmi -f <tu-usuario>/<tu-imagen>
docker run --rm <tu-usuario>/<tu-imagen>

bobuc05@bobuc05-MCLG-XX:~/fdd/fdd_o26_RobertoUribeClemente/estudiantes/RobertoUribeClemente/08_contenedores$ docker logout
Removing login credentials for [https://index.docker.io/v1/](https://index.docker.io/v1/)
bobuc05@bobuc05-MCLG-XX:~/fdd/fdd_o26_RobertoUribeClemente/estudiantes/RobertoUribeClemente/08_contenedores$ docker rmi -f bobuc05/fdd-imagen:latest
Untagged: bobuc05/fdd-imagen:latest
Deleted: sha256:cd82d2c13a8f84da5c77b509b69701b7be324053658eacbcc42d4cfd83863af2
bobuc05@bobuc05-MCLG-XX:~/fdd/fdd_o26_RobertoUribeClemente/estudiantes/RobertoUribeClemente/08_contenedores$ docker run --rm bobuc05/fdd-imagen:latest
Unable to find image 'bobuc05/fdd-imagen:latest' locally
latest: Pulling from bobuc05/fdd-imagen
2d09b6541c23: Pull complete 
d4026ac44a72: Pull complete 
096595c37430: Pull complete 
0bcf80ba6424: Pull complete 
625ece06bdf0: Pull complete 
44136fa355b3: Download complete 
f942a178a2e1: Download complete 
Digest: sha256:cd82d2c13a8f84da5c77b509b69701b7be324053658eacbcc42d4cfd83863af2
Status: Downloaded newer image for bobuc05/fdd-imagen:latest
Corriendo como: app
requests 2.32.3


```

## El tamaño

Menos de 300 MB. Pega la salida con el tamaño visible:

```text
docker images <tu-usuario>/<tu-imagen>
IMAGE                       ID             DISK USAGE   CONTENT SIZE   EXTRA
bobuc05/fdd-imagen:latest   cd82d2c13a8f        195MB         47.7MB        


```
