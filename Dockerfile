FROM gcr.io/zetta-lee-fly-vnc-001/graph-server:base
COPY . /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt \
    && pip install --no-cache-dir --upgrade -r requirements-dev.txt