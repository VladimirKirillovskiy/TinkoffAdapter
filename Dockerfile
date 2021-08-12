FROM python:3.9.6
ENV PYTHONUNBUFFERED 1
RUN git clone https://github.com/VladimirKirillovskiy/TinkoffAdapter.git

# create root directory for our project in the container
RUN mkdir /TinkoffAdapter

# Set the working directory to /TinkoffAdapter
WORKDIR /TinkoffAdapter

# Copy the current directory contents into the container at /TinkoffAdapter
ADD . /TinkoffAdapter

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

RUN python manage.py makemigrations \
	&& python manage.py migrate \

RUN python manage.py shell < TinkoffAdapter/createuser.py \
	&& python manage.py runserver
