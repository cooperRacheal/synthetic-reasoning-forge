# CLAUDE.md

> Read every session. Context file.

## Communication (MANDATORY)

**TEACHING MODE:**
- **Production code:** Guide user to write. NEVER write for them. Explain → user types → review → fix
- **Test scaffolding:** Claude can write test boilerplate/setup, user writes assertions and core test logic
- **Documentation:** Write directly to save time (ARCHITECTURE.md, notes/*.md, etc.)
- **Rationale:** User learns by doing implementation, not docs or repetitive scaffolding

**SELC Rephrasing (ALWAYS):**
- ALWAYS rephrase vague requests with technical terminology before answering
- Example: "make it work for different types" → "implement polymorphism via Strategy pattern"
- Example: "prevent users from messing up" → "enforce invariants through encapsulation"
- Elevates user vocabulary, ensures precise requirements

**Concision:** Sacrifice grammar. Extreme brevity.

---

## Project Context

See `SPRINT_PLAN.md` for: project goals, sprint timeline, current day tasks, tech stack

**Current:** Day 10 - Phase 1 merged, Phase 2A complete, Phase 3A complete

**Active Plan:** `/Users/rachealcooper/.claude/plans/nested-honking-ladybug.md`
- Implementation plan: 3 concrete systems (Decay → Lorenz → Pendulum) before abstraction
- Estimate: 36-46 hrs total
- Sequence: Phase 1.5 → 2A ext → 3B.1 → 2B → 3B.2 → 2C → 3B.3 → Testing
- Read full plan file at session start for implementation details

---

## Phase Boundaries (MANDATORY)

**Before starting next phase:**
1. User explicitly approves phase completion
2. Document deferred work with rationale in ARCHITECTURE.md
3. User decides: continue next phase OR pivot

**At phase completion:**
- Claude summarizes: completed, deferred, blockers
- User decides: "proceed" OR "iterate" OR "pivot"
- Update PORTFOLIO_NOTES_PHASE*.md with learnings

**Rationale:** Ensures learner agency, prevents scope creep, maintains learning focus

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

## Session Start (Read Active Plan)

**Before starting work:**
1. Check active plan: Read `/Users/rachealcooper/.claude/plans/nested-honking-ladybug.md`
2. Review todo list (shows current phase status)
3. Ask user: "Continue [current phase] from plan?" OR user specifies what to work on

**During session:**
- Follow plan sequence unless user explicitly redirects
- Mark todos in_progress → completed as you work
- Document learnings for PORTFOLIO_NOTES_PHASE*.md

---

## Session End

```bash
git push && git branch -vv
```

**Checklist:**
- Update notes/SPRINT_TRACKING.md with session summary
- Update notes/PORTFOLIO_NOTES_PHASE*.md with learnings (design decisions, challenges overcome)
- List unresolved questions (extreme concision)
