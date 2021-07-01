# face the backend

- [overview](#overview)
- [setup](#setup)
  - [one time](#one-time)
  - [every time](#every-time)
- [container](#container)
  - [image](#image)
  - [compose](#compose)

## overview

![architectural overview](img/face_the_facts.png) <br>
_Fig. 1: Architectural overview_

## setup

### one time

* have `python 3.9` installed
* have `poetry` installed: https://python-poetry.org/docs/#installation

### every time

```console
# (create and) enter virtual environment
$ poetry shell

# install dependencies
$ poetry install

# start development server
$ uvicorn main:app --reload`
```

## container

### image
_(you can replace `podman` with `docker` in most cases)_

```console
# build the container image
$ podman build -t ftf-backend .
```

### compose

```console
# start the podman deamon
$ sudo systemctl start podman.socket

# (check status)
$ sudo systemctl status podman.socket

# build, (re)create, start, and attach to containers for a service
$ sudo docker-compose up --build
```
