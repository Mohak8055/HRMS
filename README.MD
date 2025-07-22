# FastAPI HRMS

A Human Resource Management System (HRMS) API built with FastAPI, SQLAlchemy, and Alembic. This project provides endpoints for user authentication, department and role management, and user CRUD operations.

## Features
- User authentication (JWT-based)
- Department and role management
- User CRUD operations
- Alembic migrations for database schema
- Modular code structure

## Project Structure
```
app/
  ├── api/routes/         # API route definitions
  ├── crud/               # CRUD operations
  ├── models/             # SQLAlchemy models
  ├── schemas/            # Pydantic schemas
  ├── utils/              # Utility functions
  ├── config.py           # App configuration
  ├── database.py         # Database connection
  └── main.py             # FastAPI app entrypoint
alembic/                  # Alembic migration scripts
requirements.txt          # Python dependencies
Dockerfile                # Containerization
Makefile                  # Common tasks
```

## Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL (or your preferred DB)
- [Poetry](https://python-poetry.org/) or `pip`

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/sspsinha/FastApi-HRMS.git
   cd FastApi-HRMS
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure your database in `app/config.py`.
4. Run Alembic migrations:
   ```sh
   alembic upgrade head
   ```
5. Start the FastAPI server:
   ```sh
   uvicorn app.main:app --reload
   ```

## Usage
- API docs available at: `http://localhost:8000/docs`
- Use endpoints for authentication, user, department, and role management.

## Alembic Migrations
- Migration scripts are in `alembic/versions/`
- To create a new migration:
  ```sh
  alembic revision --autogenerate -m "Migration message"
  alembic upgrade head
  ```

## Docker
To run with Docker:
```sh
docker build -t fastapi-hrms .
docker run -p 8000:8000 fastapi-hrms
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.
