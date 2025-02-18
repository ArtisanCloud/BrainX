app-init: app-migrate app-seed app-run
app-init-db: app-migrate app-seed


app-migrate:
	python ./server.py --database --migrate

app-downgrade-all:
	python ./server.py --database --downgrade-all

app-seed:
	python ./server.py --seed

app-run:
	echo "Running in production mode."
	python ./server.py --start

task-run:
	echo "Running celery task in production mode."
	celery -A app.service.task.celery_worker worker -n brainx@worker_task --loglevel=info -P gevent

task-rag-run:
	echo "Running celery rag task in production mode."
	celery -A app.service.task.celery_worker worker -Q rag_queue -n brainx@worker_rag --loglevel=info -P gevent
