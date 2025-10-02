FROM python:3.12.11-trixie AS base

RUN apt-get update && apt-get install -y redis

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED=1

# Defaults to PIP
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

FROM base AS dependencies

WORKDIR /app/
ADD start.sh /app/
RUN chmod +x /app/start.sh

RUN python -m venv venv
RUN . /app/venv/bin/activate
RUN pip install --upgrade pip
ADD requirements.txt /app
RUN pip install -r /app/requirements.txt
ADD src /app/

# Not best practice, but let's not get into docker secrets.
ARG POLYGON_API_KEY
ENV POLYGON_API_KEY=$POLYGON_API_KEY

EXPOSE 8000
ENTRYPOINT ["/bin/sh", "/app/start.sh"]