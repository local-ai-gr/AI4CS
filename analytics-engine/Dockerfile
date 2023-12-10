# pull official base image
FROM ubuntu:jammy

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /home

# install required ubuntu packages
RUN apt-get update && \
    apt-get install tzdata -y --no-install-recommends && \
    apt-get install python3 -y --no-install-recommends && \
    apt-get install python3-pip --no-install-recommends -y && \
    pip3 install --upgrade pip && \
    apt-get install wget -y --no-install-recommends && \
    apt-get install unzip -y --no-install-recommends && \
    apt-get install libaio1 -y --no-install-recommends && \
    apt-get install cron -y --no-install-recommends && \
    apt-get install gdal-bin -y --no-install-recommends && \
    DEBIAN_FRONTEND=noninteractive apt-get install postgresql-client -y --no-install-recommends && \
    DEBIAN_FRONTEND=noninteractive apt-get install postgis -yqq --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    dpkg-reconfigure tzdata 


# install python dependencies
COPY ./requirements.txt /home/requirements.txt
RUN pip3 install -r requirements.txt

# setup cron
CMD printenv > /etc/environment && cron -f