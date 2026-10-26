# Implementation status and follow-up

## Implemented

- [x] Preserved the existing SPA/dashboard design and local quizzes, flashcards, timed challenges, XP, levels, streaks, achievements, history and recommendations.
- [x] Kept the root `py app.py` launch flow, Flask/MySQL, `.env.example`, `.gitignore`, requirements, and automatic additive schema/database setup.
- [x] Kept email unique, hashed passwords, session login/logout, no email verification, and non-overwriting development seed accounts.
- [x] Added six computing-oriented branch/course choices and branch-to-subject database mappings.
- [x] Added editable student subjects; DSA language is selectable between C++ and Java and saved in platform session state/history.
- [x] Added 32 distinct server-validated platform activities covering the 16 named computing subjects. The full 16-game status table and activity mechanics are in `MULTI_SUBJECT_GAMES.md`.
- [x] Added MySQL-backed game state/history, owner checks, completion/replay protection, server-side scoring, hints and explanations.
- [x] Added teacher-only subject/content routes, a saved-content list and platform/legacy analytics summaries.
- [x] Added unit, renderer, API-contract and opt-in MySQL integration checks; updated setup, API, architecture, deployment and formal report documents.

## Verified in this run

- Python unittest suite: passed; MySQL test is opt-in in the default run.
- Frontend renderer tests: passed for every platform mechanic.
- Python module compilation and frontend JavaScript syntax: passed.
- Opt-in local MySQL integration: passed for session persistence, scoring, ownership and replay protection.

## Remaining limitations

- [ ] User code is not compiled or executed; no hidden runtime tests, true partial execution scoring or resource-limited compiler service.
- [ ] Teacher-added game rows are saved and reviewable but do not dynamically become playable platform mechanics.
- [ ] Legacy `/api/sessions` trusts the browser-reported summary for local game modes.
- [ ] Real browser E2E across all routes and games, real device/responsive QA, and screen-reader audit remain to be run.
- [ ] Evaluation protocol exists, but no participant study or learning-improvement result exists.

Existing historic subject/game rows are preserved. The app filters retired nontechnical subject codes from the active subject catalog; no destructive cleanup migration is used.
