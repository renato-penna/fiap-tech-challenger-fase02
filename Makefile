# Makefile for FIAP Tech Challenger Phase 02
# Product Management System with Cargo Optimization

.PHONY: help up down build clean logs health test

# Default target
help:
	@echo "FIAP Tech Challenger Phase 02 - Product Management System"
	@echo ""
	@echo "Available commands:"
	@echo "  help              - Show this help message"
	@echo "  up                - Start all services (Windows)"
	@echo "  up-dev            - Start all services in detached mode (Windows)"
	@echo "  runapp            - Start all services (Linux)"
	@echo "  runapp-dev        - Start all services in detached mode (Linux)"
	@echo "  health            - Check health of all services"

# Linux commands
runapp:
	docker compose down
	docker compose up --build -d

runapp-dev:
	docker compose down
	docker compose up --build

# Windows commands
up:
	t\docker-compose -f docker-compose-win.yml down
	t\docker-compose -f docker-compose-win.yml up --build -d

up-dev:
	t\docker-compose -f docker-compose-win.yml down
	t\docker-compose -f docker-compose-win.yml up --build

health:
	@echo "Checking service health..."
	@curl -s http://localhost:8000/ || echo "Products Service: DOWN"
	@curl -s http://localhost:8002/ || echo "Optimizer Service: DOWN"
	@curl -s http://localhost:8501/ || echo "Frontend Service: DOWN"

