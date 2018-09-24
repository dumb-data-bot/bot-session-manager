Bot Session Manager
===

## Setup
```
pip install -r requirements
```

## Execution
```
docker run -p 6379:6379 redis
celery worker -A tasks.app --loglevel=debug
gunicorn -b :5000 webhook:app
```