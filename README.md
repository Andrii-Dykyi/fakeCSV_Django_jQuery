## Fake CSV Data Generator

> Generate CSV files with fake data.

> Choose number and type of column.

> Choose number of rows.

> Download file.

### Project Description:
 - Backend: **Python**, **Django3**, **Celery**.
 - Frontend: **Bootstrap**, **jQuery**.
 - Project configured **ONLY** for local run.
 - Some services running on **NOT DEFAULT** port to prevent conflicts with your local services.

### Run:
```sh
$ docker-compose build
$ docker-compose up -d
$ docker-compose run python bash -c "python3 manage.py migrate"
```
**Go to** http://127.0.0.1:8080

### Stop:
```sh
$ docker-compose down
```
