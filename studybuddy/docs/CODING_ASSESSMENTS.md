# Coding activities and execution boundary

StudyBuddy offers two related but separate sets of practice:

- Local study modes: code-line sequencing, typed missing-line practice, typing sprint, memory matching, quizzes, and flashcards. These preserve the original dashboard/XP workflows.
- Platform activities: deterministic games including C/C++/Java/Python code repair, output tracing, SQL construction, algorithm and structure tracing, plus several non-code technical simulations.

Platform code-edit tasks expose prompts and hints. Their private exercise fixtures are not sent to the browser. A constrained server-side checker validates authored answer patterns against those fixed fixtures; it does not invoke a compiler or execute submitted source. This supports deterministic correctness checks for the included exercises, but it is not a general hidden-test runner and does not provide compiler/runtime limits or general-purpose partial execution scoring.

A future executable mode requires a separately deployed isolated runner, strict CPU/memory/process/time limits, no network, a read-only filesystem, language allowlists and a narrow queue/API boundary. Never add arbitrary `subprocess` execution to Flask.
