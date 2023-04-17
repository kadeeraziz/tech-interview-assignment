# Technical Assignment
This GitHub repository contains the code, I wrote to complete the technical assigment as part of the interview process.

A todo app built in Django that allows users to manage their daily tasks. The app provides an interface that allows users to create new tasks, edit or delete existing ones, and mark completed tasks as done.

Upon logging in, the user is presented with a dashboard that displays a list of all their tasks, along with relevant information such as due date, and status. To create a new task, users can simply enter a description and set a due date, and the app will automatically store the task information in a database. Users can also edit or delete tasks at any time, as well as mark tasks as completed once they are done.

The following are the instructions on how to run the project locally or in the docker. 


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