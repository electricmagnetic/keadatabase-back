FROM python:3
RUN apt-get update ; apt-get --assume-yes install binutils libproj-dev gdal-bin libgdal-dev
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

