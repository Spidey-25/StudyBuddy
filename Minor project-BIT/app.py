import os

from backend.app import app, ensure_database, ensure_schema


if __name__ == "__main__":
    ensure_database()
    ensure_schema()
    app.run(host=os.getenv("APP_HOST", "127.0.0.1"), port=int(os.getenv("APP_PORT", "5000")), debug=os.getenv("FLASK_DEBUG", "0") == "1")
