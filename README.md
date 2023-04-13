# interview Preparation
This GitHub repository contains code snippet and resources that I have been working on to prepare for my upcoming interview.



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


- Run the the server


```
python manage.py runserver 
```


### Alternatively you can run in docker


- Build the docker image

```
docker build -t dockercontainer .
```


- Run the Container

```
docker run dockercontainer
```