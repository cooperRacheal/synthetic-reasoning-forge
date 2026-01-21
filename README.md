# Synthetic Reasoning Forge (SRF)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Lean 4](https://img.shields.io/badge/Lean-4.26.0-orange.svg)](https://lean-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Bridging Mathematical Intuition with Formal Verification**

## Overview

The **Synthetic Reasoning Forge** is an experimental pipeline designed to automate the discovery and formalization of mathematical analogies. By leveraging LLM-driven "analogy mining" and the **Lean 4** theorem prover, the system identifies structural isomorphisms between disparate domains—specifically **Control Theory** and **Systems Biology**.

The core objective is to transform fuzzy mathematical intuition into machine-verifiable proofs, ensuring that cross-domain analogies are not just metaphorical, but formally sound.

**📍 Project Status:** See [STATUS.md](STATUS.md) for current completion state, explanation of dual phase naming (original 3-phase plan vs. execution sub-phases), and next steps decision point.

## System Architecture

The Forge operates in three phases (with execution sub-phases detailed in STATUS.md):

### Phase 1: Numerical Foundation (✅ COMPLETE)
Python ODE solver with extensible visualization architecture for dynamical systems analysis.

**Components:**
- Generic ODE solver (scipy integration with method selection + auto-fallback)
- Strategy + Factory pattern visualization (2D/3D phase portraits)
- Test systems: Lorenz attractor, damped pendulum, pathological cases
- Comprehensive testing: 44 unit tests, 95% code coverage

### Phase 2: Python-Lean Bridge (⚠️ PARTIAL - Phase 2A Complete)
Symbolic equation extraction and JSON serialization for formal verification pipeline.

**Phase 2A (Complete):** SymbolicMixin foundation with lazy symbolic equation generation
**Phase 2B/2C (Deferred):** JSON serialization and LeanProofRequest API

**Components:**
- ✅ Symbolic ODE representation (sympy integration) - Phase 2A
- 📋 JSON schema for system metadata (parameters, equations, state variables) - Phase 2B planned
- 📋 Conjecture packaging API (LeanProofRequest for structural isomorphisms) - Phase 2C planned
- 📋 Subprocess communication layer - Future work

### Phase 3: Lean Formal Verification (⚠️ STARTED - Phase 3A Complete)
Manual proof development in Lean 4 for ODE system properties and structural isomorphisms.

**Phase 3A (Complete):** Lean learning + first Picard-Lindelöf proof (decay_picard_specific)
**Phase 3B/3C (Not Started):** Parametric proofs, system formalization, isomorphism theorems

**Current Status:** First complete proof validates feasibility of formal ODE verification
**Long-term Goal:** Formally prove that biological regulation (glucose-insulin homeostasis) is mathematically equivalent to classical control systems (PID controllers).

## Technical Stack

| Component | Technology | Status |
|-----------|------------|--------|
| **Formal Kernel** | Lean 4 (v4.26.0) | ⏳ Phase 3A active |
| **Orchestration** | Python 3.11+ | ✅ Active |
| **Numerical Computing** | NumPy ≥1.24, SciPy ≥1.11 | ✅ Phase 1 |
| **Symbolic Math** | SymPy ≥1.12 | ✅ Phase 2A |
| **Visualization** | Matplotlib ≥3.8 | ✅ Phase 1 |
| **Testing** | pytest ≥8.0, pytest-cov | ✅ 95% coverage (44 tests) |
| **Quality Tools** | Black, Ruff, Mypy | ✅ Black + Ruff passing |
| **Integration Layer** | LeanDojo / lean-client-python | 📋 Planned (Phase 3C) |
| **Build System** | pyproject.toml / hatchling | ✅ Active |
| **Version Control** | Git / GitHub | ✅ Active |

## Project Structure

