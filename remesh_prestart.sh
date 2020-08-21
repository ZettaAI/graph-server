# pods can be killed frequently when using preemtible instances
# re-try failed remesh jobs before starting app server
python -m app.meshing.remesh_pending &
gunicorn -c gunicorn.config.py app.main:app