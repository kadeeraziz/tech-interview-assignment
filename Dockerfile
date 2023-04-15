FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip

RUN pip install -r requirements.txt


COPY . .

RUN python manage.py migrate && python manage.py loaddata fixtures.json

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]