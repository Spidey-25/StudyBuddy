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
| POST | `/api/game-sessions/<id>/exit` | Close an active session as `exited` or `abandoned` |
| GET | `/api/game-progress` | Current user's counts, completion, best score and last play |

Platform game requests are authenticated and session IDs are owner-scoped. Each action must include a UUID `client_action_id`; replaying that identifier returns the original response without applying the action twice. Flask computes score, accuracy, completion status, duration, and XP from validated actions; clients cannot submit those results. A completed, exited, or abandoned session cannot accept new actions. Starting a new game closes any previous active session as abandoned. Refreshing the page keeps an active session resumable; leaving the game through SPA navigation closes it. DSA language is stored in the session JSON.

Local game summaries sent to `/api/sessions` must include a stable `client_session_id`, a `status` (`completed` or `abandoned`), and the final metrics. The `(user_id, client_session_id)` key makes retries idempotent; attempts are stored only for the first accepted result. Legacy local-mode scores remain browser-reported and are not tamper-proof.

Coding exercises are constrained prepared-response tasks. No arbitrary source code is compiled or run. Teacher content rows are stored and reviewable, but are not dynamically converted into platform-game mechanics.
