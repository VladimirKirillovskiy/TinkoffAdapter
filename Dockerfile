FROM python:3.9.6-slim-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY . /code/

EXPOSE 8000

RUN pip install --upgrade pip \
	&& pip install -r requirements.txt --no-cache-dir \
	&& python manage.py makemigrations \
	&& python manage.py migrate \
	&& python manage.py shell < TinkoffAdapter/createuser.py

ENTRYPOINT python manage.py runserver 0.0.0.0:8000
