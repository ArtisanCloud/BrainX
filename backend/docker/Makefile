app-init: app-migrate app-seed app-run
app-init-db: app-migrate app-seed


app-migrate:
	./dist/server/server --database --migrate

app-downgrade-all:
	./dist/server/server --database --downgrade-all

app-seed:
	./dist/server/server --seed

app-run:
	echo "Running in production mode."
	./dist/server/server --start

task-run:
	echo "Running celery task in production mode."
	./dist/task/task  -A app.service.task.celery_app --loglevel=info -P gevent

task-rag-run:
	echo "Running celery rag task in production mode."
	./dist/task/task  -A app.service.task.celery_app -Q rag_queue --loglevel=info -P gevent
