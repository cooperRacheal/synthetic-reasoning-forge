# Synthetic Reasoning Forge (SRF)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Lean 4](https://img.shields.io/badge/Lean-4.26.0-orange.svg)](https://lean-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Bridging Mathematical Intuition with Formal Verification**

## Overview

The **Synthetic Reasoning Forge** is an experimental pipeline designed to automate the discovery and formalization of mathematical analogies. By leveraging LLM-driven "analogy mining" and the **Lean 4** theorem prover, the system identifies structural isomorphisms between disparate domains—specifically **Control Theory** and **Systems Biology**.

The core objective is to transform fuzzy mathematical intuition into machine-verifiable proofs, ensuring that cross-domain analogies are not just metaphorical, but formally sound.

## System Architecture

The Forge operates in three phases:

### Phase 1: Numerical Foundation (✅ COMPLETE)
Python ODE solver with extensible visualization architecture for dynamical systems analysis.

**Components:**
- Generic ODE solver (scipy integration with method selection + auto-fallback)
- Strategy + Factory pattern visualization (2D/3D phase portraits)
- Test systems: Lorenz attractor, damped pendulum, pathological cases
- Comprehensive testing: 33 unit tests, 95% code coverage

### Phase 2: Python-Lean Bridge (🔨 IN PROGRESS)
Symbolic equation extraction and JSON serialization for formal verification pipeline.

**Components:**
- Symbolic ODE representation (sympy integration)
- JSON schema for system metadata (parameters, equations, state variables)
- Conjecture packaging API (LeanProofRequest for structural isomorphisms)
- Subprocess communication layer (planned)

### Phase 3: Lean Formal Verification (📋 PLANNED)
Automated proof generation and verification for mathematical equivalences between biological and control systems.

**Goal:** Formally prove that biological regulation (glucose-insulin homeostasis) is mathematically equivalent to classical control systems (PID controllers).

## Technical Stack

| Component | Technology | Status |
|-----------|------------|--------|
| **Formal Kernel** | Lean 4 (v4.26.0) | Planned (Phase 3) |
| **Orchestration** | Python 3.11+ | ✅ Active |
| **Numerical Computing** | NumPy ≥1.24, SciPy ≥1.11 | ✅ Phase 1 |
| **Symbolic Math** | SymPy ≥1.12 | 🔨 Phase 2 |
| **Visualization** | Matplotlib ≥3.8 | ✅ Phase 1 |
| **Testing** | pytest ≥8.0, pytest-cov | ✅ 95% coverage |
| **Quality Tools** | Black, Ruff, Mypy | ✅ Black + Ruff passing |
| **Integration Layer** | LeanDojo / lean-client-python | Planned (Phase 3) |
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
│   └── lean_bridge/            # Phase 2: Python-Lean bridge (in progress)
│       ├── symbolic.py            # SymPolicMixin (sympy integration)
│       ├── serialization.py       # ODESystemMetadata (JSON schema)
│       └── proof_request.py       # LeanProofRequest API
├── tests/                   # Comprehensive test suite
│   ├── conftest.py             # Pytest fixtures (systems, ICs, config)
│   └── unit/                   # 33 unit tests, 95% coverage
│       ├── test_solver.py         # Convergence, methods, auto-fallback
│       ├── test_factory.py        # PlotterFactory registry
│       ├── test_plotters.py       # 2D/3D plotter integration
│       ├── test_plotting_api.py   # Public API dispatch
│       ├── test_plotting_config.py # PlotConfig dataclass
│       ├── test_exceptions.py     # Exception hierarchy
│       └── test_logger.py         # Logger configuration
└── lean/                    # Lean 4 formal verification (planned)
    ├── ForgeLogic.lean         # Theorem definitions (Phase 3)
    ├── lakefile.toml           # Lake build config
    └── lean-toolchain          # Pinned Lean version
```

## Current Status

### Phase 1: Numerical Foundation ✅ COMPLETE
- [x] Environment isolation (Python 3.11+ venv)
- [x] Package manifest with dependencies (numpy, scipy, matplotlib, sympy)
- [x] Generic ODE solver (method selection + auto-fallback for stiff systems)
- [x] Strategy + Factory pattern visualization (2D/3D phase portraits)
- [x] Test systems: Lorenz, Damped Pendulum, BlowUp
- [x] Comprehensive testing: 33 unit tests, 95% code coverage
- [x] Quality checks: Black + Ruff passing (Mypy deferred with documentation)
- [x] Visual validation: 7 plots with biologically relevant parameters
- [x] **Merged to main:** PR #1 (January 17, 2026)

### Phase 2: Python-Lean Bridge 🔨 IN PROGRESS (Incremental)
**Strategy:** 3 sub-phases with validation checkpoints (5-8 hours total)

**Phase 2A: SymbolicMixin Foundation (Current - Day 6)**
- [x] Architecture design complete (ADRs #10-14 documented)
- [x] Incremental implementation plan with 3 validation checkpoints
- [ ] Add SymPy dependency
- [ ] Implement SymbolicMixin (symbolic.py)
- [ ] Extend LorenzSystem with symbolic support
- [ ] Write 10+ tests for symbolic functionality
- [ ] Verify backward compatibility (Phase 1 tests pass)

**Phase 2B: JSON Serialization (Days 8-9)**
- [ ] ODESystemMetadata dataclass (serialization.py)
- [ ] Sympy → Lean string conversion helpers
- [ ] Extend DampedPendulum with symbolic support
- [ ] Write serialization tests

**Phase 2C: Proof Request API (Days 10-11)**
- [ ] LeanProofRequest dataclass (proof_request.py)
- [ ] Factory functions for conjectures
- [ ] Integration tests
- [ ] Full workflow validation

**Target:** Complete Phase 2 by Day 12 (Jan 24, 2026)

### Phase 3: Lean Formal Verification 📋 PLANNED
- [ ] Lean 4 toolchain initialization (elan/lake)
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

### Phase 1 & 2 (Current)
- **Python 3.11+** — [Download](https://www.python.org/downloads/)
- **Git** — For version control

### Phase 3 (Future - Lean Integration)
- **elan** (Lean version manager) — [Install guide](https://github.com/leanprover/elan)

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
