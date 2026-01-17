# 7-Day Sprint Plan: Phase 1 Foundation

> **Goal:** Complete Phase 1 ODE solver infrastructure + glucose-insulin models by Sunday
>
> **Strategy:** Path A (portfolio-ready foundation) → reassess Sunday → possibly push to Path C (MVP with Lean)
>
> **Commitment:** Working more than full-time, ambitious but pragmatic
>
> **Checkpoint:** Sunday evening - decide whether to polish (Path A) or push to Lean bridge (Path C)

---

## How to Use This Document

**This file (`SPRINT_PLAN.md`):**
- ✅ Committed to git (public)
- Contains the sprint structure, milestones, and objectives
- Professional documentation for portfolio/collaboration

**For personal tracking, use `SPRINT_TRACKING.md`:**
- ❌ Gitignored (private)
- Your daily updates, blockers, frustrations, messy notes
- Write freely without worrying about polish

**Architecture documentation (`LEAN_BRIDGE_ARCHITECTURE.md`):**
- ✅ Committed to git (public)
- Technical design document for Python-Lean bridge
- Reference for Phase 2-4 implementation

---

## Sprint Overview

**Timeline:** Monday (1/12/26) to Sunday (1/18/26) - 7 Days

**Milestones:**
- Days 1-5: Complete Phase 1 (Steps 1-16)
- Day 6: Add glucose-insulin models (Phase 1.5) **Decision point**
- Day 7: Demo + documentation

---

## Day 1 (Today - Monday): Foundation Infrastructure

### Goal
Complete Steps 4-6 (Protocols, dependencies, directory structure)

### Tasks
- [x] Step 2: Exceptions ✅ (done)
- [x] Step 3: Logging ✅ (done)
- [x] Step 4: ODESystem Protocol ✅ (done Day 2)
- [x] Step 5: Add NumPy/SciPy to pyproject.toml ✅ (done Day 2)
- [x] Step 6: Create systems directory structure ✅ (done Day 2)

### Estimated Time
30-45 minutes total

### End-of-Day Checkpoint
- [x] Can import Protocol ✅
- [x] NumPy and SciPy installed and working ✅
- [x] Systems directory created ✅
- [x] Git commit: "feat: add ODESystem protocol and dependencies"

### Notes


---

## Day 2 (Tuesday): Implement Test Systems

### Goal
Complete Steps 7-8 (Lorenz and Pendulum systems)

### Tasks
- [x] Complete any incomplete steps from Monday ✅
- [x] Step 7: Implement Lorenz system (~30 min)
  - Create `src/logic/systems/lorenz.py`
  - Implement `f(t, y)` method with proper equations
  - Add parameter validation
  - Test with simple initial conditions
- [x] Step 8: Implement Pendulum system (~30 min)
  - Create `src/logic/systems/pendulum.py`
  - Implement `f(t, y)` method
  - Add parameter validation
  - Test with simple initial conditions
- [x] Verify both systems work with test scripts
- [x] Update `src/logic/systems/__init__.py` to export both

### Estimated Time
1.5-2 hours

### End-of-Day Checkpoint
- [x] Lorenz system implements ODESystem protocol
- [x] Pendulum system implements ODESystem protocol
- [x] Both systems pass basic smoke tests
- [x] Git commit: "feat: implement Lorenz and Pendulum ODE systems"

### Notes
Successful implementation of these two simple ODE system with Claude Code's guidance. Emphasis
on reviewing Python syntax and writing the code myself.

---

## Day 3 (Wednesday): Generic Solver + Trajectory Visualization

### Goal
Complete Step 9 (Generic solver wrapper) + validate with trajectory plots

### Tasks
- [x] Step 9: Implement solve_ode() function ✅ (Done Day 2, enhanced Day 5)
  - [x] Create `src/logic/solver.py`
  - [x] Wrap `scipy.integrate.solve_ivp`
  - [x] Add error handling with `SolverConvergenceError`
  - [x] Add logging statements
  - [x] Type annotations with Protocol
  - [x] Add `method` parameter for algorithm selection (RK45, LSODA, Radau, BDF) ✅ (Day 5)
  - [x] Add `auto_fallback` parameter with LSODA retry for stiff systems ✅ (Day 5)
  - [x] Update docstring with comprehensive parameter documentation ✅ (Day 5)
