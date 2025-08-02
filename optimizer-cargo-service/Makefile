runapp:
	docker compose up --build -d;

runapp-dev:
	docker compose down;
	docker compose up --build;

run-dev:
	uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload