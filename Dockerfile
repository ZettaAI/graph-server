FROM gcr.io/zetta-lee-fly-vnc-001/graph-server:base
COPY . /app
RUN mkdir /devstuff \
    && apt-get update \
    && apt-get install redis-server -y \
    && pip install --no-cache-dir --upgrade -r requirements.txt \
    && pip install --no-cache-dir --upgrade -r requirements-dev.txt