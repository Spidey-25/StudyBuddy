# Testing

## Automated checks

```powershell
py -m unittest discover -s tests -v
node --test tests/test_frontend_catalog.js tests/test_frontend_games.js
node --check frontend/games.js
py -m py_compile app.py backend/app.py backend/game_catalog.py backend/game_content.py backend/code_checks.py
```

Extract the final inline script from `frontend/index.html` and run `node --check` on it when editing that file. The Python suite covers all 32 platform IDs and mechanic mappings, all platform-level validators, private code-check fixtures, answer redaction, route/session lifecycle contracts, local-result idempotency, score/completion rules, adaptive scoring helpers and accessibility markup. Node checks all 66 local cards for unique routing, populated mechanics banks, valid answer structures and inline-script syntax, and renders every platform mechanic. Opt-in MySQL tests start each platform catalog game, exercise terminal session states and replayed actions, verify single-write results/rewards, and test login, registration and ownership.

## MySQL integration test

Set `PLATFORM_MYSQL_INTEGRATION=1` and run:

```powershell
$env:PLATFORM_MYSQL_INTEGRATION = '1'
py -m unittest tests.test_platform_mysql_integration -v
py -m unittest tests.test_end_to_end -v
Remove-Item Env:PLATFORM_MYSQL_INTEGRATION
```

The integration tests initialize the configured schema and check MySQL-backed registration/login/logout, subject selection, DSA language persistence, teacher permissions/content, each catalog route, game scoring/completion, duplicate-action replay, exit and abandonment, exact-once local results, account isolation, and progress/history. Temporary accounts, subjects, sessions and summaries are removed afterward. Use a local development database and do not point these tests at production data.

## Current limitations and manual checklist

- The end-to-end flow uses Flask's test client against MySQL. Automated frontend checks render game HTML in Node; they do not click through a real browser or verify mobile screen sizes.
- Run a manual browser pass at narrow-phone, tablet and desktop widths. Check login/register, subject editing, all local study modes, each platform game, DSA C++/Java persistence, reload/resume, teacher content and analytics, logout, and history.
- Keyboard-check every control, focus order, visible focus, error/status announcements, zoom to 200%, and reduced-motion mode. A screen-reader audit has not yet been performed.
- The MySQL-backed integration test is opt-in and requires local MySQL access.
- The evaluation-study plan is documented, but there are no participant or learning-outcome results.
- Arbitrary code execution is intentionally unavailable. Do not implement it inside Flask.
