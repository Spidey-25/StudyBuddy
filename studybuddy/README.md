# StudyBuddy

Gamified college study app: quizzes, flashcards and timed challenges with XP, levels, streaks, achievements, history, mistake review and progress charts.

This folder is the **working single-file app** (demo mode). It is not the full Next.js/Supabase build.

## Run it
Open `index.html` in a browser, or run `npm start` (serves the folder with `npx serve`).
Data is saved in your browser's localStorage under the key `studybuddy.v1`. Reset it in Profile & Settings.

## What is included
- `index.html`: the app (HTML, CSS and JS in one file; no build step)
- `tests/smoke.test.js`: scripted test of setup, pages, quiz, flashcards, retry, XP rules and saving (`npm install` then `npm test`)
- `prototypes/`: the two earlier visual prototypes, for reference
- `.env.example`: placeholders for the future Supabase version

## Features
Light-theme-only app with a typed-text welcome page (rotating subject covers over an interactive grid), login page,  onboarding (saved between refreshes), dashboard, My Subjects, game library with search and filters, Quick Quiz, Flashcard Review (Again/Hard/Good/Easy with next-review dates), Challenge Mode (20 s per question), results, mistake review and retry, study history, progress charts, 7 achievements, dark/light theme, reduced motion, reset.

## Rules
- Level n starts at 100 x n x (n-1) XP.
- XP per game is capped (quiz 100, challenge 150, flashcards 50), scaled by accuracy, and only awarded when you beat your previous best for that game, so replays cannot farm XP.
- Streaks count distinct local calendar days with a completed session.
- Recommendations are rule-based: selected subjects, weak topics (under 70% over 3+ answers), due flashcards, session length, newness, recent repeats.

## Editing the content
Questions and flashcards live in the `RAW` and `FCR` objects near the top of the script in `index.html`. They are sample material; replace them with your syllabus.

## Known limitations
No real accounts or cloud database (one browser only), no coding questions, no automated tests beyond the smoke test, not tested on physical devices.

## Next: production build
Run the master build prompt in Claude Code with Node 20+, then: `npx create-next-app@latest studybuddy --typescript --tailwind --app`, `npx shadcn@latest init`, `npm i lucide-react recharts zod @supabase/supabase-js @supabase/ssr`, `npm i -D vitest @playwright/test`. Use `index.html` as the logic and design reference.
