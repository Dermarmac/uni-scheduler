# Vue + FastAPI Class Scheduler

This is a full-stack class scheduling application using:
- **Vue 3 + Vuetify** (frontend)
- **FastAPI + SQLAlchemy** (backend)
- **PostgreSQL** (database)
- Docker and Docker Compose for local development

---

## 🚀 Getting Started (Local Development)

### 1. Clone the Repository

```bash
git clone https://your-repo-url.git
cd your-project
```

### 2. Setup `.env`

Create a `.env` file in the root:

```
POSTGRES_HOST=db
POSTGRES_DB=scheduler
POSTGRES_USER=scheduler
POSTGRES_PASSWORD=scheduler
BACKEND_PORT=8000
FRONTEND_PORT=5173
```

### 3. Build and Start with Docker Compose

```bash
docker-compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- PostgreSQL: localhost:5432

---

## 🛠 Project Structure

```
backend/
├── app/
│   ├── db/        # SQLAlchemy models and DB config
│   ├── routes/    # API endpoints (courses, instructors, etc.)
│   ├── schemas/   # Pydantic models for validation
│   └── main.py    # FastAPI app entrypoint
frontend/
├── src/           # Vue components, views, services
docker-compose.yml
.env
```

---

## 🐳 Docker Services

| Service   | Description          | Port     |
|-----------|----------------------|----------|
| frontend  | Vue 3 dev server     | 5173     |
| backend   | FastAPI app server   | 8000     |
| db        | PostgreSQL database  | 5432     |

---

## 📦 Tech Stack

- **Vue 3** + **Vuetify**
- **FastAPI** + **Pydantic**
- **SQLAlchemy**
- **PostgreSQL**
- **Docker** + **docker-compose**

---

## 📄 License

MIT License
