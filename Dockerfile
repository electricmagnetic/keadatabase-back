FROM python:3.6-slim

RUN apt update \
    && apt install -y \
        binutils \
        libproj-dev \
        gdal-bin \
        libmagic-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# To run with OpenStack Swift on Catalyst Cloud
RUN pip install django-storage-swift

COPY /src /src

CMD ["gunicorn", "-b", "0.0.0.0:8000", "keadatabase.wsgi"]