- [x] Test with Lorenz system ✅
  - [x] Check logging output
- [x] Test with Pendulum system ✅
- [x] Debug BlowUpSystem test ✅
- [ ] **Visualization Architecture** (in progress)
  - [x] Add matplotlib to pyproject.toml ✅
  - [x] Install matplotlib ✅
  - [x] Design extensible plotting architecture (Strategy pattern) ✅
  - [x] Create `src/logic/plotting/` subpackage ✅
  - [x] Implement `config.py` (PlotConfig dataclass) ✅
    - Base 7: figsize, dpi, style, save_format, show_grid, line_width, color
    - Added 4: alpha, marker_size, show_markers, aspect
    - Deferred: font sizes, legend control, axis limits, cmap (add Day 6+ if needed)
  - [x] Implement `base.py` (PhasePortraitPlotter ABC) ✅
  - [x] Create `plotting/__init__.py` (package marker) ✅
  - [x] Implement `plotters.py` (2D/3D concrete plotters) ✅
  - [x] Implement `factory.py` (PlotterFactory registry) ✅ (Day 5)
  - [x] Implement `__init__.py` (public API with plot_phase_portrait function) ✅ (Day 5)
  - [ ] Integrate optional plotting into solver (deferred)
  - [ ] Test: Plot Lorenz phase portrait (verify chaotic attractor)
  - [ ] Test: Plot Pendulum trajectories (verify damped oscillation)

### Estimated Time
2-3 hours (solver) + 3-4 hours (visualization architecture + OOP implementation)

### End-of-Day Checkpoint
- [x] `solve_ode()` successfully integrates Lorenz system ✅
- [x] `solve_ode()` successfully integrates Pendulum system ✅
- [x] Logging shows convergence info ✅
- [x] Error handling works (BlowUpSystem correctly raises SolverConvergenceError) ✅
- [x] Matplotlib dependency added ✅
- [x] Plotting subpackage structure created ✅
- [x] PlotConfig dataclass implemented (11 attributes) ✅
- [x] PhasePortraitPlotter ABC implemented ✅
- [x] plotting/__init__.py created (package marker) ✅
- [x] Concrete plotters (2D/3D) implemented ✅
- [x] Factory registry implemented ✅ (Day 5)
- [x] plotting/__init__.py public API (plot_phase_portrait function) ✅ (Day 5)
- [ ] Integration with solver complete (deferred)
- [ ] Visual validation: Lorenz attractor renders correctly
- [ ] Visual validation: Pendulum phase portrait shows damped oscillation
- [x] Git commit: "feat: add generic ODE solver wrapper" ✅
- [x] Git commit: "feat(plotting): implement PlotterFactory and public API" ✅ (Day 5)
- [x] Git commit: "feat(solver): add method selection and auto-fallback for stiff systems" ✅ (Day 5)

### Notes
**Day 2:** Completed solver early. Created tests/test_solver.py, added BlowUpSystem for error handling.

**Day 3 (Wed Jan 14):**
- Morning: Fixed docstrings, verified tests, committed solver
- Afternoon: Architectural design, chose Strategy + Factory pattern for extensibility
  - Created PLOTTING_OOP_ARCHITECTURE.md spec
  - Fixed editor tabs issue (GNU nano)
  - Added matplotlib dependency
- Evening: OOP learning session, implemented config.py + base.py
  - Deep dive: dataclasses, ABC, decorators, type hints, import scope
  - Implemented PlotConfig (11 attributes) and PhasePortraitPlotter ABC
  - Import tests passed

**Architectural Decision:** Strategy + Factory pattern for plotting vs simple script. Chosen for extensibility (bifurcation diagrams, Poincaré sections, 4D+ projections) and OOP learning. Trade-off: 3-4 hour investment for production-grade reusable infrastructure. Documented in PORTFOLIO_NOTES.md ADR #1.

**Day 3 Continuation (Wed evening):**
- Implemented plotters.py: TwoDimensionalPlotter and ThreeDimensionalPlotter
- Deep OOP learning: 2D vs 3D matplotlib API differences, negative indexing, array shapes
- Fixed multiple syntax errors with guidance (typos, indentation, list wrapping for 3D)
- Learned: y shape (3, n_points) = 2D array holding 3D system trajectory
- Learned: 3D axes require sequences `[value]` not scalars for single points
- Learned: negative indexing `y[:, -1]` = last element, length-agnostic

