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

There are **32 platform games** across 16 technical subjects. The required 16-game set includes code repair/output tracing, OOP design, Python debugging/logic construction, algorithm sequencing/data-structure tracing, SQL/ER design, CPU scheduling/memory allocation, packet routing/troubleshooting, and a constrained coding playground/UI debugging. Other enabled subjects also have two subject-specific games. These are not one MCQ template: games use code edits, trace input, sequence controls, design choices, route construction, query entry and allocation inputs, with server-side validation, scoring, hints, feedback, retry, and MySQL history.

The existing local study app retains its quiz, flashcard, timed challenge, code sequencing, missing-line, typing, XP, streak, achievement, chart, recommendation and review flows. Browser-local progress is stored under `studybuddy.v1`; platform game state is persisted in MySQL.

## Project files

- `app.py`: launcher; creates database/schema before serving.
- `backend/app.py`: Flask API, auth, MySQL schema, teacher routes.
- `backend/game_catalog.py`: platform game data, public sanitization and private validators.
- `backend/migrations/`: additive SQL migrations.
- `frontend/index.html`: existing SPA, dashboard and local games.
- `frontend/games.js`: dedicated renderer for each platform mechanic.
- `tests/`: unit, renderer, API contract and opt-in MySQL integration tests.
- `docs/`: API, architecture/ER diagrams, deployment, testing and project report.

## Verification commands

```powershell
py -m unittest discover -s tests -v
node --test tests/test_frontend_games.js
node --check frontend/games.js
py -m py_compile app.py backend/app.py backend/game_catalog.py
$env:PLATFORM_MYSQL_INTEGRATION = '1'
py -m unittest tests.test_platform_mysql_integration -v
py -m unittest tests.test_end_to_end -v
Remove-Item Env:PLATFORM_MYSQL_INTEGRATION
```

The MySQL test requires the configured local server and removes its temporary game session.

## Points and recommendations

Existing local-mode XP rules award only an improved best result, use an accuracy-scaled cap, and count streaks by distinct local calendar day. Recommendations use selected subjects, repeated weak topics, due flashcards, session duration, newness and recent activity. The platform game's score is a separate server-computed points total (100 for each passed level).

## Limits to understand

The app does not compile or execute learner-submitted code. Code tasks compare input with prepared expected responses; they do not implement hidden runtime tests, partial runtime scoring or compiler CPU/memory limits. Teacher-created content can be saved and reviewed, but it is not dynamically turned into platform mechanics. The legacy `/api/sessions` route accepts browser-reported summaries for local modes. Browser/mobile, screen-reader and learning-outcome studies have not been completed. See [the project report](docs/PROJECT_REPORT.md), [testing checklist](docs/TESTING.md), and [evaluation plan](docs/EVALUATION_STUDY.md).
