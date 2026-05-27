# Makefile for Food-Ordering-System
# Usage (run from project root):
#   make install      # install dependencies
#   make migrate      # apply Django migrations
#   make runserver    # start Django dev server
#   make seed         # seed the database (runs scratch/seed_final.py)
#   make test         # run Django tests
#   make clean        # remove python artefacts

# Detect OS (Windows) and use the venv Python executable
PYTHON := .venv\\Scripts\\python.exe
PIP := .venv\\Scripts\\pip.exe

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install   - Install Python dependencies from requirements.txt"
	@echo "  make migrate   - Apply Django migrations"
	@echo "  make dev - Run Django development server"
	@echo "  make seed      - Seed the database using scratch/seed_final.py"
	@echo "  make test      - Run Django test suite"
	@echo "  make clean     - Clean compiled python files"

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r requirements.txt~

# Apply migrations
.PHONY: migrate
migrate:
	$(PYTHON) manage.py migrate

# Run development server
.PHONY: dev
dev:
	$(PYTHON) manage.py runserver

# Seed the database
.PHONY: seed
seed:
	$(PYTHON) ./scratch/seed_final.py

# Run tests
.PHONY: test
test:
	$(PYTHON) manage.py test

# Clean up __pycache__ and *.pyc files
.PHONY: clean
clean:
	rmdir /s /q __pycache__ 2>nul || true
	del /s /q *.pyc 2>nul || true
