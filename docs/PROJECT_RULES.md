Arlo Project Development Rules

This project is developed as production-quality software.

General Rules

- Always generate COMPLETE files unless I explicitly request a snippet.
- Never ask me to manually edit code.
- If multiple files must change together, provide all complete files in the correct order.
- Follow Home Assistant best practices.
- Keep explanations concise and focus on implementation.

Project Rules

- Git is the source of truth.
- Documentation is part of the project.
- Architecture changes are only allowed during framework versions.
- After v0.10 the architecture is frozen unless fixing a bug.
- Every feature must fit the existing architecture.

Important

Whenever you identify:
- a better design,
- technical debt,
- a future enhancement,
- a performance improvement,
- a security improvement,
- or anything that would benefit Arlo later,

DO NOT interrupt the current development unless it is critical.

Instead:

1. Tell me briefly about the improvement.
2. Remind me to add it to docs/FUTURE_IMPROVEMENTS.md.
3. If it changes how Arlo should be designed permanently, also remind me to record it in docs/DECISIONS.md.
4. Continue with the current task.

Never allow important ideas to be forgotten.