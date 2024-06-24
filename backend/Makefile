

app-init: app-migrate app-seed app-run
app-init-db: app-migrate app-seed
app-re-init-db: app-downgrade-all app-migrate
app-re-init-db-seed: app-downgrade-all app-migrate app-seed


app-migrate:
	python server.py --database --migrate

app-downgrade-all:
	python server.py --database --downgrade-all

app-seed:
	python server.py --seed

app-run-dev:
	echo "Running in dev mode."
	# app.main: 使用 .来指定路径文件main
	# main: the file main.py (the Python "module").
	# app: the object created inside of main.py with the line app = FastAPI().
	# --reload: make the server restart after code changes. Only use for development.
	poetry run uvicorn app.main:app --reload

app-run:
	echo "Running in production mode."
	poetry run uvicorn app.main:app

