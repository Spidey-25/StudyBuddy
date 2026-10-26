import json
import os
import re
import uuid
from datetime import datetime, timedelta
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, jsonify, request, session, send_from_directory
from werkzeug.security import check_password_hash, generate_password_hash
from . import game_catalog

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
FRONTEND = ROOT / "frontend"

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("SECRET_KEY", "change-this-secret-key"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
)


def mysql_options(include_database=True):
    options = {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
    }
    if include_database:
        options["database"] = os.getenv("MYSQL_DATABASE", "studybuddy")
    return options


def db_connection():
    return mysql.connector.connect(**mysql_options())


BRANCHES = {
    "cse": "Computer Science and Engineering",
    "it": "Information Technology",
    "ce": "Computer Engineering",
    "aiml": "Artificial Intelligence and Machine Learning",
    "ds": "Data Science",
    "cyber": "Cybersecurity",
}
SUBJECT_CODE_ALIASES = {"Python": "PYTHON", "Web": "WEB", "C++": "CPP", "DSA-C++": "DSA", "DSA-Java": "DSA"}

SUBJECTS = {
    "cse": [("C", "C Programming"), ("CPP", "C++"), ("JAVA", "Java"), ("PYTHON", "Python"), ("DSA", "Data Structures and Algorithms"), ("DBMS", "Database Management Systems"), ("OS", "Operating Systems"), ("CN", "Computer Networks"), ("WEB", "Web Development"), ("SE", "Software Engineering"), ("AI", "Artificial Intelligence"), ("ML", "Machine Learning"), ("CYBER", "Cybersecurity"), ("CLOUD", "Cloud Computing"), ("EMBEDDED", "Embedded Systems"), ("IOT", "Internet of Things")],
    "it": [("C", "C Programming"), ("CPP", "C++"), ("JAVA", "Java"), ("PYTHON", "Python"), ("DSA", "Data Structures and Algorithms"), ("DBMS", "Database Management Systems"), ("OS", "Operating Systems"), ("CN", "Computer Networks"), ("WEB", "Web Development"), ("SE", "Software Engineering"), ("CYBER", "Cybersecurity"), ("CLOUD", "Cloud Computing")],
    "ce": [("C", "C Programming"), ("CPP", "C++"), ("JAVA", "Java"), ("PYTHON", "Python"), ("DSA", "Data Structures and Algorithms"), ("DBMS", "Database Management Systems"), ("OS", "Operating Systems"), ("CN", "Computer Networks"), ("EMBEDDED", "Embedded Systems"), ("IOT", "Internet of Things")],
    "aiml": [("JAVA", "Java"), ("PYTHON", "Python"), ("DSA", "Data Structures and Algorithms"), ("DBMS", "Database Management Systems"), ("OS", "Operating Systems"), ("CN", "Computer Networks"), ("AI", "Artificial Intelligence"), ("ML", "Machine Learning"), ("CLOUD", "Cloud Computing")],
    "ds": [("JAVA", "Java"), ("PYTHON", "Python"), ("DSA", "Data Structures and Algorithms"), ("DBMS", "Database Management Systems"), ("OS", "Operating Systems"), ("CN", "Computer Networks"), ("ML", "Machine Learning"), ("AI", "Artificial Intelligence"), ("CLOUD", "Cloud Computing")],
    "cyber": [("C", "C Programming"), ("CPP", "C++"), ("JAVA", "Java"), ("PYTHON", "Python"), ("DSA", "Data Structures and Algorithms"), ("DBMS", "Database Management Systems"), ("OS", "Operating Systems"), ("CN", "Computer Networks"), ("WEB", "Web Development"), ("CYBER", "Cybersecurity"), ("CLOUD", "Cloud Computing")],
}
# Keep existing account branch codes working without rewriting user records.
SUBJECTS.update({"software": SUBJECTS["cse"], "information": SUBJECTS["it"], "electronics": SUBJECTS["ce"], "ai": SUBJECTS["aiml"], "data": SUBJECTS["ds"]})
SUPPORTED_SUBJECT_CODES = {code for branch_subjects in SUBJECTS.values() for code, _ in branch_subjects}


def ensure_database():
    database = os.getenv("MYSQL_DATABASE", "studybuddy")
    connection = mysql.connector.connect(**mysql_options(include_database=False))
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cursor.close()
    connection.close()


