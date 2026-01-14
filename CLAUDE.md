# CLAUDE.md — Project Governance

> **Purpose:** Single source of truth for AI-assisted development. Read at start of every session.

**Communication Style:** Be extremely concise. Sacrifice grammar for concision in all interactions and commit messages.

**Teaching Mode:** Guide user through writing code, don't write it for them. Rephrase user questions in proper technical terminology before answering.

---

## Project State

**Name:** Synthetic Reasoning Forge (SRF)
**Goal:** Prove mathematical equivalences between biological regulation and control systems using Lean 4
**Stage:** Pre-Alpha (Phase 1 in progress)
**Target:** Portfolio project for systems/software roles
**Sprint:** Jan 12-19 → Phase 1 ODE solver + glucose models

---

## Active Sprint

**Files:**
- `SPRINT_PLAN.md` - roadmap/milestones (committed)
- `SPRINT_TRACKING.md` - daily notes (gitignored)
- `LEAN_BRIDGE_ARCHITECTURE.md` - Phase 2-4 design (committed)

**Goal:** Phase 1 ODE solver + glucose-insulin models

**Daily Check-In:**
1. Ask for yesterday's progress
2. Review today's tasks from SPRINT_PLAN.md
3. Check blockers
4. Help update SPRINT_TRACKING.md
5. Keep on track for Sunday checkpoint

**Sunday Decision:** Path A (polish) vs Path B (Lean bridge)

---

## Directory Structure

```
reasoning_forge/
├── .venv/              # Python 3.12 venv (gitignored)
├── pyproject.toml      # Package manifest
├── README.md           # External docs
├── CLAUDE.md           # This file
├── SPRINT_PLAN.md      # Sprint roadmap (committed)
├── SPRINT_TRACKING.md  # Daily notes (gitignored)
├── LICENSE             # MIT
├── data/               # Datasets
├── scripts/            # Utilities
├── src/logic/          # Python ODE solver
├── tests/              # Pytest suite
└── lean/               # Lean 4 proofs
    ├── ForgeLogic.lean
    ├── lakefile.toml
    ├── lean-toolchain  # v4.26.0
    └── README_LOCAL.md # (gitignored)
```

---

## Tech Stack

| Layer | Tech | Notes |
|-------|------|-------|
| Formal | Lean 4 v4.26.0 | Via lean-toolchain |
| Runtime | Python 3.12 | In .venv/ |
| Build | hatchling | pyproject.toml |
| Integration | LeanDojo | Not yet installed |
| Format | black | 88-char lines |
| Lint | ruff | E,F,I,UP,B,SIM |
| Types | mypy | Strict mode |
| Test | pytest | - |

---

## Commands

```bash
# Environment
source .venv/bin/activate
pip install -e ".[dev]"

# Quality
black .
ruff check .
mypy src/
pytest

# Lean
cd lean && lake build
```

---

## Initialization Checklist

- [x] Directory skeleton
- [x] Python venv (3.12)
- [x] pyproject.toml
- [x] LICENSE (MIT)
- [x] README.md
- [x] Lean 4 toolchain (v4.26.0)
- [x] CLAUDE.md
- [x] src/logic/__init__.py
- [x] tests/__init__.py
- [x] Sprint plan files
- [ ] Dev dependencies installed
- [ ] CI/CD
- [ ] Pre-commit hooks

---

## Feature Roadmap

### Phase 1: Foundation (Current)
- [ ] ODESystem Protocol
- [ ] Generic ODE solver
- [ ] Lorenz/Pendulum test systems
- [ ] Glucose-insulin models
- [ ] Unit tests (80%+ coverage)

### Phase 2: Bridge
- [ ] JSON schema Python ↔ Lean
- [ ] Lean subprocess runner
- [ ] Exception mapping

### Phase 3: Intelligence
- [ ] Analogy mining
- [ ] Mathlib traversal
- [ ] Automated verification

---

## Engineering Standards

**Code:**
1. `pyproject.toml` + `src/` layout (no setup.py)
2. `black` format, 88-char lines
3. `ruff` lint (E,F,I,UP,B,SIM)
4. Type hints on all functions, `mypy --strict`

