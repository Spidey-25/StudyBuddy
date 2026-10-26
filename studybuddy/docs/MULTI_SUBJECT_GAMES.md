# StudyBuddy technical game platform

The Flask catalog has 32 server-validated activities across 16 computing subjects. The following 16 are the required core set; eight additional subjects each add two more. Each game has a separate player interaction, prepared game rules, a score, hints, explanatory feedback, saved sessions, results and retry.

| Subject / game | Frontend | Playable mechanic | Backend validation | MySQL persistence | Test coverage |
|---|---|---|---|---|---|
| C++ — Code Debugger | Dedicated code-edit renderer | Replace a faulty statement | Prepared expected line | Session, score, events | Every level + renderer type |
| C++ — Output & Logic Challenge | Output input renderer | Trace integer and post-increment output | Exact expected output | Session, score, events | Every level + renderer type |
| Java — Code Debugger | Dedicated code-edit renderer | Repair predicate or accumulator | Prepared expected line | Session, score, events | Every level + renderer type |
| Java — Object-Oriented Design Lab | Design-choice renderer | Choose encapsulation/interface design | Server-side choice key | Session, score, events | Every level + renderer type |
| Python — Debugging Lab | Dedicated code-edit renderer | Repair a prepared Python logic line | Prepared expected line | Session, score, events | Every level + renderer type |
| Python — Logic Builder | Reorder controls | Assemble a Boolean condition | Exact block order | Session, score, events | Every level + renderer type |
| DSA — Algorithm Arena | Reorder controls | Order binary-search and BFS steps | Exact sequence | Session, score, events, language | Every level + renderer type |
| DSA — Data Structure Visualizer | Trace input renderer | Apply stack/queue operations; enter final contents | Expected resulting state | Session, score, events, language | Every level + renderer type |
| DBMS — SQL Query Lab | SQL editor | Enter a query for a given schema/task | Prepared normalized query match | Session, score, events | Every level + renderer type |
| DBMS — ER Diagram Builder | Design-choice renderer | Choose relationship cardinality | Server-side choice key | Session, score, events | Every level + renderer type |
| OS — CPU Scheduling Simulator | Reorder controls | Arrange processes by non-preemptive SJF | Server-computed burst order | Session, score, events | Every level + renderer type |
| OS — Memory Allocation Challenge | Allocation inputs | Apply first-fit while tracking remaining blocks | Server-simulated allocation | Session, score, events | Every level + renderer type |
| Computer Networks — Packet Routing Simulator | Route input renderer | Build shortest valid path using available links | Link/path validation | Session, score, events | Every level + renderer type |
| Computer Networks — Network Troubleshooting Lab | Diagnosis choices | Diagnose a layered connectivity issue | Server-side diagnosis key | Session, score, events | Every level + renderer type |
| Web Development — Web Coding Playground | Code-edit renderer | Complete constrained HTML/CSS/JS exercises | Prepared expected answer | Session, score, events | Every level + renderer type |
| Web Development — UI Debugging Challenge | UI-fix choices | Select responsive/accessibility repair | Server-side choice key | Session, score, events | Every level + renderer type |

Additional enabled subjects: C (Code Debugger, Memory Trace); Software Engineering (Requirements Prioritizer, Test Design Lab); AI (Inference Trace, Feature Selection Lab); ML (Metric Match, Overfit Repair Lab); Cybersecurity (Incident Response, Phishing Defense); Cloud (Architecture Builder, Cost Estimator); Embedded Systems (Interrupt Trace, Pin Mapping); IoT (Protocol Lab, Topology Builder).

## Request and scoring flow

1. `GET /api/game-catalog` returns public instructions, choices, prompts, hints, and objectives. Answer keys are removed.
2. An authenticated learner starts a session with `POST /api/game-sessions`. DSA requires the learner to choose C++ or Java; the selection is persisted with the session.
3. The client submits a game-specific action to `POST /api/game-sessions/<id>/action`.
4. Flask reloads authoritative state from MySQL, validates the action using private rules, awards 100 points for a passed level, records mistakes and explanatory feedback, then commits.
5. The session owner can read history/results and progress. Another account cannot access it; completed sessions reject new actions.

## Coding execution boundary

Code repair and coding-playground activities compare submitted text with prepared responses and display sample expectations. They do not compile or execute submitted code and do not provide hidden runtime tests, resource limits, or general-purpose partial execution scoring. Arbitrary learner source is never executed in Flask or against the app database. A future executable mode needs a separately isolated runner; enabling `subprocess` in Flask is not acceptable.

## Persistence and content

`backend/game_catalog.py` stores definitions and private rules. `platform_game_sessions` stores per-user game state and results; `platform_game_attempts` stores server-validated per-level outcomes and response time for teacher analytics. Branch and subject links use `branches`, `subjects`, and `user_subjects`. Migrations `005_computing_course_catalog.sql` and `006_platform_game_attempts.sql` add active technical subjects and per-level analytics additively. Existing unrelated legacy database rows are retained but hidden from active subject selection. Existing frontend-local quiz/flashcard/challenge, XP, streak and achievement flows remain separate.

Teacher-added content is stored in the `games` table and listed in the teacher panel. It is not dynamically compiled into the deterministic platform catalog; teacher content does not yet appear as student-playable platform games.
