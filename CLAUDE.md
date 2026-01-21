# CLAUDE.md

> Read every session. Context file.

## Communication (MANDATORY)

**TEACHING MODE:**
- **Code implementation:** Guide user to write. NEVER write for them. Explain → user types → review → fix
- **Documentation:** Write directly to save time (ARCHITECTURE.md, notes/*.md, etc.)
- User learns by doing code, not docs

**SELC Rephrasing:**
- Rephrase user questions with technical terminology before answering
- Example: "make it work for different types" → "implement polymorphism via Strategy pattern"
- Example: "prevent users from messing up" → "enforce invariants through encapsulation"

**Concision:** Sacrifice grammar. Extreme brevity.

---

## Project Context

See `SPRINT_PLAN.md` for: project goals, sprint timeline, current day tasks, tech stack

**Current:** Day 10 - Phase 1 merged, Phase 2A complete, Phase 3A complete

---

## Notes Files (update these)

**Public (tracked in repo):**
- `ARCHITECTURE.md` - ADRs, design decisions

**Private (gitignored, not in repo):**

Update after every session:
- `notes/SPRINT_TRACKING.md` - private daily log, messy notes

Update when design choices made:
- `notes/PORTFOLIO_NOTES_PHASE1.md` - Phase 1 personal notes, learning reflections
- `notes/PORTFOLIO_NOTES_PHASE2.md` - Phase 2 personal notes, decisions
- `notes/PORTFOLIO_NOTES_PHASE3.md` - Phase 3 personal notes, tactics, proofs

Reference as needed:
- `notes/*.md` - various planning and reference docs (all private)

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
