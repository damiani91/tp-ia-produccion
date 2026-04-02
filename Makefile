.PHONY: help setup up down logs train serve test clean

help:
	@echo "Comandos disponibles:"
	@echo "  make setup          - Instalar dependencias"
	@echo "  make up             - Levantar servicios (docker-compose)"
	@echo "  make down           - Parar servicios"
	@echo "  make logs           - Ver logs de servicios"
	@echo "  make train          - Entrenar modelo"
	@echo "  make serve          - Levantar API"
	@echo "  make test           - Correr tests"
	@echo "  make clean          - Limpiar artifacts"

setup:
	pip install -r requirements.txt
	pre-commit install

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

train:
	python scripts/train.py

serve:
	python scripts/serve.py

test:
	pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf mlruns/ .pytest_cache/ .coverage htmlcov/