```
reasoning_forge/
├── pyproject.toml           # Package manifest & dependencies
├── README.md                # This file
├── ARCHITECTURE.md          # Architecture decision records (ADRs)
├── CLAUDE.md                # AI governance & project memory
├── SPRINT_PLAN.md           # Development timeline
├── Makefile                 # Quality checks & test automation
├── examples/                # Validation scripts & visual outputs
│   ├── validate_plotting.py    # 7 plots proving architecture
│   └── output/                 # Generated phase portraits
├── src/logic/               # Python ODE solver + visualization
│   ├── solver.py               # Generic ODE integration (scipy wrapper)
│   ├── exceptions.py           # Custom exception hierarchy
│   ├── logger.py               # Centralized logging
│   ├── protocols.py            # ODESystem protocol (interface)
│   ├── systems/                # Concrete ODE system implementations
│   │   ├── lorenz.py              # Lorenz attractor (chaotic dynamics)
│   │   ├── pendulum.py            # Damped pendulum (dissipative system)
│   │   └── blow_up_system.py     # Pathological system (tests error handling)
│   ├── plotting/               # Strategy + Factory visualization
│   │   ├── base.py                # PhasePortraitPlotter ABC
│   │   ├── config.py              # PlotConfig dataclass
│   │   ├── plotters.py            # 2D/3D concrete implementations
│   │   ├── factory.py             # PlotterFactory registry
│   │   └── __init__.py            # Public API (plot_phase_portrait)
│   └── lean_bridge/            # Phase 2: Python-Lean bridge (Phase 2A complete)
│       ├── symbolic.py            # SymbolicMixin (sympy integration) ✅
│       ├── serialization.py       # ODESystemMetadata (JSON schema) - planned
│       └── proof_request.py       # LeanProofRequest API - planned
├── tests/                   # Comprehensive test suite
│   ├── conftest.py             # Pytest fixtures (systems, ICs, config)
│   └── unit/                   # 44 unit tests, 95% coverage
│       ├── test_solver.py         # Convergence, methods, auto-fallback (8 tests)
│       ├── test_systems.py        # System implementations (6 tests)
│       ├── test_plotting_factory.py # PlotterFactory registry (4 tests)
│       ├── test_plotting_plotters.py # 2D/3D plotter integration (4 tests)
│       ├── test_plotting_api.py   # Public API dispatch (3 tests)
│       ├── test_plotting_config.py # PlotConfig dataclass (2 tests)
│       ├── test_exceptions.py     # Exception hierarchy (3 tests)
│       ├── test_logger.py         # Logger configuration (3 tests)
│       └── test_lean_bridge_symbolic.py # SymbolicMixin (10 tests)
└── lean/                    # Lean 4 formal verification (2 separate Lake projects)
    ├── ForgeLogic/          # Production project (future Python-Lean bridge target)
    │   └── Basic.lean       # Core definitions (placeholder)
    └── lean_learning/       # Learning project (separate Lake config)
        └── LeanBasics/      # Learning exercises + first proofs
            ├── Arithmetic.lean        # Session 1A: First proofs
            ├── ODETypes.lean          # Session 1B: Structures
            ├── Tactics.lean           # Session 2A: Core tactics
            ├── AnalysisTactics.lean   # Session 2B: Analysis tactics
            └── PicardExample.lean     # Phase 3A: decay_picard_specific ✅
```

## Documentation Structure

### Public Files (Tracked in Repository)

