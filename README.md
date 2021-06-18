# face the backend

* run postgres: `podman run --rm -p "5432:5432" -e POSTGRES_PASSWORD=postgres postgres`
* activate virtual environment: `poetry shell`
* db migrations: `python manage.py migrate`
* run server `python manage.py runserver`