**Quality:**
5. `pytest` in tests/, unit tests for core
6. Docstrings for public functions only
7. No `sorry` in committed Lean code

**Process:**
8. Conventional commits (feat/fix/docs/chore/refactor/test)
9. Co-authorship: `Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>`

---

## Logging

```python
# src/logic/logger.py
import logging

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
```

**Usage:** `logger = get_logger(__name__)`

---

## Configuration

```python
import os

LEAN_TIMEOUT = int(os.getenv("LEAN_TIMEOUT", "30"))
DATA_DIR = os.getenv("DATA_DIR", "data/")
```

**Rules:**
- Never commit `.env`
- Create `.env.example` when needed
- Document all env vars here

**Current:** None. Create when needed.

---

## Error Handling

**Exceptions in `src/logic/exceptions.py`:**

```python
class ForgeError(Exception):
    """Base exception."""

class LeanTimeoutError(ForgeError):
    """Lean subprocess timeout."""

class LeanVerificationError(ForgeError):
    """Lean proof failed."""

class SolverConvergenceError(ForgeError):
    """ODE solver failed."""
```

**Philosophy:**
1. Fail fast, fail loud
2. Log before raising
3. Specific exception types

---

## Interfaces (Protocols)

```python
from typing import Protocol
import numpy as np
from numpy.typing import NDArray

class ODESystem(Protocol):
    """Any object with .f(t, y) method."""

    def f(self, t: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
        """Compute dy/dt."""
        ...
```

Allows solver to accept any system without coupling.

---

## Testing Strategy

| Type | Location | What |
|------|----------|------|
| Unit | tests/unit/ | Python logic, ODE solver |
| Integration | tests/integration/ | Python ↔ Lean |
| Smoke | tests/smoke/ | End-to-end |

**Coverage:** 80%+ for src/logic/

**Mocking:**
- Mock Lean in unit tests
- Real Lean in integration tests

**Naming:** `test_<function>_<scenario>.py`

---

## Git Workflow

**Strategy:** GitHub Flow

1. main = always deployable
2. Feature branches: `git checkout -b feat/name`
3. PR when ready
4. Merge after review

**Commits:** Conventional (feat/fix/docs/chore/refactor/test)

**Protected branch:** None (solo). Add when collaborating.

---

## Dependency Management

- **Bounds:** In pyproject.toml (>=X,<Y)
- **Lockfile:** `pip freeze > requirements-lock.txt`
- **CI:** Install from lockfile

**Future:** Consider uv or poetry

---

## Unresolved Questions

### Technical
1. CI/CD with Lean 4 + mathlib may timeout/exhaust disk
2. Solver performance: pure Python vs numba. Start pure, optimize if needed
3. Bridge interface for Lean panics/timeouts undefined
4. LeanDojo/mathlib4 volatile, pin versions

### Process
5. Pre-commit hooks: evaluate when setting up CI/CD
6. Lean version parity local/CI (lean-toolchain helps)
7. Use Pydantic v2 if/when needed

### Scope
8. Consider splitting CLAUDE.md if grows large
9. Track data in data/ now, gitignore if performance issues

---

## README.md Status

**Complete:**
- Title, badges
- Overview, architecture
- Tech stack
- Structure
- Status checklist
- Prerequisites
- Setup/install
- License, contributing

**Future:**
- [ ] Development section → CLAUDE.md
- [ ] CONTRIBUTING.md when external contributors
- [ ] CI badges when Actions configured

---

## Session Continuity

**Start new session:**

1. Activate:
   ```bash
   cd /Users/rachealcooper/Documents/TBM_PhD/Personal_Projects/reasoning_forge
   source .venv/bin/activate
   ```

2. Read: `CLAUDE.md`

3. Check sprint:
   - Review SPRINT_PLAN.md for current day
   - Ask about progress/blockers
   - Update SPRINT_TRACKING.md if needed

4. Check state: `git status` + initialization checklist

**This file = project memory. Update as decisions made.**

---

**At end of each session: List unresolved questions if any. Be extremely concise. Sacrifice grammar for concision.**
