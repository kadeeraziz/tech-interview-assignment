# interview Preparation
This GitHub repository contains code snippet and resources that I have been working on to prepare for my upcoming technical interview.


### Local Installation

- Clone the repositorie into your system

```
git clone git@github.com:kadeeraziz/tech-interview-assignment.git
```

- Create a virtual environment

```
python3 -m venv venv
```

- Activate the virtual environment


```
source venv/bin/activate
```


- Install requirements by environments:


```
pip install -r requirements.txt
```

By default, the project is configured to use a PostgreSQL database through Docker Compose. If you wish to use SQLite instead, please uncomment the relevant configuration in `settings.py` and comment out the PostgreSQL configuration. Alternatively, if you prefer to use a locally installed PostgreSQL database, please add your database configuration details.

- Make migrations for todo app

```
python manage.py makemigrations todo
```

- Run migrations

```
python manage.py migrate
```

- Import Initial Data

```
python manage.py loaddata fixtures.json
```

- Run the the server


```
python manage.py runserver 
```


# Alternatively you can run the app in the Docker


### Run in docker
- Build docker images
```
docker-compose build
````

- Start and run the containers

```
docker-compose up
```

- Run the migrations

```
docker-compose run web python manage.py migrate
```

- Load intial data

```
docker-compose run web python manage.py loaddata fixtures.json
```