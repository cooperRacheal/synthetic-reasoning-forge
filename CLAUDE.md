# CLAUDE.md — Project Governance

> **Purpose:** Single source of truth for AI-assisted development. Read this file at the start of every session.

---

## Project State

**Name:** Synthetic Reasoning Forge (SRF)
**Goal:** Automate discovery and formalization of mathematical analogies between Control Theory and Systems Biology using Lean 4 formal verification.
**Stage:** Pre-Alpha (infrastructure complete, core logic not yet implemented)
**Target:** Senior-level portfolio project for systems/software engineering roles

---

## Directory Structure

```
reasoning_forge/
├── .venv/              # Python 3.12 virtual environment (git-ignored)
├── pyproject.toml      # Package manifest & tool configuration
├── README.md           # External documentation (portfolio pitch)
├── CLAUDE.md           # This file (AI governance)
├── LICENSE             # MIT License
├── data/               # Raw math problems & datasets
├── scripts/            # Automation utilities
├── src/logic/          # Python bridge, heuristics, ODE solver
├── tests/              # Pytest suite
└── lean/               # Lean 4 formal verification
    ├── ForgeLogic.lean
    ├── lakefile.toml
    ├── lean-toolchain  # Pinned to v4.26.0
    └── README_LOCAL.md # Local notes (git-ignored)
```

---

## Tech Stack

| Layer | Technology | Notes |
|-------|------------|-------|
| Formal Kernel | Lean 4 (v4.26.0) | Pinned via `lean-toolchain` |
| Orchestration | Python 3.11+ | Isolated in `.venv/` (currently 3.12) |
| Build System | hatchling | Configured in `pyproject.toml` |
| Integration | LeanDojo / lean-client-python | **Not yet installed** |
| AI Agent | Claude Code CLI | You are here |
| Formatting | black | 88-char lines, configured in `pyproject.toml` |
| Linting | ruff | Rules: E, F, I, UP, B, SIM |
| Type Checking | mypy | Strict mode enabled |
| Testing | pytest | Configured in `pyproject.toml` |

---

## Commands

```bash
# Environment
source .venv/bin/activate       # Activate Python venv
pip install -e ".[dev]"         # Install package + dev dependencies

# Python Quality
black .                         # Format code
ruff check .                    # Lint code
mypy src/                       # Type check
pytest                          # Run tests

# Lean
cd lean && lake build           # Build Lean project
```

---

## Initialization Checklist

- [x] Directory skeleton created
- [x] Python venv (`.venv/`) with Python 3.12
- [x] `pyproject.toml` manifest with tool configs
- [x] `LICENSE` file (MIT)
- [x] `README.md` with badges, structure, prerequisites
- [x] Lean 4 toolchain initialized (`lake init`)
- [x] `lean-toolchain` pinned to v4.26.0
- [x] `CLAUDE.md` governance document
- [ ] `src/logic/__init__.py` created
- [ ] `tests/__init__.py` created
- [ ] Dev dependencies installed (`pip install -e ".[dev]"`)
- [ ] CI/CD baseline (`.github/workflows/`)
- [ ] Pre-commit hooks configured

---

## Feature Roadmap

### Phase 1: Foundation (Current)
- [ ] Initialize `src/logic/` package structure
- [ ] Create `typing.Protocol` for ODE System interface
- [ ] Implement generic ODE solver
- [ ] Unit tests for solver with known systems (Lorenz, Pendulum)

### Phase 2: Bridge
- [ ] Define JSON schema for Python ↔ Lean goal state passing
- [ ] Create Lean subprocess runner with timeout/memory limits
- [ ] Exception mapping for Lean errors (tactic timeouts, kernel panics)

### Phase 3: Intelligence
- [ ] Cross-domain analogy mining logic
- [ ] Mathlib namespace traversal
- [ ] Automated verification loop

---

## Engineering Standards

### Code Style
1. **Packaging:** Use `pyproject.toml` and `src/` layout. No `setup.py`.
2. **Formatting:** `black` for code, 88-char line length.
3. **Linting:** `ruff` with rules: E, F, I, UP, B, SIM.
4. **Type Hints:** All functions must have type annotations. `mypy --strict`.

### Quality
5. **Testing:** `pytest` in `tests/`. Unit tests for core logic.
6. **Documentation:** Docstrings for public functions. No over-documentation.
7. **Lean:** No `sorry` in committed code. All proofs must verify.

