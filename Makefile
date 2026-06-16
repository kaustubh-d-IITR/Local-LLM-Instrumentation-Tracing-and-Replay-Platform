.PHONY: up down rebuild logs migrate health

up:
	docker-compose up -d

down:
	docker-compose down

rebuild:
	docker-compose up --build -d

logs:
	docker-compose logs -f

migrate:
	docker-compose exec backend alembic upgrade head

health:
	curl -f http://localhost:8000/health || echo "Backend is not healthy."
