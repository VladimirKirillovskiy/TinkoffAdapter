# TinkoffAdapter
Python adapter to link Tinkoff API with Java Telegram Bot

To add requirements needed for the project do the next command:
```
python -m pip install -r requirements.txt
```

To start the project locally you should do next commands:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Start with Docker
Download Dockerfile to empty folder, change directory to it, then type in CLI:
```
docker build . -t tinkoffadapter
docker run -d -p 8000:8000 tinkoffadapter
```
