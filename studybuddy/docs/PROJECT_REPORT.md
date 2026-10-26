# StudyBuddy project report

## Abstract

StudyBuddy is a Flask and MySQL study application for college computing courses. It combines a preserved dashboard with quizzes, flashcards, timed challenges, progress history, XP and a separate server-validated games platform. The active platform contains 32 games across 16 subjects; each game has at least four authored levels and Python Logic Builder has twelve. This report describes the implementation and its limits; it does not claim measured learning gains.

## Problem and users

Students need short, interactive practice that helps them retrieve concepts, debug logic, trace algorithms and apply technical procedures. Teachers need a simple way to add content and inspect aggregate class activity. StudyBuddy is a local/minor-project prototype, not a hosted learning management system.

## Requirements and implementation

- Email-based registration and login; unique email; hashed passwords; no email verification.
- Student and teacher roles, computing branches/courses, branch-to-subject relationships, and editable student subject choices.
- Two platform activities for each of 16 enabled subjects, with unique authored content, progressive difficulty, hints, feedback, per-level scoring, retry and persisted sessions.
- DSA C++/Java choice saved with the student's platform session.
- Server-side validation, session ownership, terminal lifecycle states and idempotent action/result writes.
- Teacher-only subject/content endpoints and analytics for session volume, completion, weak topics, and question-quality aggregates.
- Existing frontend design and local study experience preserved.

## Design and data model

Flask serves the single-page frontend and JSON API. MySQL stores accounts, branches, subjects, user-subject mappings, teacher content, idempotent legacy session summaries, question attempts, platform-game state, lifecycle status, per-action responses and one-time XP rewards. The ER diagram and request flow are in `ARCHITECTURE.md`. Schema initialization is additive and startup creates the configured database and missing tables when the MySQL account has permission.

## Games and learning objectives

Each platform level has a task-specific objective, prompt, difficulty and hint. New runs randomize content within the difficulty progression and avoid opening with the prior run's final question. The catalog includes code repair and output tracing, OOP decisions, logic construction, algorithm ordering, stack/queue tracing, SQL construction, ER cardinality, scheduling, memory allocation, packet routing, troubleshooting, responsive UI, testing strategy, inference, metrics, incident response, cloud design, embedded interrupts and IoT topology. Answers are kept in server-side definitions. A correct level awards 100 points; completion writes accuracy, duration and XP once. Incorrect actions record a mistake and do not advance. Explanatory feedback is returned after a correct answer.

## Safety and limitations

Platform code-edit challenges use private deterministic fixtures and constrained checks for authored exercise patterns. They do not compile or execute learner-supplied source and do not provide a general compiler, runtime limits, or arbitrary hidden-test support. Teacher-created database game records are saved and reviewable but are not dynamically wired into the deterministic game engine. The legacy local-game session API accepts browser-reported summaries and is not authoritative in the same way as the platform game API. Educational simulations are small deterministic examples rather than full systems models.

## Testing and evaluation

Automated unit tests exercise all catalog levels, distinct routes, difficulty variety, answer redaction, navigation lifecycle contracts and mechanic renderers. Opt-in MySQL integration tests check every catalog start route, persistence, completion, exit/abandonment, action replay, exact-once rewards, ownership and authorization. A local browser demonstration was separately inspected; physical-device, screen-reader and broad browser matrix testing remain follow-up checks. Report the current run's test results separately rather than treating this report as a test log.

The evaluation protocol in `EVALUATION_STUDY.md` proposes a small pre-test/post-test and usability study. No participant data has been collected; therefore, no learning-improvement claim is made.

## Professional self-assessment

The implementation is a solid minor-project prototype with breadth, a clear API/data model and meaningful non-quiz interactions. It is not a production-grade assessment system: code is not executed, teacher-created content is not playable through the platform catalog, real browser/device and screen-reader coverage is incomplete, and educational effectiveness has not been measured. A rating above 9/10 would be unsupported until those gaps are addressed and evaluated.

## References

- University of St Andrews, *Software Engineering Project Guidance*: https://info.cs.st-andrews.ac.uk/student-handbook/projects/project-type-software-engineering.html
- Temple University, *IEEE Capstone Rubric*: https://athena.tu.temple.edu/~lbai/capstone/rubric
- StudyBuddy evaluation-study protocol: `EVALUATION_STUDY.md`