def ensure_schema():
    connection = db_connection()
    cursor = connection.cursor()
    statements = [
        """CREATE TABLE IF NOT EXISTS branches (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, code VARCHAR(40) NOT NULL UNIQUE, name VARCHAR(120) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        """CREATE TABLE IF NOT EXISTS users (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, email VARCHAR(190) NOT NULL UNIQUE, username VARCHAR(40) NOT NULL, password_hash VARCHAR(255) NOT NULL, display_name VARCHAR(40) NOT NULL, role ENUM('student','teacher') NOT NULL DEFAULT 'student', branch_id INT UNSIGNED NULL, course VARCHAR(120) NULL, created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, CONSTRAINT fk_user_branch FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE SET NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        """CREATE TABLE IF NOT EXISTS subjects (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, code VARCHAR(60) NOT NULL, name VARCHAR(160) NOT NULL, branch_id INT UNSIGNED NULL, created_by INT UNSIGNED NULL, UNIQUE KEY uq_subject_branch (code, branch_id), CONSTRAINT fk_subject_branch FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE CASCADE, CONSTRAINT fk_subject_creator FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        """CREATE TABLE IF NOT EXISTS user_subjects (user_id INT UNSIGNED NOT NULL, subject_id INT UNSIGNED NOT NULL, PRIMARY KEY (user_id, subject_id), CONSTRAINT fk_us_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE, CONSTRAINT fk_us_subject FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        """CREATE TABLE IF NOT EXISTS games (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, subject_id INT UNSIGNED NOT NULL, title VARCHAR(160) NOT NULL, game_type VARCHAR(40) NOT NULL, content_json JSON NOT NULL, UNIQUE KEY uq_game_subject_title (subject_id, title), CONSTRAINT fk_game_subject FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        """CREATE TABLE IF NOT EXISTS study_sessions (id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY, user_id INT UNSIGNED NOT NULL, client_session_id VARCHAR(64) NULL, subject_code VARCHAR(60) NOT NULL, game_type VARCHAR(40) NOT NULL, status VARCHAR(16) NOT NULL DEFAULT 'completed', accuracy DECIMAL(5,2) NOT NULL DEFAULT 0, seconds INT UNSIGNED NOT NULL DEFAULT 0, points INT UNSIGNED NOT NULL DEFAULT 0, xp_awarded INT UNSIGNED NOT NULL DEFAULT 0, completed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, UNIQUE KEY uq_study_client_session (user_id,client_session_id), CONSTRAINT fk_session_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        """CREATE TABLE IF NOT EXISTS question_attempts (id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY, session_id BIGINT UNSIGNED NOT NULL, user_id INT UNSIGNED NOT NULL, subject_code VARCHAR(60) NOT NULL, topic VARCHAR(160) NOT NULL, correct BOOLEAN NOT NULL, response_seconds INT UNSIGNED NOT NULL DEFAULT 0, CONSTRAINT fk_attempt_session FOREIGN KEY (session_id) REFERENCES study_sessions(id) ON DELETE CASCADE, CONSTRAINT fk_attempt_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        """CREATE TABLE IF NOT EXISTS platform_game_sessions (id CHAR(36) PRIMARY KEY, user_id INT UNSIGNED NOT NULL, game_id VARCHAR(80) NOT NULL, subject_code VARCHAR(60) NOT NULL, state_json JSON NOT NULL, score INT UNSIGNED NOT NULL DEFAULT 0, accuracy DECIMAL(5,2) NOT NULL DEFAULT 0, mistakes INT UNSIGNED NOT NULL DEFAULT 0, xp_awarded INT UNSIGNED NOT NULL DEFAULT 0, status VARCHAR(16) NOT NULL DEFAULT 'active', started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, ended_at TIMESTAMP NULL, completed_at TIMESTAMP NULL, seconds INT UNSIGNED NOT NULL DEFAULT 0, INDEX ix_platform_user_subject (user_id, subject_code), INDEX ix_platform_status_user (user_id, status), INDEX ix_platform_game (game_id), CONSTRAINT fk_platform_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        """CREATE TABLE IF NOT EXISTS platform_game_attempts (id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY, platform_session_id CHAR(36) NOT NULL, client_action_id CHAR(36) NULL, response_json JSON NULL, user_id INT UNSIGNED NOT NULL, game_id VARCHAR(80) NOT NULL, subject_code VARCHAR(60) NOT NULL, level_index INT UNSIGNED NOT NULL, topic VARCHAR(160) NOT NULL, objective VARCHAR(500) NOT NULL, correct BOOLEAN NOT NULL, response_seconds INT UNSIGNED NOT NULL DEFAULT 0, created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, UNIQUE KEY uq_platform_action_id (platform_session_id, client_action_id), INDEX ix_platform_attempt_topic (subject_code, game_id, correct), CONSTRAINT fk_platform_attempt_session FOREIGN KEY (platform_session_id) REFERENCES platform_game_sessions(id) ON DELETE CASCADE, CONSTRAINT fk_platform_attempt_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
    ]
    for statement in statements:
        cursor.execute(statement)
    # Older installations created this table before lifecycle and reward data
    # was tracked. Apply additive, idempotent upgrades without dropping rows.
    cursor.execute("SHOW COLUMNS FROM platform_game_sessions")
    platform_columns = {row[0] for row in cursor.fetchall()}
    additions = {
        "accuracy": "DECIMAL(5,2) NOT NULL DEFAULT 0",
        "xp_awarded": "INT UNSIGNED NOT NULL DEFAULT 0",
        "status": "VARCHAR(16) NOT NULL DEFAULT 'active'",
        "ended_at": "TIMESTAMP NULL",
    }
    for column, definition in additions.items():
        if column not in platform_columns:
            cursor.execute(f"ALTER TABLE platform_game_sessions ADD COLUMN {column} {definition}")
    cursor.execute("SHOW INDEX FROM platform_game_sessions")
    platform_indexes = {row[2] for row in cursor.fetchall()}
    if "ix_platform_status_user" not in platform_indexes:
        cursor.execute("ALTER TABLE platform_game_sessions ADD INDEX ix_platform_status_user (user_id, status)")
    cursor.execute("UPDATE platform_game_sessions SET status='completed', ended_at=COALESCE(ended_at, completed_at) WHERE completed_at IS NOT NULL AND status<>'completed'")
    cursor.execute("UPDATE platform_game_sessions SET ended_at=COALESCE(ended_at, started_at) WHERE status IN ('abandoned','exited') AND ended_at IS NULL")
    cursor.execute("SHOW COLUMNS FROM study_sessions")
    legacy_columns = {row[0] for row in cursor.fetchall()}
    for column, definition in {
        "client_session_id": "VARCHAR(64) NULL",
        "status": "VARCHAR(16) NOT NULL DEFAULT 'completed'",
        "xp_awarded": "INT UNSIGNED NOT NULL DEFAULT 0",
    }.items():
        if column not in legacy_columns:
            cursor.execute(f"ALTER TABLE study_sessions ADD COLUMN {column} {definition}")
    cursor.execute("SHOW INDEX FROM study_sessions")
    legacy_indexes = {row[2] for row in cursor.fetchall()}
    if "uq_study_client_session" not in legacy_indexes:
        cursor.execute("ALTER TABLE study_sessions ADD UNIQUE INDEX uq_study_client_session (user_id,client_session_id)")
    cursor.execute("SHOW COLUMNS FROM platform_game_attempts")
    attempt_columns={row[0] for row in cursor.fetchall()}
    for column,definition in {"client_action_id":"CHAR(36) NULL","response_json":"JSON NULL"}.items():
        if column not in attempt_columns:
            cursor.execute(f"ALTER TABLE platform_game_attempts ADD COLUMN {column} {definition}")
    cursor.execute("SHOW INDEX FROM platform_game_attempts")
    attempt_indexes={row[2] for row in cursor.fetchall()}
    if "uq_platform_action_id" not in attempt_indexes:
        cursor.execute("ALTER TABLE platform_game_attempts ADD UNIQUE INDEX uq_platform_action_id (platform_session_id,client_action_id)")
    for code, name in BRANCHES.items():
        cursor.execute("INSERT IGNORE INTO branches (code, name) VALUES (%s, %s)", (code, name))
    cursor.execute("SELECT id, code FROM branches")
    branch_ids = {code: branch_id for branch_id, code in cursor.fetchall()}
    for branch_code, subjects in SUBJECTS.items():
        if branch_code not in branch_ids: continue
        for code, name in subjects:
            cursor.execute("INSERT IGNORE INTO subjects (code, name, branch_id) VALUES (%s, %s, %s)", (code, name, branch_ids[branch_code]))
            cursor.execute("SELECT id FROM subjects WHERE code=%s AND branch_id=%s", (code, branch_ids[branch_code]))
            cursor.fetchone()
    connection.commit()
    seed_test_users(cursor, branch_ids)
    connection.commit()
    cursor.close()
    connection.close()


def seed_test_users(cursor, branch_ids):
    users = [
        ("student@example.com", "Test Student", "student", branch_ids["cse"], BRANCHES["cse"], "Student@123"),
        ("teacher@example.com", "Test Teacher", "teacher", None, None, "Teacher@123"),
    ]
    for email, display_name, role, branch_id, course, password in users:
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            continue
        cursor.execute("INSERT INTO users (email, username, password_hash, display_name, role, branch_id, course) VALUES (%s,%s,%s,%s,%s,%s,%s)", (email, email.split("@")[0], generate_password_hash(password), display_name, role, branch_id, course))
        if branch_id:
            user_id = cursor.lastrowid
            cursor.execute("INSERT IGNORE INTO user_subjects SELECT %s, id FROM subjects WHERE branch_id=%s", (user_id, branch_id))


def current_user_id():
    return session.get("user_id")


def subject_rows(cursor, user_id=None, branch_id=None):
    query = "SELECT s.id, s.code, s.name, b.code, b.name FROM subjects s LEFT JOIN branches b ON b.id=s.branch_id"
    params = []
    supported = sorted(SUPPORTED_SUBJECT_CODES)
    conditions = ["(s.code IN (" + ",".join(["%s"] * len(supported)) + ") OR s.created_by IS NOT NULL)"]
    if user_id:
        cursor.execute("SELECT branch_id FROM users WHERE id=%s", (user_id,)); user_branch = cursor.fetchone()
        query += " JOIN user_subjects us ON us.subject_id=s.id"
        conditions.append("us.user_id=%s")
        params.append(user_id)
        if user_branch and user_branch[0] is not None:
            conditions.append("(s.branch_id=%s OR s.branch_id IS NULL)")
            params.append(user_branch[0])
    if branch_id is not None:
        conditions.append("(s.branch_id=%s OR s.branch_id IS NULL)")
        params.append(branch_id)
    query += " WHERE " + " AND ".join(conditions)
    params = [*supported, *params]
    query += " ORDER BY s.name"
    cursor.execute(query, params)
    return [{"id": r[0], "code": r[1], "name": r[2], "branch_code": r[3], "branch_name": r[4]} for r in cursor.fetchall()]


def payload(cursor, row):
    user_id, email, username, display_name, role, branch_id, course = row
    cursor.execute("SELECT code, name FROM branches WHERE id=%s", (branch_id,))
    branch = cursor.fetchone()
    return {"id": user_id, "email": email, "username": username, "display_name": display_name, "role": role, "branch_id": branch_id, "branch": branch[0] if branch else None, "branch_name": branch[1] if branch else None, "course": course, "subjects": subject_rows(cursor, user_id=user_id)}


@app.get("/api/health")
def health():
    try:
        connection = db_connection()
        connection.ping(reconnect=True, attempts=1, delay=0)
        connection.close()
        return jsonify({"ok": True, "database": "connected"})
    except mysql.connector.Error as error:
        return jsonify({"ok": False, "database": "unavailable", "error": str(error)}), 503


@app.get("/api/branches")
def branches():
    return jsonify({"branches": [{"code": k, "name": v} for k, v in BRANCHES.items()]})


@app.post("/api/register")
def register():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    role = str(data.get("role", "student")).lower()
    display_name = str(data.get("display_name", "")).strip()
    password = str(data.get("password", ""))
    branch = str(data.get("branch", "")).strip().lower()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email): return jsonify({"error": "Enter a valid email address."}), 400
    if role not in ("student", "teacher"): return jsonify({"error": "Choose a valid account type."}), 400
    if not display_name or len(display_name) > 40: return jsonify({"error": "Display name is required."}), 400
    if not 6 <= len(password) <= 128: return jsonify({"error": "Password must be between 6 and 128 characters."}), 400
    if role == "student" and branch not in BRANCHES: return jsonify({"error": "Choose a branch/course."}), 400
    connection = db_connection(); cursor = connection.cursor()
    try:
        branch_id = None
        if branch: cursor.execute("SELECT id FROM branches WHERE code=%s", (branch,)); branch_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO users (email, username, password_hash, display_name, role, branch_id, course) VALUES (%s,%s,%s,%s,%s,%s,%s)", (email, email.split("@")[0], generate_password_hash(password), display_name, role, branch_id, BRANCHES.get(branch)))
        user_id = cursor.lastrowid
        if branch_id:
            cursor.execute("INSERT IGNORE INTO user_subjects SELECT %s, id FROM subjects WHERE branch_id=%s", (user_id, branch_id))
        connection.commit()
    except mysql.connector.IntegrityError: connection.rollback(); return jsonify({"error": "That email is already registered."}), 409
    finally: cursor.close(); connection.close()
    session.permanent = True; session["user_id"] = user_id
    connection = db_connection(); cursor = connection.cursor(); cursor.execute("SELECT id,email,username,display_name,role,branch_id,course FROM users WHERE id=%s", (user_id,)); result = payload(cursor, cursor.fetchone()); cursor.close(); connection.close()
    return jsonify({"user": result}), 201


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}; email = str(data.get("email", "")).strip().lower(); password = str(data.get("password", ""))
    connection = db_connection(); cursor = connection.cursor(); cursor.execute("SELECT id,email,username,display_name,role,branch_id,course,password_hash FROM users WHERE email=%s", (email,)); row = cursor.fetchone(); cursor.close(); connection.close()
    if not row or not check_password_hash(row[7], password): return jsonify({"error": "Invalid email or password."}), 401
    session.permanent = True; session["user_id"] = row[0]
    connection = db_connection(); cursor = connection.cursor(); cursor.execute("SELECT id,email,username,display_name,role,branch_id,course FROM users WHERE id=%s", (row[0],)); result = payload(cursor, cursor.fetchone()); cursor.close(); connection.close()
    return jsonify({"user": result})


@app.post("/api/logout")
def logout(): session.clear(); return jsonify({"ok": True})


@app.get("/api/me")
def me():
    if not current_user_id(): return jsonify({"user": None})
    connection = db_connection(); cursor = connection.cursor(); cursor.execute("SELECT id,email,username,display_name,role,branch_id,course FROM users WHERE id=%s", (current_user_id(),)); row = cursor.fetchone()
    if not row: session.clear(); cursor.close(); connection.close(); return jsonify({"user": None})
    result = payload(cursor, row); cursor.close(); connection.close(); return jsonify({"user": result})


@app.get("/api/subjects")
def get_subjects():
    connection = db_connection(); cursor = connection.cursor()
    branch = request.args.get("branch")
    branch_id = request.args.get("branch_id")
    if branch:
        cursor.execute("SELECT id FROM branches WHERE code=%s", (branch.lower(),)); found = cursor.fetchone(); branch_id = found[0] if found else -1
    elif branch_id and not str(branch_id).isdigit():
        cursor.execute("SELECT id FROM branches WHERE code=%s", (str(branch_id).lower(),)); found = cursor.fetchone(); branch_id = found[0] if found else -1
    result = subject_rows(cursor, branch_id=int(branch_id) if branch_id else None); cursor.close(); connection.close(); return jsonify({"subjects": result})


@app.get("/api/game-catalog")
def get_game_catalog():
    subject = request.args.get("subject", "").upper()
    catalog = [game_catalog.public_game(game_id) for game_id in game_catalog.GAMES]
    if subject:
        catalog = [item for item in catalog if item["subject"] == subject]
    return jsonify({"games": catalog})


def platform_session_row(cursor, session_id, user_id, lock=False):
    cursor.execute("SELECT game_id, subject_code, state_json, score, mistakes, started_at, completed_at, seconds, status, ended_at, accuracy, xp_awarded FROM platform_game_sessions WHERE id=%s AND user_id=%s" + (" FOR UPDATE" if lock else ""), (session_id, user_id))
    return cursor.fetchone()


@app.post("/api/game-sessions")
def start_platform_game():
    user_id = current_user_id()
    if not user_id: return jsonify({"error": "Login required."}), 401
    request_data = request.get_json(silent=True) or {}
    game_id = str(request_data.get("game_id", ""))
    game = game_catalog.public_game(game_id)
    if not game: return jsonify({"error": "Unknown game."}), 404
    language = str(request_data.get("language", "")).strip()
    if game["subject"] == "DSA" and language not in {"C++", "Java"}: return jsonify({"error": "Choose C++ or Java for DSA practice."}), 400
    connection = db_connection(); cursor = connection.cursor()
    cursor.execute("SELECT u.branch_id, u.role FROM users u WHERE u.id=%s", (user_id,)); user = cursor.fetchone()
    if not user: cursor.close(); connection.close(); return jsonify({"error": "Login required."}), 401
    if user[1] != "teacher":
        cursor.execute("SELECT 1 FROM user_subjects us JOIN subjects s ON s.id=us.subject_id WHERE us.user_id=%s AND s.code=%s LIMIT 1", (user_id, game["subject"]))
        if not cursor.fetchone(): cursor.close(); connection.close(); return jsonify({"error": "Choose this subject before starting its games."}), 403
    cursor.execute("SELECT state_json FROM platform_game_sessions WHERE user_id=%s AND game_id=%s ORDER BY started_at DESC LIMIT 1", (user_id,game_id))
    previous = cursor.fetchone()
    previous_order = []
    if previous:
        previous_state = json.loads(previous[0]) if isinstance(previous[0], str) else previous[0]
        previous_order = previous_state.get("level_order", [])
    session_id = str(__import__("uuid").uuid4()); state = game_catalog.initial_state(game_id, previous_order); state["level_started_at"] = datetime.now().isoformat()
    game = game_catalog.public_session_game(game_id, state)
    if game["subject"] == "DSA": state["language"] = language; game["language"] = language
    try:
        now = datetime.now()
        cursor.execute("UPDATE platform_game_sessions SET status='abandoned', ended_at=%s, seconds=GREATEST(seconds,TIMESTAMPDIFF(SECOND,started_at,%s)) WHERE user_id=%s AND status='active'", (now, now, user_id))
        cursor.execute("INSERT INTO platform_game_sessions (id,user_id,game_id,subject_code,state_json,status) VALUES (%s,%s,%s,%s,%s,'active')", (session_id,user_id,game_id,game["subject"],json.dumps(state)))
        connection.commit()
    except Exception:
        connection.rollback(); raise
    finally:
        cursor.close(); connection.close()
    return jsonify({"session_id": session_id, "game": game, "state": state}), 201


@app.get("/api/game-sessions/<session_id>")
def get_platform_session(session_id):
    user_id = current_user_id()
    if not user_id: return jsonify({"error": "Login required."}), 401
    connection = db_connection(); cursor = connection.cursor(); row = platform_session_row(cursor, session_id, user_id)
    if not row: cursor.close(); connection.close(); return jsonify({"error": "Session not found."}), 404
    game_id, subject, state_json, score, mistakes, started, completed, seconds, status, ended, accuracy, xp_awarded = row
    cursor.close(); connection.close()
    state = json.loads(state_json) if isinstance(state_json, str) else state_json
    game_catalog_game = game_catalog.public_session_game(game_id, state)
    if state.get("language"): game_catalog_game["language"] = state["language"]
    return jsonify({"session_id": session_id, "game": game_catalog_game, "state": state, "score": score, "accuracy": float(accuracy or 0), "mistakes": mistakes, "xp_awarded": xp_awarded, "status": status, "ended_at": ended.isoformat() if ended else None, "complete": status == "completed", "seconds": seconds})


@app.get("/api/game-sessions")
def list_platform_sessions():
    user_id = current_user_id()
    if not user_id: return jsonify({"error": "Login required."}), 401
    connection = db_connection(); cursor = connection.cursor()
    cursor.execute("SELECT id,game_id,subject_code,score,mistakes,started_at,completed_at,seconds,state_json,status,ended_at,accuracy,xp_awarded FROM platform_game_sessions WHERE user_id=%s ORDER BY started_at DESC LIMIT 100", (user_id,))
    rows = cursor.fetchall(); cursor.close(); connection.close()
    sessions = []
    for row in rows:
        state = json.loads(row[8]) if isinstance(row[8], str) else row[8]
        game = game_catalog.public_game(row[1])
        sessions.append({"id":row[0],"game_id":row[1],"title":game["title"],"subject":row[2],"language":state.get("language"),"score":row[3],"mistakes":row[4],"started_at":row[5].isoformat() if row[5] else None,"completed_at":row[6].isoformat() if row[6] else None,"seconds":row[7],"status":row[9],"ended_at":row[10].isoformat() if row[10] else None,"accuracy":float(row[11] or 0),"xp_awarded":row[12],"complete":row[9] == "completed","level":state.get("level",0),"actions":state.get("actions",0)})
    return jsonify({"sessions": sessions, "total_xp": sum(item["xp_awarded"] for item in sessions)})


@app.post("/api/game-sessions/<session_id>/exit")
def end_platform_session(session_id):
    user_id = current_user_id()
    if not user_id: return jsonify({"error": "Login required."}), 401
    data = request.get_json(silent=True) or {}
    status = data.get("status", "exited")
    if not isinstance(status,str) or status not in {"exited", "abandoned"}: return jsonify({"error": "Session status must be exited or abandoned."}), 400
    connection = db_connection(); cursor = connection.cursor()
    try:
        row = platform_session_row(cursor, session_id, user_id, lock=True)
        if not row: connection.rollback(); return jsonify({"error": "Session not found."}), 404
        current_status = row[8]
        if current_status == "active":
            now = datetime.now()
            state = json.loads(row[2]) if isinstance(row[2], str) else row[2]
            elapsed = max(0, int((now - row[5]).total_seconds()))
            events = state.get("events", [])
            actions = len(events)
            accuracy = round(sum(bool(event.get("correct")) for event in events) * 100 / actions, 2) if actions else 0
            cursor.execute("UPDATE platform_game_sessions SET status=%s,ended_at=%s,seconds=%s,accuracy=%s WHERE id=%s AND user_id=%s AND status='active'", (status,now,elapsed,accuracy,session_id,user_id))
            connection.commit()
            current_status = status
        else:
            connection.rollback()
        return jsonify({"session_id":session_id,"status":current_status,"complete":current_status == "completed"})
    except Exception:
        connection.rollback(); raise
    finally:
        cursor.close(); connection.close()


@app.post("/api/game-sessions/<session_id>/action")
def platform_game_action(session_id):
    user_id = current_user_id()
    if not user_id: return jsonify({"error": "Login required."}), 401
    action = request.get_json(silent=True)
    if not isinstance(action, dict) or len(json.dumps(action)) > 4000: return jsonify({"error": "Provide a valid game action under 4 KB."}), 400
    try: action_id=str(uuid.UUID(str(action.get("client_action_id", ""))))
    except (ValueError, AttributeError, TypeError): return jsonify({"error":"A valid client_action_id UUID is required."}),400
    connection = db_connection(); cursor = connection.cursor()
    try:
        row = platform_session_row(cursor, session_id, user_id, lock=True)
        if not row: connection.rollback(); return jsonify({"error": "Session not found."}), 404
        cursor.execute("SELECT response_json FROM platform_game_attempts WHERE platform_session_id=%s AND client_action_id=%s", (session_id,action_id))
        previous_action=cursor.fetchone()
        if previous_action:
            cached=json.loads(previous_action[0]) if isinstance(previous_action[0],str) else previous_action[0]
            connection.rollback(); return jsonify(cached)
        game_id, subject, state_json, score, mistakes, started, completed, seconds, status, ended, accuracy, xp_awarded = row
        if status != "active": connection.rollback(); return jsonify({"error": "This session is no longer active."}), 409
        state = json.loads(state_json) if isinstance(state_json, str) else state_json
        if int(state.get("actions",0)) >= 500: connection.rollback(); return jsonify({"error":"This session reached its 500-action limit."}), 429
        level_index = int(state.get("level", 0))
        level_started = datetime.fromisoformat(state.get("level_started_at", started.isoformat()))
        response_seconds = max(0, min(86400, int((datetime.now() - level_started).total_seconds())))
        game = game_catalog.GAMES[game_id]
        state, feedback = game_catalog.apply_action(game_id, state, action)
        now = datetime.now()
        if feedback.get("correct") and not state.get("complete"):
            state["level_started_at"] = now.isoformat()
        elapsed = max(0, int((now - started).total_seconds()))
        done = bool(state.get("complete"))
        action_count = int(state.get("actions", 0))
        accuracy = round(sum(bool(event.get("correct")) for event in state.get("events", [])) * 100 / action_count, 2) if action_count else 0
        xp_awarded = max(0, int(state["score"] / 10) - state["mistakes"] * 2 + max(0, len(state.get("level_order", [])) * 2 - elapsed // 30)) if done else 0
        result={"state":state,"feedback":feedback,"complete":done,"status":"completed" if done else "active","accuracy":accuracy,"xp_awarded":xp_awarded,"seconds":elapsed}
        cursor.execute("INSERT INTO platform_game_attempts (platform_session_id,client_action_id,response_json,user_id,game_id,subject_code,level_index,topic,objective,correct,response_seconds) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (session_id,action_id,json.dumps(result),user_id,game_id,subject,level_index,game["title"],game["objective"],bool(feedback.get("correct")),response_seconds))
        cursor.execute("UPDATE platform_game_sessions SET state_json=%s,score=%s,accuracy=%s,mistakes=%s,xp_awarded=%s,status=%s,seconds=%s,completed_at=%s,ended_at=%s WHERE id=%s AND user_id=%s AND status='active'", (json.dumps(state),state["score"],accuracy,state["mistakes"],xp_awarded,"completed" if done else "active",elapsed,now if done else None,now if done else None,session_id,user_id))
        if cursor.rowcount != 1:
            connection.rollback(); return jsonify({"error": "This session is no longer active."}), 409
        connection.commit()
        return jsonify(result)
    except ValueError as error:
        connection.rollback(); return jsonify({"error": str(error)}), 400
    finally:
        cursor.close(); connection.close()


@app.get("/api/game-progress")
def platform_game_progress():
    user_id = current_user_id()
    if not user_id: return jsonify({"error": "Login required."}), 401
    connection = db_connection(); cursor = connection.cursor()
    cursor.execute("SELECT game_id,subject_code,COUNT(*),SUM(status='completed'),MAX(CASE WHEN status='completed' THEN score END),MAX(COALESCE(ended_at,started_at)),SUM(status='active'),SUM(xp_awarded) FROM platform_game_sessions WHERE user_id=%s GROUP BY game_id,subject_code ORDER BY subject_code,game_id", (user_id,))
    progress = [{"game_id":r[0],"subject":r[1],"plays":r[2],"completed":int(r[3] or 0),"best_score":r[4],"last_played":r[5].isoformat() if r[5] else None,"active":int(r[6] or 0),"xp_awarded":int(r[7] or 0)} for r in cursor.fetchall()]
    cursor.execute("SELECT COALESCE(SUM(xp_awarded),0),COUNT(*),COALESCE(SUM(seconds),0) FROM platform_game_sessions WHERE user_id=%s AND status='completed'", (user_id,)); platform_totals=cursor.fetchone()
    cursor.execute("SELECT COALESCE(SUM(xp_awarded),0),COUNT(*),COALESCE(SUM(seconds),0) FROM study_sessions WHERE user_id=%s AND status='completed'", (user_id,)); legacy_totals=cursor.fetchone()
    cursor.execute("SELECT COUNT(*),COALESCE(SUM(correct),0) FROM platform_game_attempts WHERE user_id=%s", (user_id,)); platform_attempts=cursor.fetchone()
    cursor.execute("SELECT COUNT(*),COALESCE(SUM(a.correct),0) FROM question_attempts a JOIN study_sessions s ON s.id=a.session_id WHERE s.user_id=%s AND s.status='completed'", (user_id,)); legacy_attempts=cursor.fetchone()
    cursor.execute("SELECT subject_code,COUNT(*),COALESCE(SUM(correct),0) FROM platform_game_attempts WHERE user_id=%s GROUP BY subject_code", (user_id,)); platform_subject_attempts={row[0]:{"attempts":int(row[1]),"correct":int(row[2])} for row in cursor.fetchall()}
    cursor.execute("SELECT a.subject_code,COUNT(*),COALESCE(SUM(a.correct),0) FROM question_attempts a JOIN study_sessions s ON s.id=a.session_id WHERE s.user_id=%s AND s.status='completed' GROUP BY a.subject_code", (user_id,)); legacy_subject_attempts={row[0]:{"attempts":int(row[1]),"correct":int(row[2])} for row in cursor.fetchall()}
    cursor.execute("SELECT DATE(completed_at) FROM platform_game_sessions WHERE user_id=%s AND status='completed' UNION SELECT DATE(completed_at) FROM study_sessions WHERE user_id=%s AND status='completed' ORDER BY 1", (user_id,user_id))
    completed_days=[row[0].isoformat() for row in cursor.fetchall()]
    cursor.execute("SELECT study_day,SUM(seconds) FROM (SELECT DATE(completed_at) AS study_day,seconds FROM platform_game_sessions WHERE user_id=%s AND status='completed' UNION ALL SELECT DATE(completed_at) AS study_day,seconds FROM study_sessions WHERE user_id=%s AND status='completed') AS completed GROUP BY study_day", (user_id,user_id))
    seconds_by_day={row[0].isoformat():int(row[1]) for row in cursor.fetchall()}
    cursor.close(); connection.close()
    subject_attempts={}
    for source in (platform_subject_attempts,legacy_subject_attempts):
        for subject,row in source.items():
            subject_attempts.setdefault(subject,{"attempts":0,"correct":0})
            subject_attempts[subject]["attempts"]+=row["attempts"];subject_attempts[subject]["correct"]+=row["correct"]
    return jsonify({"progress":progress,"platform_xp":int(platform_totals[0]),"legacy_xp":int(legacy_totals[0]),"completed_count":int(platform_totals[1])+int(legacy_totals[1]),"total_seconds":int(platform_totals[2])+int(legacy_totals[2]),"total_attempts":int(platform_attempts[0])+int(legacy_attempts[0]),"correct_attempts":int(platform_attempts[1])+int(legacy_attempts[1]),"subject_attempts":subject_attempts,"completed_days":completed_days,"seconds_by_day":seconds_by_day})


@app.post("/api/me/subjects")
def update_subjects():
    user_id = current_user_id()
    if not user_id: return jsonify({"error": "Login required."}), 401
    ids = (request.get_json(silent=True) or {}).get("subject_ids", [])
    if not isinstance(ids, list): return jsonify({"error": "subject_ids must be a list."}), 400
    connection = db_connection(); cursor = connection.cursor()
    cursor.execute("SELECT branch_id FROM users WHERE id=%s", (user_id,)); user_branch = cursor.fetchone()[0]
    chosen = []
    for subject_id in ids:
        if isinstance(subject_id, str) and not subject_id.isdigit():
            code = SUBJECT_CODE_ALIASES.get(subject_id, subject_id).upper()
            cursor.execute("SELECT id FROM subjects WHERE code=%s AND (branch_id=%s OR branch_id IS NULL) ORDER BY branch_id IS NULL LIMIT 1", (code, user_branch)); found = cursor.fetchone()
            if not found: connection.rollback(); cursor.close(); connection.close(); return jsonify({"error": f"Subject {code} is not available for your branch."}), 400
            subject_id = found[0]
        try: subject_id = int(subject_id)
        except (TypeError, ValueError): connection.rollback(); cursor.close(); connection.close(); return jsonify({"error": "Subject IDs must be valid integers."}), 400
        cursor.execute("SELECT id FROM subjects WHERE id=%s AND (branch_id=%s OR branch_id IS NULL) AND (code IN (" + ",".join(["%s"]*len(SUPPORTED_SUBJECT_CODES)) + ") OR created_by IS NOT NULL)", (subject_id, user_branch, *sorted(SUPPORTED_SUBJECT_CODES)))
        if not cursor.fetchone(): connection.rollback(); cursor.close(); connection.close(); return jsonify({"error": "A selected subject is not available for your branch."}), 400
        chosen.append(subject_id)
    cursor.execute("DELETE FROM user_subjects WHERE user_id=%s", (user_id,))
    for subject_id in set(chosen): cursor.execute("INSERT INTO user_subjects (user_id, subject_id) VALUES (%s,%s)", (user_id, subject_id))
    connection.commit(); cursor.close(); connection.close(); return jsonify({"ok": True})


@app.post("/api/subjects")
def create_subject():
    if not current_user_id(): return jsonify({"error": "Login required."}), 401
    connection = db_connection(); cursor = connection.cursor(); cursor.execute("SELECT role FROM users WHERE id=%s", (current_user_id(),)); role = cursor.fetchone()[0]
    if role != "teacher": cursor.close(); connection.close(); return jsonify({"error": "Only teachers can add subjects."}), 403
    data = request.get_json(silent=True) or {}; name = str(data.get("name", "")).strip(); code = str(data.get("code", "")).strip().upper(); branch = str(data.get("branch", "")).strip().lower()
    if not name or len(name) > 160 or not re.fullmatch(r"[A-Z][A-Z0-9_-]{1,59}", code): cursor.close(); connection.close(); return jsonify({"error": "Enter a subject name and a code using 2–60 letters, digits, underscores, or hyphens."}), 400
    if branch and branch not in BRANCHES: cursor.close(); connection.close(); return jsonify({"error": "Choose a valid computing branch/course."}), 400
    branch_id = None
    if branch: cursor.execute("SELECT id FROM branches WHERE code=%s", (branch,)); found = cursor.fetchone(); branch_id = found[0] if found else None
    try:
        cursor.execute("INSERT INTO subjects (code,name,branch_id,created_by) VALUES (%s,%s,%s,%s)", (code, name, branch_id, current_user_id())); subject_id = cursor.lastrowid; connection.commit()
    except mysql.connector.IntegrityError: connection.rollback(); cursor.close(); connection.close(); return jsonify({"error": "That subject already exists for this branch."}), 409
    cursor.close(); connection.close(); return jsonify({"id": subject_id, "code": code, "name": name}), 201


@app.post("/api/sessions")
def record_session():
    user_id = current_user_id()
    if not user_id: return jsonify({"error": "Login required."}), 401
    data = request.get_json(silent=True)
    if not isinstance(data, dict): return jsonify({"error":"Provide a valid session result."}), 400
    client_session_id = str(data.get("client_session_id", ""))
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", client_session_id): return jsonify({"error":"A valid client_session_id is required."}), 400
    status = data.get("status", "completed")
    if status not in {"completed", "abandoned"}: return jsonify({"error":"Session status must be completed or abandoned."}), 400
    try:
        accuracy = max(0, min(100, float(data.get("accuracy", 0))))
        seconds = max(0, min(86400, int(data.get("seconds", 0))))
        points = max(0, min(1000000, int(data.get("points", 0)))) if status == "completed" else 0
        xp_awarded = max(0, min(1000000, int(data.get("xp_awarded", 0)))) if status == "completed" else 0
        attempts = data.get("attempts", [])
        if not isinstance(attempts, list) or len(attempts) > 500 or any(not isinstance(attempt, dict) for attempt in attempts): raise ValueError
        if not 0 <= accuracy <= 100: raise ValueError
        normalized_attempts=[]
        for attempt in attempts:
            response_seconds=max(0,min(86400,int(attempt.get("response_seconds",0))))
            correct=attempt.get("correct")
            if not isinstance(correct,bool): raise ValueError
            normalized_attempts.append((attempt,response_seconds,correct))
    except (TypeError, ValueError, OverflowError):
        return jsonify({"error":"Session metrics or attempts are invalid."}), 400
    connection = db_connection(); cursor = connection.cursor()
    try:
        cursor.execute("INSERT IGNORE INTO study_sessions (user_id,client_session_id,subject_code,game_type,status,accuracy,seconds,points,xp_awarded) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (user_id,client_session_id,str(data.get("subject_code", ""))[:60],str(data.get("game_type", "quiz"))[:40],status,accuracy,seconds,points,xp_awarded))
        inserted = cursor.rowcount == 1
        if inserted:
            session_id = cursor.lastrowid
            for attempt,response_seconds,correct in normalized_attempts:
                cursor.execute("INSERT INTO question_attempts (session_id,user_id,subject_code,topic,correct,response_seconds) VALUES (%s,%s,%s,%s,%s,%s)", (session_id,user_id,str(attempt.get("subject_code", data.get("subject_code", "")))[:60],str(attempt.get("topic", "General"))[:160],correct,response_seconds))
        else:
            cursor.execute("SELECT id FROM study_sessions WHERE user_id=%s AND client_session_id=%s", (user_id,client_session_id))
            row = cursor.fetchone()
            if not row: raise RuntimeError("Unable to find the existing session result.")
            session_id = row[0]
        connection.commit()
        return jsonify({"ok": True, "session_id": session_id, "duplicate": not inserted}), 201 if inserted else 200
    except ValueError:
        connection.rollback(); return jsonify({"error":"Session metrics or attempts are invalid."}), 400
    except Exception:
        connection.rollback(); raise
    finally:
        cursor.close(); connection.close()


@app.get("/api/teacher/analytics")
def teacher_analytics():
    user_id = current_user_id()
    if not user_id: return jsonify({"error": "Login required."}), 401
    connection = db_connection(); cursor = connection.cursor(); cursor.execute("SELECT role FROM users WHERE id=%s", (user_id,))
    if cursor.fetchone()[0] != "teacher": cursor.close(); connection.close(); return jsonify({"error": "Teacher access required."}), 403
    cursor.execute("SELECT subject_code, COUNT(*), ROUND(AVG(accuracy),1), ROUND(AVG(points),0) FROM study_sessions WHERE status='completed' GROUP BY subject_code ORDER BY subject_code")
    completion = [{"subject_code": r[0], "sessions": r[1], "accuracy": float(r[2] or 0), "average_points": int(r[3] or 0)} for r in cursor.fetchall()]
    cursor.execute("SELECT a.subject_code, a.topic, COUNT(*), ROUND(AVG(a.correct)*100,1) FROM question_attempts a JOIN study_sessions s ON s.id=a.session_id WHERE s.status='completed' GROUP BY a.subject_code,a.topic HAVING AVG(a.correct)<0.7 ORDER BY AVG(a.correct)")
    weak_topics = [{"subject_code": r[0], "topic": r[1], "attempts": r[2], "accuracy": float(r[3] or 0)} for r in cursor.fetchall()]
    cursor.execute("SELECT a.subject_code, a.topic, COUNT(*), ROUND(AVG(a.correct)*100,1) FROM question_attempts a JOIN study_sessions s ON s.id=a.session_id WHERE s.status='completed' GROUP BY a.subject_code,a.topic ORDER BY COUNT(*) DESC")
    question_quality = [{"subject_code": r[0], "topic": r[1], "attempts": r[2], "accuracy": float(r[3] or 0)} for r in cursor.fetchall()]
    cursor.execute("SELECT subject_code,topic,COUNT(*),ROUND(AVG(correct)*100,1),ROUND(AVG(response_seconds),1) FROM platform_game_attempts GROUP BY subject_code,topic HAVING AVG(correct)<0.7 ORDER BY AVG(correct)")
    weak_topics.extend({"subject_code":r[0],"topic":r[1],"attempts":r[2],"accuracy":float(r[3] or 0),"average_response_seconds":float(r[4] or 0),"source":"platform"} for r in cursor.fetchall())
    cursor.execute("SELECT subject_code,topic,COUNT(*),ROUND(AVG(correct)*100,1),ROUND(AVG(response_seconds),1) FROM platform_game_attempts GROUP BY subject_code,topic ORDER BY COUNT(*) DESC")
    question_quality.extend({"subject_code":r[0],"topic":r[1],"attempts":r[2],"accuracy":float(r[3] or 0),"average_response_seconds":float(r[4] or 0),"source":"platform"} for r in cursor.fetchall())
    cursor.execute("SELECT subject_code, COUNT(*), SUM(completed_at IS NOT NULL), ROUND(AVG(score),1), COUNT(DISTINCT user_id) FROM platform_game_sessions GROUP BY subject_code ORDER BY subject_code")
    platform = [{"subject_code":r[0],"sessions":r[1],"completed":int(r[2] or 0),"average_score":float(r[3] or 0),"students":r[4]} for r in cursor.fetchall()]
    cursor.execute("SELECT COUNT(*), COUNT(DISTINCT user_id) FROM study_sessions")
    legacy_sessions, legacy_students = cursor.fetchone()
    cursor.execute("SELECT COUNT(*), COUNT(DISTINCT user_id) FROM platform_game_sessions")
    platform_sessions, platform_students = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM (SELECT user_id FROM study_sessions UNION SELECT user_id FROM platform_game_sessions) activity_users")
    active_students = cursor.fetchone()[0]; cursor.close(); connection.close()
    return jsonify({"class_performance": {"students": active_students, "sessions": (legacy_sessions or 0) + (platform_sessions or 0)}, "completion": completion, "platform_completion": platform, "weak_topics": weak_topics, "question_quality": question_quality})


@app.get("/api/teacher/games")
def teacher_games():
    user_id = current_user_id()
    if not user_id: return jsonify({"error": "Login required."}), 401
    connection = db_connection(); cursor = connection.cursor(); cursor.execute("SELECT role FROM users WHERE id=%s", (user_id,)); row = cursor.fetchone()
    if not row or row[0] != "teacher": cursor.close(); connection.close(); return jsonify({"error": "Teacher access required."}), 403
    cursor.execute("SELECT g.id,g.title,g.game_type,g.content_json,s.code,s.name,b.name FROM games g JOIN subjects s ON s.id=g.subject_id LEFT JOIN branches b ON b.id=s.branch_id ORDER BY g.id DESC LIMIT 200")
    games = []
    for r in cursor.fetchall():
        content = json.loads(r[3]) if isinstance(r[3], str) else r[3]
        games.append({"id":r[0],"title":r[1],"game_type":r[2],"content":content,"subject_code":r[4],"subject_name":r[5],"branch_name":r[6]})
    cursor.close(); connection.close(); return jsonify({"games":games})


@app.post("/api/games")
def create_game():
    user_id = current_user_id()
    if not user_id: return jsonify({"error": "Login required."}), 401
    connection = db_connection(); cursor = connection.cursor(); cursor.execute("SELECT role FROM users WHERE id=%s", (user_id,))
    if cursor.fetchone()[0] != "teacher": cursor.close(); connection.close(); return jsonify({"error": "Teacher access required."}), 403
    data = request.get_json(silent=True) or {}; subject_id = data.get("subject_id"); title = str(data.get("title", "")).strip(); game_type = str(data.get("game_type", "quiz")).strip(); content = data.get("content", {})
    if not subject_id or not title or len(title) > 160 or game_type not in ("quiz", "flashcards", "challenge", "coding", "fill", "typing") or not isinstance(content, dict) or len(json.dumps(content)) > 32000:
        cursor.close(); connection.close(); return jsonify({"error": "Subject, title, game type, and valid content are required."}), 400
    cursor.execute("SELECT 1 FROM subjects WHERE id=%s AND (code IN (" + ",".join(["%s"]*len(SUPPORTED_SUBJECT_CODES)) + ") OR created_by=%s)", (int(subject_id), *sorted(SUPPORTED_SUBJECT_CODES), user_id))
    if not cursor.fetchone(): cursor.close(); connection.close(); return jsonify({"error": "Choose an active computing subject."}), 400
    cursor.execute("INSERT INTO games (subject_id,title,game_type,content_json) VALUES (%s,%s,%s,%s)", (int(subject_id), title, game_type, json.dumps(content)))
    game_id = cursor.lastrowid; connection.commit(); cursor.close(); connection.close(); return jsonify({"id": game_id, "title": title}), 201


@app.get("/")
def index(): return send_from_directory(FRONTEND, "index.html")


@app.get("/games.js")
def game_platform_js(): return send_from_directory(FRONTEND, "games.js")


@app.get("/legacy-game-content.js")
def legacy_game_content_js(): return send_from_directory(FRONTEND, "legacy-game-content.js")


@app.get("/rotating-game-content.js")
def rotating_game_content_js(): return send_from_directory(FRONTEND, "rotating-game-content.js")


@app.get("/typing-programs.js")
def typing_programs_js(): return send_from_directory(FRONTEND, "typing-programs.js")


@app.get("/images/<path:filename>")
def images(filename): return send_from_directory(FRONTEND / "images", filename)


if __name__ == "__main__":
    ensure_database(); ensure_schema()
    app.run(host=os.getenv("APP_HOST", "127.0.0.1"), port=int(os.getenv("APP_PORT", "5000")), debug=os.getenv("FLASK_DEBUG", "0") == "1")
