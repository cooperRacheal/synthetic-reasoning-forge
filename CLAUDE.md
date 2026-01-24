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

**Current:** Day 11-12 (1/22-1/23) - Phase 1 merged, Phase 1.5 complete, Phase 2A complete, Phase 3A complete

**Status:** POC bridge implementation ~85% complete
- Phase 3B.1 paused at ~70% (parametric proof has 2 `sorry` cases remaining)
- Building POC Python-Lean bridge using completed Phase 3A proof
- Strategy: Learn subprocess/JSON/Lean I/O before finishing parametric proofs
- **POC Progress:** Lean executable built ✓, Python components complete ✓, integration tests written (pending validation)
- **Blocker:** Circular import in serializer.py (fix identified: `from __future__ import annotations`)
- Remaining: Fix import, validate tests, add error handling tests (~1-2 hrs)

**Active Plan (CURRENT PRIORITY):** `/Users/rachealcooper/.claude/plans/mossy-greeting-gem.md`
- **Enhanced POC Python-Lean Bridge** - Use Phase 3A specific-case proof (100% complete)
- Hardcoded values: x0=5, t∈[-0.1, 0.1], lambda=1
- **Production architecture:** Rat-based JSON (exact rationals), custom exception hierarchy, comprehensive error handling, timeout support
- Deliverable: Production-ready integration test demonstrating Python → JSON → Lean → Result
- **Work on this plan EXCLUSIVELY until POC complete**
- Implementation: Rat-based ({"num": X, "den": Y}) instead of Float for exact precision
- Read full plan file for implementation details
- **Supersedes:** `wild-percolating-candle.md` (basic POC, not implemented)

**Background Plan (resume after POC):** `/Users/rachealcooper/.claude/plans/nested-honking-ladybug.md`
- Vertical integration: 3 concrete systems (Decay → Lorenz → Pendulum) before abstraction
- Original estimate: 36-46 hrs total
- Sequence: Phase 1.5 ✅ → 2A ext → 3B.1 → 2B → 3B.2 → 2C → 3B.3 → Testing
- On hold until POC validates bridge architecture

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
1. **PRIORITY:** Check POC plan: Read `/Users/rachealcooper/.claude/plans/mossy-greeting-gem.md`
2. Review todo list (shows POC progress)
3. Continue POC implementation until complete (7.5-8 hrs estimated)
4. Background context: `/Users/rachealcooper/.claude/plans/nested-honking-ladybug.md` (resume after POC)

**During POC implementation:**
- Follow POC plan sequence (Lean → Python → Tests)
- Mark todos in_progress → completed as you work
- POC is learning-focused: understand integration mechanics
- When POC complete, user decides: continue to parametric proofs OR other work

**After POC complete:**
- Document learnings in PORTFOLIO_NOTES_PHASE2.md (bridge architecture, JSON design, subprocess patterns)
- Document learnings in PORTFOLIO_NOTES_PHASE3.md (Lean I/O, error handling, type correctness)
- Resume nested-honking-ladybug.md plan OR user redirects

---

## Session End

```bash
git push && git branch -vv
```

**Checklist:**
- Update notes/SPRINT_TRACKING.md with session summary
- Update notes/PORTFOLIO_NOTES_PHASE*.md with learnings (design decisions, challenges overcome)
- List unresolved questions (extreme concision)
