# Signals Backend - Production-Ready API

## 📋 Project Overview

**Signals Backend** is a production-ready FastAPI application for managing **Assets**, **Signals**, and **Measurements**. The application has been refactored from legacy code into a **Clean Architecture** implementation with full type safety, comprehensive testing, and Docker support.

## 🔧 Setup & Installation

### Local Development

```bash
# 1. Clone and navigate
git clone <repo-url>
cd backend-refactor

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -e .

# 4. Run server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Access API:**
- 🌐 API: `http://localhost:8000`
- 📖 Swagger UI: `http://localhost:8000/docs`
- 📚 ReDoc: `http://localhost:8000/redoc`


## 🐳 Docker Deployment

### Quick Start with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# In background mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

```bash
# Single test file
pytest tests/test_assets.py -v

# Single test
pytest tests/test_assets.py::test_create_asset -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```
