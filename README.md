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

* `poetry shell`: (create and) enter virtual environment
* `poetry install`: install dependencies
* `uvicorn main:app --reload`: start development server

## container

### image
_(you can replace `podman` with `docker` in most cases)_

* `podman build -t ftf-backend .`: build the container image

### compose
* `sudo systemctl start podman.socket`: start the podman deamon (check status with `sudo systemctl status podman.socket`)
* `sudo docker-compose up --build`: build, (re)create, start, and attach to containers for a service