**Status:** ~75% complete Day 3 visualization work. Remaining: factory.py, __init__.py public API, integration, visual validation.


---

## Day 4 (Thursday): Testing Infrastructure

### Goal
Complete Steps 10-12 (Unit tests)

### Tasks
- [ ] Step 10: Create test directory structure (~5 min)
  - `mkdir -p tests/unit`
  - `touch tests/unit/__init__.py`
- [ ] Step 11: Write tests for systems (~1 hour)
  -x- Create `tests/unit/test_systems.py` (Done Day 2)
  -x- Test Lorenz initialization, shape, known values (Done Day 2)
  -x- Test Pendulum initialization, shape, equilibrium (Done Day 2)
  - Test error cases (wrong dimensions)
- [ ] Step 12: Write tests for solver (~1.5 hours)
  - Create `tests/unit/test_solver.py`
  - Test exponential decay (known solution)
  - Test harmonic oscillator (energy conservation)
  - Test with different methods (RK45, LSODA)
  - Test error handling
- [ ] Run full test suite: `pytest tests/unit/ -v`
- [ ] Check coverage: `pytest tests/unit/ --cov=src/logic --cov-report=term-missing`
- [ ] Fix failing tests

### Estimated Time
3-4 hours

### End-of-Day Checkpoint
- [ ] All tests passing (100% pass rate)
- [ ] Coverage ≥ 80%
- [ ] No mypy errors
- [ ] Git commit: "test: add comprehensive unit tests for systems and solver"

### Notes


---

## Day 5 (Friday): Quality Checks + Package Update

### Goal
Complete Steps 13-14 (Quality tooling)

### Tasks
- [ ] Step 13: Update `src/logic/__init__.py` (~10 min)
  - Export `solve_ode`, `LorenzSystem`, `DampedPendulum`
  - Export exceptions
  - Add `__version__` and `__all__`
- [ ] Step 14: Run quality checks
  - **Black:** `black src/ tests/`
  - **Ruff:** `ruff check src/ tests/`
  - **Mypy:** `mypy src/`
  - **Pytest:** `pytest tests/ -v --cov=src/logic --cov-report=term-missing`
- [ ] Fix any issues (~1 hour)
  - Type errors from mypy
  - Linting warnings from ruff
  - Missing imports
- [ ] Verify all checks pass
- [ ] Commit to git branch

### Estimated Time
2-3 hours

### End-of-Day Checkpoint
- [ ] Black: ✓ All files formatted
- [ ] Ruff: ✓ No linting errors
- [ ] Mypy: ✓ No type errors
- [ ] Pytest: ✓ All tests pass, 80%+ coverage
- [ ] Git commit: "chore: pass all quality checks (black, ruff, mypy)"

### **Phase 1 Complete! 🎉**

### Notes


---

## Day 6 (Saturday): Glucose-Insulin Models

### Goal
Implement glucose and insulin minimal models (Phase 1.5)

### Tasks
- [ ] **Refactor PlotterFactory registry to Enum keys** (~30 min)
  - Create PlotType enum in factory.py
  - Update registry: int keys → Enum keys (PlotType.PHASE_2D, etc.)
  - Update create() signature: `create(plot_type: PlotType, ...)`
  - Update plot_phase_portrait() to infer PlotType from dimensionality
  - Fix tests to use PlotType enum
  - **Rationale:** int keys insufficient for bifurcation diagrams (2D but not phase portraits)
  - **Context:** Technical debt from Day 5, documented in DESIGN_DECISIONS.md
- [ ] Implement `GlucoseMinimalModel` (~1 hour)
  - Create `src/logic/systems/glucose.py`
  - Equations 9-10 from Van Riel paper
  - Parameters: k1, k2, k3, Gb, Ib
  - Handle insulin input I(t) via interpolation
  - Add docstrings with biological context
- [ ] Implement `InsulinMinimalModel` (~1 hour)
  - Create `src/logic/systems/insulin.py`
  - Equation 12 from Van Riel paper
  - Parameters: k, γ, GT
  - Handle glucose input G(t) via interpolation
  - Event handling for G(t) > GT threshold
- [ ] Add FSIGT test data (~30 min)
  - Create `data/fsigt_test_data.py` or `.csv`
  - Van Riel paper Appendix A data
  - Time, glucose, insulin measurements
