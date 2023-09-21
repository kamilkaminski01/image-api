# Image API

This project involves creating a simple REST API application to upload images
and receive thumbnails, images and expiring images urls based on the users
account tiers.

## Running from sources

```bash
git clone https://github.com/kamilkaminski01/image-api
cd image-api/
```

### Docker setup

```bash
make build
make run
make initial-data
```

Make sure you have enabled **Docker Compose V2**.

### Local setup with a virtual environment

```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate

cd api/

pip install -r requirements.txt
python manage.py migrate
python manage.py initialize_data
python manage.py runserver
```

The app will be available at `localhost:8000` and `127.0.0.1:8000`

After running the app and initializing the database you can log in to 1 of the 3 default accounts and upload images.

The available endpoints are: <br />
`http://localhost:8000/api/images/` for uploading and listing images <br />
`http://localhost:8000/api/images/expire/` for fetching an expiring link to an image

## Makefile

[`Makefile`](Makefile) contains common commands that can be used to build, run
and test the project. The commands include:

- `build`: builds the project with Docker.
- `recreate`: rebuilds the Docker containers.
- `run`: runs the project.
- `clear`: stops the currently running Docker container and removes the project image.
- `lint`: performs static code checks.
- `pytest`: runs unit tests.

### Application setup

After running the application, the following actions should be executed:

Run `make initial-data` or `cd api/ && python manage.py initialize_data` to initialize the database with example data including:

- global superuser (admin@admin.com)
- basic@user.com:
    - user with basic account tier features
- premium@user.com
    - user with premium account tier features
- enterprise@user.com:
    - user with enterprise account tier features

Every user can be logged in with its associated email and password which is by
default `Admin-123`

Access to the django admin panel only has a `global superuser` so to log in, use the credentials:
```
admin@admin.com
Admin-123
```


### Troubleshooting

In case of errors with typing or missing dependencies, try to rebuild the
Docker image:

```bash
make clear
make build
```

If `make` is not supported, the associated Docker commands can be
used directly in order to build and run the project:

```bash
cd image-api/
docker compose build
docker compose up
```

## Code quality standards

All python code is formatted and verified by `black`, `flake8`,
`mypy` and `isort` tools. Their configurations can be found in the
[setup.cfg](api/setup.cfg) file.

Custom functions and methods use **type hints** to improve IDE code
completions, prevent from type errors and extend code documentation.

All features are verified with automated unit tests, including
the expected "happy paths" as well as edge cases that might cause issues
or errors.

In order to run unit tests make sure that the `pytest` library is installed, next run:

```bash
cd image-api/
make pytest
```

## Additional information

It took me about 5 evenings to perform this task (~20/24 hours). :)

Unfortunately, I didn't implement the functionality of returning valid expiring urls because of my lack of time. <br />
I guess this feature requires using `Django Signing` in which I don't have experience with, but I would be happy to learn
more about it in the future.