**Core Documentation:**
- `README.md` - Project overview, setup instructions, usage examples
- `STATUS.md` - **Current project status, dual phase naming explanation, next steps**
- `ARCHITECTURE.md` - Architecture Decision Records (ADRs #1-16)
- `SPRINT_PLAN.md` - Development timeline, milestones, progress tracking
- `CLAUDE.md` - AI collaboration guidelines, communication protocols

**Code & Proofs:**
- `src/logic/` - Python ODE solver + visualization infrastructure
- `tests/` - 44 unit tests (95% coverage)
- `examples/` - Validation scripts and generated plots
- `lean/lean_learning/LeanBasics/PicardExample.lean` - First Picard-Lindelöf proof
- `lean/lean_learning/lakefile.toml`, `lean-toolchain` - Lean build config

**Supporting Documentation:**
- `docs/REFERENCES.md` - Scientific literature citations (biomechanics, control theory)

### Private Files (Gitignored, Not in Repository)

**Daily Logs:**
- `notes/SPRINT_TRACKING.md` - Daily work log, messy notes, time tracking

**Personal Learning Notes:**
- `notes/PORTFOLIO_NOTES_PHASE1.md` - Phase 1 reflections and decisions
- `notes/PORTFOLIO_NOTES_PHASE2.md` - Phase 2 SymbolicMixin notes
- `notes/PORTFOLIO_NOTES_PHASE3.md` - Phase 3 Lean proof walkthrough notes

**Planning & Exploration:**
- `notes/*.md` - Various planning documents, catch-up checklists, architecture explorations

**Rationale:** Private notes contain messy work-in-progress thoughts, personal reflections, and detailed daily logs. Public documentation captures polished decisions, architecture, and completed work suitable for collaboration and portfolio presentation.

**Understanding Phase Naming:**
- `STATUS.md` explains dual naming: original 3-phase architecture (design) vs. execution sub-phases (2A/2B/2C, 3A/3B/3C)
- `PHASE2_3_LEAN_BRIDGE.md` (private) describes the original 3-phase architectural vision
- `SPRINT_PLAN.md` shows day-by-day actual execution timeline
- When documentation mentions "Phase 2A" or "Phase 3A", these are execution milestones within the original phases

---

## Current Status (Day 10 - January 21, 2026)

**Timeline:** Started Monday Jan 12 (Day 1), currently Day 10 (Wed Jan 21) - *calendar days, includes weekends*
**Sprint Status:** Extended beyond original 7-day plan

**📍 Quick Reference:** See [STATUS.md](STATUS.md) for detailed breakdown of what's complete vs. deferred, and explanation of why the project pivoted from Phase 2 to Phase 3 on Day 7.

### Phase 1: Numerical Foundation ✅ COMPLETE (Days 1-6)
- [x] Environment isolation (Python 3.11+ venv)
- [x] Package manifest with dependencies (numpy, scipy, matplotlib, sympy)
- [x] Generic ODE solver (method selection + auto-fallback for stiff systems)
- [x] Strategy + Factory pattern visualization (2D/3D phase portraits)
- [x] Test systems: Lorenz, Damped Pendulum, BlowUp
- [x] Comprehensive testing: 44 unit tests, 95% code coverage
- [x] Quality checks: Black + Ruff passing (Mypy deferred with documentation)
- [x] Visual validation: 7 plots with biologically relevant parameters
- [x] **Merged to main:** PR #1 (Day 6 - January 17, 2026)

### Phase 2: Python-Lean Bridge 🔨 PARTIAL (Phase 2A Complete)
**Strategy:** 3 sub-phases with validation checkpoints (5-8 hours total)

**Phase 2A: SymbolicMixin Foundation ✅ COMPLETE (Day 6 - Jan 17)**
- [x] Architecture design complete (ADRs #10-14 documented)
- [x] Incremental implementation plan with 3 validation checkpoints
- [x] Add SymPy dependency (sympy>=1.12,<2.0)
- [x] Implement SymbolicMixin (symbolic.py) with lazy caching
- [x] Extend LorenzSystem with symbolic support
- [x] Write 10+ tests for symbolic functionality (10 tests added)
- [x] Verify backward compatibility (all 44 tests pass)
- [x] Branch: feat/phase2-lean-bridge (not yet merged)

**Phase 2B: JSON Serialization (Not Started)**
- [ ] ODESystemMetadata dataclass (serialization.py)
- [ ] Sympy → Lean string conversion helpers
- [ ] Extend DampedPendulum with symbolic support
- [ ] Write serialization tests

**Phase 2C: Proof Request API (Not Started)**
- [ ] LeanProofRequest dataclass (proof_request.py)
- [ ] Factory functions for conjectures
- [ ] Integration tests
- [ ] Full workflow validation

**Original Target:** Complete Phase 2 by Day 12 (Jan 24, 2026) - Timeline adjusted, behind schedule

### Phase 3: Lean Formal Verification ⏳ IN PROGRESS
**Current Status:** Learning Lean 4, first proof complete

**Phase 3A: First Lean Proof ✅ COMPLETE (Days 7-9 - Jan 18-20)**
- [x] Lean 4 toolchain initialization (elan/lake)
- [x] Lean learning sessions 1A-2B (4 hours)
  - First proofs, types & structures, core tactics, analysis tactics
- [x] Complete first Picard-Lindelöf proof (decay_picard_specific)
  - System: dx/dt = -x on interval [-0.1, 0.1]
  - All 4 cases proven (Lipschitz, continuity, norm bound, consistency)
  - File: lean/lean_learning/LeanBasics/PicardExample.lean
- [x] Deep dive proof walkthrough and LaTeX documentation

**Phase 3B: Parametric Proofs (Not Started)**
- [ ] Generalize decay_picard for arbitrary intervals
- [ ] Prove Picard-Lindelöf for Lorenz system
- [ ] Prove for Damped Pendulum system

**Phase 3C: System Formalization (Not Started)**
- [ ] Formalize glucose-insulin minimal model
- [ ] Formalize PID controller system
- [ ] Prove structural isomorphism theorem
- [ ] Automated verification loop integration

## Usage

### Running the ODE Solver (Phase 1)

```python
from src.logic.solver import solve_ode
from src.logic.systems.lorenz import LorenzSystem
from src.logic.plotting import plot_phase_portrait, PlotConfig
import numpy as np

# Create system with default chaotic parameters
lorenz = LorenzSystem(sigma=10.0, rho=28.0, beta=8/3)

# Solve ODE system
initial_conditions = np.array([1.0, 0.0, 0.0])
solution = solve_ode(lorenz, t_span=(0, 50), y0=initial_conditions)

# Visualize phase portrait
config = PlotConfig(figsize=(12, 10), dpi=150)
fig = plot_phase_portrait(
    solution.t,
    solution.y,
    labels=['x', 'y', 'z'],
    title='Lorenz Attractor',
    config=config,
    save_path='lorenz_attractor.png'
)
```

### Running Tests

```bash
# Run all tests with coverage
make test-cov

# Run specific test module
pytest tests/unit/test_solver.py -v

# Run tests with coverage report
pytest tests/unit/ --cov=src/logic --cov-report=html
open htmlcov/index.html  # View detailed coverage

# Quality checks
make quality  # Runs Black + Ruff
```

### Visual Validation

```bash
# Generate all 7 validation plots
python examples/validate_plotting.py

# Outputs saved to examples/output/
# - lorenz_chaotic.png (3D butterfly attractor)
# - lorenz_chaotic_xy.png (2D x-y projection)
# - lorenz_stable.png, lorenz_convective.png (other regimes)
# - pendulum_damped.png (spiral to equilibrium)
```

## Prerequisites

### Phase 1 & 2 (Python Development)
- **Python 3.11+** — [Download](https://www.python.org/downloads/)
- **Git** — For version control

### Phase 3 (Lean Formal Verification - Currently Active)
- **elan** (Lean version manager) — [Install guide](https://github.com/leanprover/elan) ✅ Installed
- **Lean 4.26.0** — Managed via elan ✅ Active

## Setup & Installation

```bash
# Clone the repository
git clone https://github.com/cooperRacheal/synthetic-reasoning-forge.git
cd synthetic-reasoning-forge

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests to verify installation
make test

# (Optional) Generate visual validation plots
python examples/validate_plotting.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

This project is in early development. Contributions are welcome! Please open an issue to discuss changes before submitting a pull request.
