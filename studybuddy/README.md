# StudyBuddy

A college computing study app with a preserved dashboard, quizzes, flashcards, timed challenges, XP, levels, streaks, achievements, history, recommendations, and a MySQL-backed platform of distinct educational games.

## Run locally

Requirements: Python 3.10+, MySQL 8, and permission for the MySQL account to create a database.

```powershell
Copy-Item .env.example .env
# Edit .env with a private SECRET_KEY and your MySQL credentials.
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py app.py
```

Open `http://127.0.0.1:5000`. The root launcher automatically creates the configured database and missing tables, adds current branches and subjects, and seeds development users without replacing an existing account:

- Student: `student@example.com` / `Student@123`
- Teacher: `teacher@example.com` / `Teacher@123`

Keep `.env` private and change the demonstration passwords before sharing the app outside your machine.

## Subjects and games

Active courses cover C, C++, Java, Python, DSA, DBMS, Operating Systems, Computer Networks, Web Development, Software Engineering, AI, ML, Cybersecurity, Cloud Computing, Embedded Systems, and IoT. Branch-to-subject relationships are stored in MySQL; students can change their selected subjects from My Subjects. DSA activities let students choose C++ or Java and persist that choice with session history.

There are **32 platform games** across 16 technical subjects. Every game has at least four distinct levels across progressive difficulty; Python Logic Builder has twelve varied tasks. Sessions randomize questions within difficulty and avoid repeating the previous run's final question first. The catalog includes code repair/output tracing, OOP design, logic construction, algorithm sequencing/data-structure tracing, SQL/ER design, CPU scheduling/memory allocation, packet routing/troubleshooting, and responsive UI debugging. Games use dedicated mechanics including code edits, trace input, sequence controls, design choices, route construction, query entry and allocation inputs, with server-side validation, scoring, hints, feedback and MySQL history.

The existing local study app retains its quiz, flashcard, timed challenge, code sequencing, missing-line, typing, XP, streak, achievement, chart, recommendation and review flows. Browser-local progress is stored under `studybuddy.v1`; platform game state is persisted in MySQL.

## Project files

- `app.py`: launcher; creates database/schema before serving.
- `backend/app.py`: Flask API, auth, MySQL schema, teacher routes.
- `backend/game_catalog.py` and `backend/game_content.py`: platform catalog, authored content, public sanitization and private validators.
- `backend/migrations/`: additive SQL migrations.
- `frontend/index.html`: existing SPA, dashboard and local games.
- `frontend/games.js`: dedicated renderer for each platform mechanic.
- `tests/`: unit, renderer, API contract and opt-in MySQL integration tests.
- `docs/`: API, architecture/ER diagrams, deployment, testing and project report.
- `docs/GAME_CATALOG_AUDIT.md`: game-by-game implementation, content-count and test matrix.

## Verification commands

```powershell
py -m unittest discover -s tests -v
node --test tests/test_frontend_catalog.js tests/test_frontend_games.js
node --check frontend/games.js
py -m py_compile app.py backend/app.py backend/game_catalog.py backend/game_content.py backend/code_checks.py
$env:PLATFORM_MYSQL_INTEGRATION = '1'
py -m unittest tests.test_platform_mysql_integration -v
py -m unittest tests.test_end_to_end -v
Remove-Item Env:PLATFORM_MYSQL_INTEGRATION
```

The MySQL tests require the configured local server and remove temporary sessions, results, accounts, subjects and teacher content.

## Points and recommendations

Existing local-mode XP rules award only an improved best result. Platform game XP, best scores, completion counts, accuracy and time are computed and stored by Flask; XP rewards are committed once when a session completes. Account progress combines platform totals with the preserved browser-local progress.

## Limits to understand

The app does not compile or execute learner-submitted code. Code-edit activities use private, deterministic checks for their authored exercises, including arithmetic and known program patterns; they are not a general compiler or runtime, and do not enforce execution limits. Teacher-created content can be saved and reviewed, but it is not dynamically turned into platform mechanics. The legacy `/api/sessions` route accepts browser-reported summaries for local modes. Browser/device, screen-reader and learning-outcome studies have not been completed. See [the project report](docs/PROJECT_REPORT.md), [testing checklist](docs/TESTING.md), and [evaluation plan](docs/EVALUATION_STUDY.md).
