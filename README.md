# face the backend

## overview

![architectural overview](img/face_the_facts.png) <br>
_Fig. 1: Architectural overview_

## setup

* run postgres: `podman run --rm -p "5432:5432" -e POSTGRES_PASSWORD=postgres postgres`
* activate virtual environment: `poetry shell`
* db migrations: `python manage.py migrate`
* run server `python manage.py runserver`
