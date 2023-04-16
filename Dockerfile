FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && \
    apt install -y wget && \
    apt-get install -y --no-install-recommends gcc  \
    libpq-dev -y  \ 
    python3-dev \
    python3-venv python3-wheel -y 

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip

RUN pip install -r requirements.txt


COPY . .

# This command runs database migrations as part of the container build process.
# I understand that this is not a common practice, it may be preferable to run migrations as a separate step outside of the Dockerfile.
# This allows you to better manage your database schema changes and rollbacks,
RUN python manage.py migrate && python manage.py loaddata fixtures.json

#EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#CMD python3 manage.py runserver 0.0.0.0:8000