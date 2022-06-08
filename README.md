# SchoolLib

# View Postman Documentation [here](https://documenter.getpostman.com/view/17046923/Uz5MDYRC)

_How to run with docker_

## Run

- docker compose build
- docker compose up

---

_How to run without docker_

(If you have python and redis installed, you can skip steps 1 and 2)

1. Install python from [here (preferrably version 3.9.8)](https://www.example.com)
2. Install redis from [here](https://redis.io/download/)
3. Create a virtual environment using pipenv, virtualenv or any other tool of your choice
4. Active the environment and run `pip install -r requirements.txt`
5. Create a .env file and copy the environmental variables in the docker-compose.yaml file to the .env file
6. Create a postgres database with host name of `pgdb` and password and username of `postgres`
7. Run `python manage.py migrate && python manage.py makemigrations`
8. Run `python manage.py create_admin`
9. Run `python manage.py runserver`
