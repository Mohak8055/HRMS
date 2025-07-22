dev:
	uvicorn app.main:app --reload

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

prod:
	gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
prod2:
	pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8070" --name "my-fastapi-app"
build:
	docker build -t emp-fastapi .
docker:
	docker run -p 8000:8000 emp-fastapi
revision:
	alembic revision --autogenerate -m "$(msg)"

migrate:
	alembic upgrade head