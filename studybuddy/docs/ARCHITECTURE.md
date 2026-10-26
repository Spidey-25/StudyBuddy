# Architecture

```mermaid
flowchart TD
  Browser[Vanilla JS frontend<br/>dashboard and game renderers] -->|HTTP JSON + session cookie| Flask[Flask application]
  Flask --> Auth[Registration and authentication]
  Flask --> Catalog[Public game catalog]
  Flask --> Validator[Private per-mechanic validators]
  Flask --> Teacher[Teacher content and analytics routes]
  Auth --> DB[(MySQL)]
  Validator --> DB
  Teacher --> DB
  DB --> Users[users]
  DB --> Branches[branches]
  DB --> Subjects[subjects]
  Users --> UserSubjects[user_subjects]
  Subjects --> UserSubjects
  Subjects --> Games[games: teacher-created content]
  Users --> PlatformSessions[platform_game_sessions]
  Users --> LegacySessions[study_sessions and question_attempts]
```

```mermaid
erDiagram
  BRANCHES ||--o{ USERS : enrolls
  BRANCHES ||--o{ SUBJECTS : offers
  USERS ||--o{ USER_SUBJECTS : selects
  SUBJECTS ||--o{ USER_SUBJECTS : selected_by
  SUBJECTS ||--o{ GAMES : contains
  USERS ||--o{ PLATFORM_GAME_SESSIONS : plays
  PLATFORM_GAME_SESSIONS ||--o{ PLATFORM_GAME_ATTEMPTS : records
  USERS ||--o{ STUDY_SESSIONS : records
  STUDY_SESSIONS ||--o{ QUESTION_ATTEMPTS : contains
```

The root `app.py` initializes the configured MySQL database and additive schema, then starts Flask. Authentication uses a signed HTTP-only session cookie; password hashes are generated with Werkzeug. The frontend keeps its existing local study-mode model and UI. The platform catalog is fetched from Flask, with each activity rendered by a dedicated mechanic in `frontend/games.js`.

For platform games, the browser receives public prompt data only. Flask retains the answer rules, reloads the session by authenticated owner, validates each action, computes score and persists progress. The DSA language selection is included in saved session state. Teacher analytics are role-gated and aggregate both legacy session summaries and platform game runs.

**Trust boundary:** platform game scores are server-computed. The legacy `/api/sessions` endpoint still accepts browser-reported score and accuracy for the original local game modes. Code activities are prepared-response exercises and do not run arbitrary source code. Teacher-created rows in `games` can be reviewed in the teacher panel but are not dynamically added to the platform catalog.
