FROM python:3.6-slim

RUN apt update \
    && apt install -y \
        binutils \
        libproj-dev \
        gdal-bin \
        libmagic-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY /src /src

CMD ["gunicorn", "--pythonpath", "src", "--bind", "0.0.0.0:8000", "keadatabase.wsgi"]