- [ ] Write unit tests (~1 hour)
  - Create `tests/unit/test_glucose_insulin.py`
  - Test system initialization
  - Test f() returns correct shape
  - Test parameter bounds (SI, SG in normal ranges)
- [ ] Basic parameter estimation script (~1.5 hours)
  - Create `scripts/fit_glucose_model.py`
  - Use `scipy.optimize.least_squares`
  - Fit k1, k2, k3, G0 to Van Riel data
  - Print estimated SI and SG
  - Compare to published values

### Estimated Time
5-6 hours

### End-of-Day Checkpoint
- [ ] Glucose model solves successfully
- [ ] Insulin model solves successfully
- [ ] Can fit glucose model to Van Riel data
- [ ] Estimated SI and SG in normal ranges
- [ ] Git commit: "feat: implement glucose-insulin minimal models with parameter estimation"

### Notes


---

## Day 7 (Sunday): Demo + Documentation

### Goal
Create demo script and polish

### Tasks
- [ ] Step 15: Create demo script (~1 hour)
  - Create `scripts/demo_solver.py`
  - Demonstrate Lorenz system
  - Demonstrate Pendulum system
  - Demonstrate Glucose-insulin system
  - Print summary statistics
- [ ] Create Jupyter notebook (~2 hours)
  - Create `notebooks/glucose_insulin_demo.ipynb`
  - Load Van Riel FSIGT data
  - Fit glucose minimal model
  - Fit insulin minimal model
  - Visualize trajectories
  - Compare to published results
  - Add markdown explanations
- [ ] Polish README (optional) (~30 min)
  - Add usage examples
  - Add installation instructions
  - Update status checklist
- [ ] Final quality check
  - Run all tests
  - Run all quality tools
  - Verify demo script works
- [ ] Commit everything to git
  - Clean commit history
  - Meaningful commit messages
  - Push to remote (optional)

### Estimated Time
4-5 hours

### End-of-Day Checkpoint
- [ ] Demo script runs successfully
- [ ] Jupyter notebook renders nicely
- [ ] All code committed to git
- [ ] README updated
- [ ] Ready for Sunday checkpoint

### **Phase 1.5 Complete! 🎉**

### Notes


---

## Day 8 (Monday): Decision Point

### Goal
Assess progress and decide next steps

### Assessment Questions

1. **How complete is Phase 1?**
   - [ ] All Steps 1-16 complete
   - [ ] Tests passing with 80%+ coverage
   - [ ] Quality checks all pass

2. **How well do glucose-insulin models work?**
   - [ ] Successfully fit to Van Riel data
   - [ ] Parameters in expected ranges
   - [ ] Visualizations look correct

3. **How polished is the codebase?**
   - [ ] Clean, documented code
   - [ ] Good test coverage
   - [ ] Ready to show others

4. **How much energy/time do you have left?**
   - [ ] Burned out → Need to wrap up
   - [ ] Energized → Ready to push forward

### Decision Options

#### **Option A: Polish and Present (Safe Choice)**

**What to do:**
- Finalize documentation
- Clean up any rough edges
- Create portfolio-ready README
- Maybe add CI/CD (GitHub Actions)
- **Outcome:** Solid, demonstrable work you can show now

**Time needed:** 1-2 more days

#### **Option B: Push to Lean Bridge (Ambitious MVP)**

**What to do:**
- Week 2 Days 8-10: Learn Lean 4 basics
- Week 2 Days 11-12: Minimal Python-Lean bridge
- Week 2 Days 13-14: Formalize one simple system
- **Outcome:** End-to-end Python → Lean demo (even if rough)

**Time needed:** Full second week (6-7 more days)

#### **Option C: Hybrid Approach**

**What to do:**
- Days 8-9: Polish Phase 1, make it portfolio-ready
- Days 10-14: Start Lean exploration (lower pressure)
- **Outcome:** Polished Phase 1 + early Lean experiments

**Time needed:** 1 week

### My Decision

**I choose:** [ A / B / C ]

**Reasoning:**


**Next steps:**


---

## What If You're Ahead of Schedule?

If you finish early, add these **bonus items** (in priority order):

1. **Coverage report:** `pytest --cov=src/logic --cov-report=html`
   - View detailed coverage: `open htmlcov/index.html`

