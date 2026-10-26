# Testing

## Automated checks

```powershell
py -m unittest discover -s tests -v
node --test tests/test_frontend_games.js
node --check frontend/games.js
py -m py_compile app.py backend/app.py backend/game_catalog.py
```

Extract the final inline script from `frontend/index.html` and run `node --check` on it when editing that file. The automated suite covers API contracts, authentication route availability, branch-subject relationships, catalog answer redaction, every game-level validator, incorrect actions, score/completion rules, adaptive scoring helpers, accessibility markup, and rendering of all platform mechanics.

## MySQL integration test

Set `PLATFORM_MYSQL_INTEGRATION=1` and run:

```powershell
$env:PLATFORM_MYSQL_INTEGRATION = '1'
py -m unittest tests.test_platform_mysql_integration -v
py -m unittest tests.test_end_to_end -v
Remove-Item Env:PLATFORM_MYSQL_INTEGRATION
```

The integration tests initialize the configured schema and check MySQL-backed registration/login/logout, subject selection, DSA language persistence, teacher permissions/content, game scoring/completion, duplicate-action rejection, account isolation, and progress/history. Temporary accounts, subjects and sessions are removed afterward. Use a local development database and do not point these tests at production data.

## Current limitations and manual checklist

- The end-to-end flow uses Flask's test client against MySQL. Automated frontend checks render game HTML in Node; they do not click through a real browser or verify mobile screen sizes.
- Run a manual browser pass at narrow-phone, tablet and desktop widths. Check login/register, subject editing, all local study modes, each platform game, DSA C++/Java persistence, reload/resume, teacher content and analytics, logout, and history.
- Keyboard-check every control, focus order, visible focus, error/status announcements, zoom to 200%, and reduced-motion mode. A screen-reader audit has not yet been performed.
- The MySQL-backed integration test is opt-in and requires local MySQL access.
- The evaluation-study plan is documented, but there are no participant or learning-outcome results.
- Arbitrary code execution is intentionally unavailable. Do not implement it inside Flask.
