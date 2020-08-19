from os import environ


bind = "0.0.0.0:" + environ.get("GRAPH_SERVER_PORT", "1000")
preload = True
workers = int(environ.get("GRAPH_SERVER_WORKERS", 3))
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 300

errorlog = "-"
loglevel = "info"
accesslog = "-"
