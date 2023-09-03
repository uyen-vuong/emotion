FROM python:3.10

# install dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
    apt-get install vim default-libmysqlclient-dev gettext \
    libmagic1 ffmpeg libsm6 libxext6 libgl1-mesa-glx cron -yq --no-install-recommends

# copy source and install dependencies
RUN mkdir -p /opt/app/resms
WORKDIR /opt/app/resms
COPY . /opt/app/resms/

RUN python3 -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install setuptools --upgrade \
    && /env/bin/pip install --no-cache-dir -r requirements.txt

# make scripts executable
RUN chmod 755 *.sh

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# start server
EXPOSE 8000
STOPSIGNAL SIGTERM
