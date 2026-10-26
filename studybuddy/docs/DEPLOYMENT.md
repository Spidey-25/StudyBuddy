# Deployment and local setup

## Local Windows setup

1. Install Python 3.10+ and MySQL 8. Create a MySQL account with permission to create the configured database and tables.
2. Copy `.env.example` to `.env`; set `MYSQL_USER`, `MYSQL_PASSWORD`, and a random `SECRET_KEY`.
3. From the project root run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py app.py
```

4. Open `http://127.0.0.1:5000`. Startup creates the database and missing schema objects and inserts the development users only if those email addresses do not already exist.

Development accounts:
- `student@example.com` / `Student@123`
- `teacher@example.com` / `Teacher@123`

Change or disable these seed credentials before exposing the app beyond a local demonstration.

## Configuration and persistence

See `.env.example`. The root launcher calls `ensure_database()` and `ensure_schema()` before Flask starts. SQL changes are additive; do not drop old tables to apply them. `backend/migrations/005_computing_course_catalog.sql` documents the new branch and technical-subject rows. The MySQL account needs `CREATE DATABASE` permission for automatic database creation.

## Demo and security boundary

Use a local database with disposable demo data. Set a private `SECRET_KEY`; keep `.env` out of version control. The Flask development server is for the class demo and is not a production deployment server. The app does not execute submitted code. To add real code execution, deploy a separate isolated runner with a constrained runtime, no network, read-only filesystem, resource limits, and a strict request boundary; do not run user code inside Flask.

No production deployment or public hosting is configured by this project.
