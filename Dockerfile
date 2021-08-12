FROM python:3.9.6
ENV PYTHONUNBUFFERED=1

WORKDIR /code
RUN git clone https://github.com/VladimirKirillovskiy/TinkoffAdapter.git /code/
RUN git checkout docker
RUN pip install -r requirements.txt
COPY . /code/

RUN python manage.py makemigrations \
	&& python manage.py migrate

RUN python manage.py shell < TinkoffAdapter/createuser.py \
	&& python manage.py runserver 0.0.0.0:8000
