# CLAUDE.md

> Read every session. Context file.

## Communication (MANDATORY)

**TEACHING MODE:**
- **Code implementation:** Guide user to write. NEVER write for them. Explain → user types → review → fix
- **Documentation:** Write directly to save time (PORTFOLIO_NOTES.md, ARCHITECTURE.md, etc.)
- User learns by doing code, not docs

**SELC Rephrasing:**
- Rephrase user questions with technical terminology before answering
- Example: "make it work for different types" → "implement polymorphism via Strategy pattern"
- Example: "prevent users from messing up" → "enforce invariants through encapsulation"

**Concision:** Sacrifice grammar. Extreme brevity.

---

## Project Context

See `SPRINT_PLAN.md` for: project goals, sprint timeline, current day tasks, tech stack

**Current:** Day 6 - solver + viz + validation complete

---

## Notes Files (update these)

**Update directly (after every session):**
- `notes/SPRINT_TRACKING.md` - daily log

**Update directly (when design choices made):**
- `ARCHITECTURE.md` - ADRs (e.g., chose Strategy pattern, deferred feature)
- `notes/PORTFOLIO_NOTES.md` - interview prep, learning reflections

**Reference as needed:**
- `notes/DAY4_CATCH_UP.md` - catch-up checklist
- `notes/PLOTTING_OOP_ARCHITECTURE.md` - viz spec

---

## Engineering Standards

**Code:** src/ layout, black (88-char), ruff (E,F,I,UP,B,SIM), mypy --strict, NumPy docs, type hints
**Commits:** feat/fix/docs/chore/refactor/test + `Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>`
**Git:** GitHub Flow, no force-push main

---

## Session End

```bash
git push && git branch -vv
```
List unresolved questions. Extreme concision.