2. **Combined minimal model:** Solve glucose + insulin together as coupled system

3. **Visualization:**
   - Phase portraits for Lorenz attractor
   - Parameter sensitivity analysis for glucose model
   - Matplotlib or plotly plots

4. **CI/CD:**
   - Create `.github/workflows/tests.yml`
   - Run tests on every push
   - Add status badge to README

5. **More systems:**
   - Lotka-Volterra (predator-prey)
   - SIR epidemic model
   - Van der Pol oscillator

---

## Daily Standups

At the end of each day, update the SPRINT_TRACKING.md file with:

### Day X Standup

**Completed:**
-

**Blockers/Questions:**
-

**Tomorrow's Focus:**
-

**Overall Status:** [On track / Behind / Ahead]

---

## Progress Tracker

| Day | Goal | Status | Notes |
|-----|------|--------|-------|
| 1 (Mon) | Foundation Infrastructure | ✅ Complete | Steps 4-6 done Day 2 |
| 2 (Tue) | Test Systems | ✅ Complete | Steps 7-8 done Day 2 |
| 3 (Wed) | Generic Solver + Visualization | ⏳ In Progress | Solver done, plotters.py done, factory/API remain |
| 4 (Thu) | Testing Infrastructure | 🔜 Not Started | |
| 5 (Fri) | Quality Checks | 🔜 Not Started | |
| 6 (Sat) | Glucose-Insulin Models | 🔜 Not Started | |
| 7 (Sun) | Demo + Documentation | 🔜 Not Started | |
| 8 (Mon) | **Decision Point** | 🔜 Not Started | |

**Legend:**
- 🔜 Not Started
- ⏳ In Progress
- ✅ Complete
- ⚠️ Blocked
- ⏭️ Skipped

---

## Week 2 Preview (If Option B Chosen)

### Days 8-10: Learn Lean 4 Basics

**Resources:**
- [Theorem Proving in Lean 4](https://leanprover.github.io/theorem_proving_in_lean4/)
- [Mathlib4 Documentation](https://leanprover-community.github.io/mathlib4_docs/)
- [Lean 4 VS Code Extension](https://marketplace.visualstudio.com/items?itemName=leanprover.lean4)

**Tasks:**
- Install Lean 4 toolchain
- Complete first 5 chapters of TPiL4
- Study Mathlib ODE examples
- Write first simple proof

### Days 11-12: Minimal Python-Lean Bridge

**Tasks:**
- Design JSON schema for system representation
- Create Lean subprocess runner
- Test Python → Lean communication
- Handle basic errors

### Days 13-14: Formalize One Simple System

**Tasks:**
- Formalize exponential decay in Lean
- Prove stability theorem
- End-to-end demo: Python sends system → Lean proves property
- Document the workflow

---

## Deferred Features

### Solver Plotting Integration (Optional Convenience)
**Status:** Deferred to future sprint
**Reason:** Non-critical convenience feature, behind schedule on Phase 1 core

**Proposed Feature:**
Add optional plotting parameters to `solve_ode()` for one-line solve+plot workflow:
```python
# Current (two-step, fully functional)
sol = solve_ode(system, t_span, y0)
plot_phase_portrait(sol.t, sol.y, save_path='output.png')

# Future (one-step convenience)
sol = solve_ode(system, t_span, y0, plot=True, save_path='output.png')
```

**Implementation:**
- Add `plot: bool = False` parameter
- Add `plot_config: Optional[PlotConfig] = None` parameter
- Add `save_path: Optional[str] = None` parameter
- Lazy import: `from src.logic.plotting import plot_phase_portrait` inside `if plot:` block
- Forward reference: `Optional["PlotConfig"]` to avoid circular import

**Trade-offs:**
- ✓ Convenience (one line instead of two)
- ✗ Couples solver to plotting (violates separation of concerns)
- ✗ Added complexity for minimal gain
- ✗ Current two-step workflow already clean

**Decision:** Implement if time permits after Phase 1 completion. Not required for core functionality.

---

## Reflections

### What Went Well


### What Was Challenging


### What I Learned


### What I'd Do Differently


---

**Last Updated:** 2026-01-14
**Sprint Start:** Monday, 2026-01-12
**Sprint End:** Sunday, 2026-01-19
**Status:** Active
