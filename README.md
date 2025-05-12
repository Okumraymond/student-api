# Student CRUD REST API

A simple REST API for managing student records, built with Python and Flask.

## Features

- Create, read, update, and delete student records
- Proper RESTful endpoints with versioning
- Database migrations
- Environment-based configuration
- Health check endpoint
- Unit tests

## Prerequisites

- Python 3.8+
- PostgreSQL
- Git

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/student-api.git
   cd student-api

2. python -m venv venv
source venv/bin/activate  #On Windows: venv\Scripts\activate

3. pip install -r requirements.txt

4. FLASK_APP=app.py

FLASK_ENV=development

DATABASE_URL=postgresql://username:password@localhost:5432/studentdb

5. flask db upgrade 

6. **Run the application**:
   ```bash
   make run

## Docker Deployment

### Build the Docker Image
```bash
make docker-build

### Run the Docker Image
```bash
export DATABASE_URL=postgresql://username:password@hostname:5432/studentdb
make docker-run
