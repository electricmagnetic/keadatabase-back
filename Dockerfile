FROM python:3.6

ARG GDAL_VERSION=2.1.3
ARG PROJ_VERSION=4.9.3
ARG GEOS_VERSION=3.6.1

RUN cd /tmp && \
    curl http://download.osgeo.org/gdal/$GDAL_VERSION/gdal-$GDAL_VERSION.tar.gz -s -o - | tar zxf - && \
    cd gdal-$GDAL_VERSION && \
    ./configure && \
    make && \
    make install

RUN cd /tmp && \
    curl http://download.osgeo.org/geos/geos-$GEOS_VERSION.tar.bz2 -s -o - | tar xjf - && \
    cd geos-$GEOS_VERSION && \
    ./configure && \
    make && \
    make install

RUN cd /tmp && \
    curl http://download.osgeo.org/proj/proj-$PROJ_VERSION.tar.gz -s -o - | tar zxf - && \
    cd proj-$PROJ_VERSION && \
    ./configure && \
    make && \
    make install

RUN /sbin/ldconfig

ENV GEO_LIBRARIES_PATH=/usr/local

COPY requirements.txt /src/requirements.txt

RUN pip install -r /src/requirements.txt

COPY src /src

WORKDIR /src

CMD ["/usr/local/bin/gunicorn", "keadatabase.wsgi"]
