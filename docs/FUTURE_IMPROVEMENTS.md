# Arlo Future Improvements

This file contains ideas and reminders discovered during development.
Items are added whenever we identify something that should be improved later.

---

## Architecture

- [ ] Replace temporary queue timing with event-driven transmission if MeshCore provides a reliable completion event.
- [ ] Remove any remaining global state.
- [ ] Review all modules for Home Assistant best practices.
- [ ] Add automatic unit tests.

---

## Performance

- [ ] Profile message queue under heavy load.
- [ ] Measure memory usage with 500+ registered users.
- [ ] Cache leaderboard calculations.

---

## Reliability

- [ ] Retry failed transmissions with exponential backoff.
- [ ] Detect duplicate incoming messages.
- [ ] Detect lost acknowledgements.
- [ ] Recover queue after Home Assistant restart.

---

## Storage

- [ ] Add automatic database migration.
- [ ] Add backup and restore.
- [ ] Export statistics to CSV.

---

## MeshCore Monday

- [ ] One check-in per Monday.
- [ ] Weekly winner.
- [ ] Monthly winner.
- [ ] Bonus points.
- [ ] Streak recovery.
- [ ] Holiday events.

---

## AI

- [ ] Natural language commands.
- [ ] Conversation memory.
- [ ] Context-aware replies.
- [ ] Personality profiles.

---

## Documentation

- [ ] Generate developer documentation.
- [ ] Generate user manual.
- [ ] Installation guide.
- [ ] API documentation.

---

## Release Checklist

Before every release:

- [ ] Update CHANGELOG.md
- [ ] Update ROADMAP.md
- [ ] Review TODO.md
- [ ] Commit all changes
- [ ] Tag release in Git

One improvement I'd like to adopt

Before we write more code, I'd like to standardize versioning:

manifest.json should always match the Git tag (for example, 0.10.0 rather than 1.0.0-alpha.2).
const.py should expose the same version string.
Every release should have a matching Git tag.