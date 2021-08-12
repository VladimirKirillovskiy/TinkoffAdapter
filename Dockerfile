# FROM ubuntu:21.04
# в систему входит python 3.9.4

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.9.6

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /TinkoffAdapter

# Set the working directory to /TinkoffAdapter
WORKDIR /TinkoffAdapter

# Copy the current directory contents into the container at /TinkoffAdapter
ADD . /TinkoffAdapter

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt


# RUN apt update && apt install git \
# 	&& rm -rf /var/lib/apt/lists/*




# COPY requirements.txt /tmp/
# RUN pip install -r /tmp/requirements.txt
# COPY . /tmp/