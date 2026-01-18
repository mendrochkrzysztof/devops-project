.PHONY: help build test run stop clean deploy infra

help:
	@echo "Available commands:"
	@echo "  make build     - Build Docker images"
	@echo "  make test      - Run tests"
	@echo "  make run       - Start services"
	@echo "  make stop      - Stop services"
	@echo "  make clean     - Remove all containers, images, volumes"
	@echo "  make logs      - View logs"
	@echo "  make deploy    - Deploy to production"
	@echo "  make infra     - Deploy Azure infrastructure"

build:
	docker-compose build

test:
	docker build --target test .

run:
	docker-compose up -d

stop:
	docker-compose down

clean:
	docker-compose down -v
	docker system prune -af
	docker volume prune -f

logs:
	docker-compose logs -f

deploy:
	@echo "Deploying to production..."
	# Add deployment logic here

infra:
	cd infra && \
	az deployment group create \
		--resource-group devops-project-rg \
		--template-file main.bicep \
		--parameters parameters.json

migrate:
	docker-compose run --rm migration_runner

seed:
	docker-compose run --rm seed_runner

shell:
	docker-compose exec app sh

db-shell:
	docker-compose exec db psql -U flask_user -d flask_db

nginx-reload:
	docker-compose exec nginx nginx -s reload

status:
	docker-compose ps
	docker-compose top