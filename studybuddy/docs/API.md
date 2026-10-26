# StudyBuddy API

All JSON routes are served from Flask and use the HTTP-only session cookie for authentication.

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/health` | MySQL health check |
| GET | `/api/branches` | Active technical branches/courses |
| POST | `/api/register` | Register student or teacher; no email verification |
| POST | `/api/login` | Email/password login |
| POST | `/api/logout` | Clear the session |
| GET | `/api/me` | Current user and chosen subjects |
| GET | `/api/subjects?branch=cse` | Subject catalog, optionally filtered to branch |
| POST | `/api/me/subjects` | Replace student's allowed subject choices |
| POST | `/api/subjects` | Teacher-only subject creation |
| POST | `/api/games` | Teacher-only saved game/stage content |
| GET | `/api/teacher/games` | Teacher-only saved game content list |
| POST | `/api/sessions` | Legacy local-mode summary endpoint |
| GET | `/api/teacher/analytics` | Teacher-only session and topic aggregates |
| GET | `/api/game-catalog?subject=DSA` | Public prompts and game metadata (answer keys removed) |
| POST | `/api/game-sessions` | Start a game; DSA requires `language: "C++"` or `"Java"` |
| GET | `/api/game-sessions` | List current user's recent sessions |
| GET | `/api/game-sessions/<id>` | Read only the current user's session/result |
| POST | `/api/game-sessions/<id>/action` | Validate and persist one game action |
| GET | `/api/game-progress` | Current user's counts, completion, best score and last play |

Platform game requests are authenticated and session IDs are owner-scoped. Flask computes score from validated actions; clients cannot submit a score or completion flag. Completed sessions reject more actions. DSA language is stored in the session JSON. The legacy `/api/sessions` route still accepts client-reported result summaries for the browser-local game modes; do not treat those summaries as tamper-proof.

Coding exercises are constrained prepared-response tasks. No arbitrary source code is compiled or run. Teacher content rows are stored and reviewable, but are not dynamically converted into platform-game mechanics.
