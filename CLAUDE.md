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

**Current:** Day 15 (1/26) - **PROJECT PAUSED FOR LEAN STUDY**

**Status:** POC bridge **100% COMPLETE** ✅
- Phase 3B.1 paused at ~70% (parametric proof has 2 `sorry` cases remaining)
- POC Python-Lean bridge: **COMPLETE**
  - Lean executable: ✓ (Rat-based JSON I/O, structured errors)
  - Python components: ✓ (serializer, client, exceptions)
  - Integration tests: ✓ (18 tests, 100% coverage on core components)
  - Error handling: ✓ (8 error tests, all exception types validated)
  - Coverage: 96% overall, 100% client/exceptions/serializer
- **Decision:** Pause project to study Lean 4 directly (tactics, proof fundamentals)
- **Return trigger:** Comfortable with techniques needed for Phase 3B.1 completion

**Active Plan:** ⏸️ **PAUSED** - User studying Lean directly
- POC complete: `/Users/rachealcooper/.claude/plans/mossy-greeting-gem.md` (achieved 100%)
- Parametric integration: `/Users/rachealcooper/.claude/plans/nested-honking-ladybug.md` (resume when ready)

**When Resuming:**
1. Finish Phase 3B.1 parametric proof (~2-3 hrs) - resolve 2 `sorry` cases
2. Update POC to use parametric proof (~2-3 hrs) - remove hardcoded validation
3. Continue vertical integration: Lorenz → Pendulum proofs + serialization

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

## Session Start

**⏸️ PROJECT CURRENTLY PAUSED - User studying Lean 4 directly**

**Status check:**
- POC bridge: 100% complete (18 tests, 96% coverage, documented)
- Phase 3B.1: 70% complete (2 `sorry` cases remaining)
- User learning: Lean tactics, proof fundamentals, Mathlib patterns

**When resuming (user will notify):**
1. Check user's Lean study progress
2. Read parametric plan: `/Users/rachealcooper/.claude/plans/nested-honking-ladybug.md`
3. Resume Phase 3B.1 parametric proof (~2-3 hrs remaining)
4. Then update POC to use parametric proof (~2-3 hrs)

**If user returns with questions:**
- Lean syntax/tactics: Explain + point to resources
- POC architecture: Reference PORTFOLIO_NOTES_PHASE2/3.md
- Proof strategies: Discuss approach, user implements

---

## Session End

```bash
git push && git branch -vv
```

**Checklist:**
- Update notes/SPRINT_TRACKING.md with session summary
- Update notes/PORTFOLIO_NOTES_PHASE*.md with learnings (design decisions, challenges overcome)
- List unresolved questions (extreme concision)