### Process
8. **Commits:** Conventional commits (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`).
9. **Co-authorship:** Include `Co-Authored-By: Claude <noreply@anthropic.com>` when AI-assisted.

---

## Logging

Use Python's `logging` module with a centralized configuration.

```python
# src/logic/logger.py
import logging

def get_logger(name: str) -> logging.Logger:
    """Get a configured logger for the given module name."""
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

Use environment variables for secrets and configurable paths.

```python
import os

LEAN_TIMEOUT = int(os.getenv("LEAN_TIMEOUT", "30"))  # seconds
DATA_DIR = os.getenv("DATA_DIR", "data/")
```

**Rules:**
- Never commit `.env` files
- Create `.env.example` as a template when configuration is needed
- Document all environment variables in this file

**Current environment variables:** None yet. Create `.env.example` when first config is needed.

---

## Error Handling

### Custom Exceptions

Define in `src/logic/exceptions.py`:

```python
class ForgeError(Exception):
    """Base exception for all Forge errors."""

class LeanTimeoutError(ForgeError):
    """Lean subprocess exceeded time limit."""

class LeanVerificationError(ForgeError):
    """Lean proof failed to verify."""

class SolverConvergenceError(ForgeError):
    """ODE solver failed to converge."""
```

### Philosophy
1. **Fail fast, fail loud:** Raise exceptions rather than returning `None` silently.
2. **Log before raising:** Always log error context before raising.
3. **Typed exceptions:** Use specific exception types, not generic `Exception`.

---

## Interfaces (Protocols)

Use `typing.Protocol` for dependency inversion and testability.

```python
from typing import Protocol
import numpy as np
from numpy.typing import NDArray

class ODESystem(Protocol):
    """Any object with a .f(t, y) method can be solved."""

    def f(self, t: float, y: NDArray[np.float64]) -> NDArray[np.float64]:
        """Compute the derivative dy/dt at time t and state y."""
        ...
```

This allows the solver to accept *any* system without tight coupling.

---

## Testing Strategy

| Type | Location | What to Test |
|------|----------|--------------|
| Unit | `tests/unit/` | Pure Python logic, ODE solver, parsers |
| Integration | `tests/integration/` | Python ↔ Lean subprocess communication |
| Smoke | `tests/smoke/` | End-to-end "does it run?" checks |

**Coverage goal:** 80%+ for `src/logic/`

**Mocking strategy:**
- Mock Lean subprocess calls in unit tests
- Use real Lean in integration tests

**Test naming:** `test_<function>_<scenario>.py`

---

## Git Workflow

**Branch strategy:** GitHub Flow (simple)

1. `main` is always deployable
2. Create feature branches: `git checkout -b feat/ode-solver`
3. Open PR when ready for review
4. Merge to main after review

**Commit style:** Conventional Commits
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `chore:` maintenance
- `refactor:` code restructure
- `test:` adding tests

**Protected branch:** None currently (solo project). Add protection when collaborating.

---

## Dependency Management

- **Bounds:** Defined in `pyproject.toml` (`>=X,<Y` for stability)
- **Lockfile:** Generate with `pip freeze > requirements-lock.txt` after installing
- **CI:** Install from lockfile for reproducibility

**Future consideration:** Migrate to `uv` or `poetry` for better dependency resolution.

---

## Unresolved Questions

> For AI context only. Migrate active work items to GitHub Issues.

### Technical
1. **CI/CD Complexity:** Lean 4 + mathlib is heavy; GitHub Actions may timeout or exhaust disk space.
2. **Solver Performance:** Pure Python ODE solver vs numba-optimized. Decision: Start pure Python, optimize if profiling shows need.
3. **Bridge Interface:** No strategy yet for handling Lean kernel panics or tactic timeouts in Python subprocess.
4. **Dependency Volatility:** `lean-client-python` and `mathlib4` update frequently. Pin specific versions when installing.

### Process
5. **Pre-commit Hooks:** Not yet configured. Evaluate `pre-commit` library when CI/CD is set up.
6. **Environment Parity:** Lean versions must match between local and CI (`lean-toolchain` helps).
7. **Pydantic Version:** Use Pydantic v2 if/when data validation is needed.

### Scope
8. **CLAUDE.md vs claude.local.md:** Consider splitting personal/local notes to a git-ignored file if this grows too large.
9. **Data Strategy:** Track raw data in `data/` now; add to `.gitignore` if Git performance degrades.

---

## README.md Status

The README is correctly scoped for external audiences (recruiters, users, contributors).

**Currently complete sections:**
- Project title and badges
- Overview and System Architecture
- Technical Stack (table format)
- Project Structure
- Current Status checklist
- Prerequisites
- Setup & Installation
- License
- Contributing

**Future additions (not needed yet):**
- [ ] "Development" section linking to CLAUDE.md for internal guidelines
- [ ] CONTRIBUTING.md file when accepting external contributions
- [ ] Badges for CI status once GitHub Actions is configured

---

## Session Continuity

When starting a new Claude Code session:

1. Activate environment:
   ```bash
   cd /Users/rachealcooper/Documents/TBM_PhD/Personal_Projects/reasoning_forge
   source .venv/bin/activate
   ```

2. Tell Claude:
   ```
   Read CLAUDE.md
   ```

3. Optionally check state:
   ```
   Check git status and continue from the initialization checklist
   ```

**This file is the project's memory. Update it as decisions are made.**
