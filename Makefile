# Makefile for FIAP Tech Challenger Phase 02
# Product Management System with Cargo Optimization

.PHONY: help up down build clean logs health test setup-env

# Default target
help:
	@echo "FIAP Tech Challenger Phase 02 - Product Management System"
	@echo ""
	@echo "Available commands:"
	@echo "  help              - Show this help message"
	@echo "  setup-env         - Create .env files from examples"
	@echo "  up                - Start all services"
	@echo "  up-dev            - Start all services in development mode"
	@echo "  down              - Stop all services"
	@echo "  build             - Build all services"
	@echo "  clean             - Stop and remove all containers and volumes"
	@echo "  logs              - Show logs from all services"
	@echo "  health            - Check health of all services"
	@echo "  restart           - Restart all services"

# Setup environment files
setup-env:
	@echo "Creating .env files..."
	@if [ ! -f products-service/.env ]; then \
		echo "DATABASE_URL=postgresql://app_user:mysecretpassword@fiap-tech-challenger-fase2-db:5432/products_db" > products-service/.env; \
		echo "HOST=0.0.0.0" >> products-service/.env; \
		echo "PORT=8000" >> products-service/.env; \
		echo "Created products-service/.env"; \
	fi
	@if [ ! -f optimizer-cargo-service/.env ]; then \
		echo "HOST=0.0.0.0" > optimizer-cargo-service/.env; \
		echo "PORT=8002" >> optimizer-cargo-service/.env; \
		echo "Created optimizer-cargo-service/.env"; \
	fi
	@if [ ! -f products-frontend/.env ]; then \
		echo "PRODUCTS_API_URL=http://fiap-tech-challenger-fase2-products-service:8000/products" > products-frontend/.env; \
		echo "OPTIMIZER_URL=http://fiap-tech-challenger-fase2-optimizer-cargo-service:8002/optimize/" >> products-frontend/.env; \
		echo "Created products-frontend/.env"; \
	fi
	@echo "Environment files created successfully!"

# Start services
up: setup-env
	docker-compose up -d --build

# Start services in development mode
up-dev: setup-env
	docker-compose up --build

# Stop services
down:
	docker-compose down

# Build services
build:
	docker-compose build

# Clean everything
clean:
	docker-compose down -v
	docker system prune -f

# Show logs
logs:
	docker-compose logs -f

# Show logs for specific service
logs-%:
	docker-compose logs -f $*

# Check health
health:
	@echo "Checking service health..."
	@echo "Database:"
	@docker-compose exec fiap-tech-challenger-fase2-db pg_isready -U app_user -d products_db || echo "Database: DOWN"
	@echo ""
	@echo "Products Service:"
	@curl -s http://localhost:8000/health/ || echo "Products Service: DOWN"
	@echo ""
	@echo "Optimizer Service:"
	@curl -s http://localhost:8002/health/ || echo "Optimizer Service: DOWN"
	@echo ""
	@echo "Frontend Service:"
	@curl -s http://localhost:8501/ || echo "Frontend Service: DOWN"

# Restart services
restart:
	docker-compose restart

# Status
status:
	docker-compose ps

