FROM gcr.io/zetta-lee-fly-vnc-001/graph-server:base
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --upgrade git+https://github.com/seung-lab/PyChunkedGraph.git@akhilesh-unit-tests