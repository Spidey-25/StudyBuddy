# Coding activities and execution boundary

StudyBuddy offers two related but separate sets of practice:

- Local study modes: code-line sequencing, typed missing-line practice, typing sprint, memory matching, quizzes, and flashcards. These preserve the original dashboard/XP workflows.
- Platform activities: deterministic games including C/C++/Java/Python code repair, output tracing, SQL construction, algorithm and structure tracing, plus several non-code technical simulations.

Platform coding tasks expose prepared sample expectations and hints. The server compares answers against a fixed answer key; it never executes learner-supplied code. There is currently no hidden test runner, compiler, runtime limit enforcement, or general-purpose partial execution score. This is an explicit limitation, not an enabled capability.

A future executable mode requires a separately deployed isolated runner, strict CPU/memory/process/time limits, no network, a read-only filesystem, language allowlists and a narrow queue/API boundary. Never add arbitrary `subprocess` execution to Flask.
