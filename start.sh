#/bin/sh

service redis-server start
python -m uvicorn main:app --host=0.0.0.0 --port 8000
