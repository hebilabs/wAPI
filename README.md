# wAPI

**Weak Application Programming Interface** is a **deliberately vulnerable** REST API built with FastAPI for **educational purposes only**. Use it to learn and practice common web security issues (e.g. SQL injection, broken access control, sensitive data exposure) in a safe environment.

---

## Educational use only

**This application is intentionally insecure.** It is designed for security training, CTFs, and learning how vulnerabilities work and how to find them.

**Do not deploy this API in production or expose it on the internet.** Do not use it with real user data or credentials. The maintainers are not responsible for any misuse or damage arising from its use.

---

## Features

- **Authentication** — Login with email/password; JWT-based access tokens.
- **Users** — Register and retrieve user data (intentionally exposing sensitive fields for training).
- **Products** — List products; create, update, and delete products (admin only).
- **Cart** — Add items, update quantities, view cart, checkout (with intentional access-control issues).
- **Web views** — Simple HTML pages served via Jinja2 templates.
- **Admin** — Admin-only endpoints (e.g. panel) when the admin router is mounted; access based on token payload.

The codebase includes well-documented, intentional vulnerabilities for teaching purposes. Fixing them is left as an exercise.

---

## Tech stack

- **Python 3**
- **FastAPI** — Web framework
- **SQLite** — Database (via `sqlite3`)
- **Pydantic** — Request/response schemas
- **python-jose** — JWT handling
- **Jinja2** — HTML templates
- **Uvicorn** — ASGI server

---

## Setup

1. **Clone the repository** (or use your local copy).

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   # or: venv\Scripts\activate   # Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment** (optional):  
   Copy or create a `.env` file if the app uses one (e.g. for `DATABASE_URL`, `SECRET_KEY`, `APP_NAME`). See `app/core/config.py` for expected settings.

5. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`. Interactive docs at `http://127.0.0.1:8000/docs`.

---

## Run with Docker (easy way)

The project includes a **Dockerfile** and **docker-compose** so you can run everything in one command.

### Option 1: Docker Compose (recommended)

From the project root:

```bash
docker compose up --build
```

This builds the image and starts the API. Open **http://localhost:8000** in your browser; docs at **http://localhost:8000/docs**.

- Stop: `Ctrl+C`, then `docker compose down` if you want to remove the container.
- Run in the background: `docker compose up -d --build`.

### Option 2: Plain Docker

Build and run in one go:

```bash
docker build -t wapi .
docker run -p 8000:8000 --env SECRET_KEY=your_secret wapi
```

Then visit **http://localhost:8000**.

---

## Project structure

```
wAPI/
├── app/
│   ├── main.py              # FastAPI app and router registration
│   ├── core/                # Config, database, security
│   ├── routers/             # API routes (auth, users, products, cart, views, admin)
│   ├── schemas/             # Pydantic models
│   ├── services/            # Business logic and DB access
│   ├── static/              # Static assets
│   └── templates/           # Jinja2 HTML templates
├── requirements.txt
└── README.md
```

---

## API overview

| Area         | Endpoints (examples)                                                               | Notes                              |
| ------------ | ---------------------------------------------------------------------------------- | ---------------------------------- |
| **Auth**     | `POST /auth/login`, `GET /auth/me`                                                 | Token in `Authorization`           |
| **Users**    | `GET /users/{id}`, `POST /users/`                                                  | Registration, user data            |
| **Products** | `GET /products/`, `POST /products/`, `PUT /products/{id}`, `DELETE /products/{id}` | Create/update/delete require admin |
| **Cart**     | `GET /cart/`, `POST /cart/add`, `PUT /cart/update`, `POST /cart/checkout`          | Requires authenticated user        |
| **Views**    | Various HTML routes                                                                | Served via templates               |

Use the Swagger UI at `/docs` to explore and call endpoints.

---

## License

Use only for education and in controlled environments. See the repository for any license terms.
