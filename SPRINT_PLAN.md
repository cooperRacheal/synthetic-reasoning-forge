# 6-Day Sprint Plan: Phase 1 Foundation

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

**Timeline:** Today (Monday) → Next Sunday (6 days)

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
- [ ] Step 4: ODESystem Protocol (~15 min)
- [ ] Step 5: Add NumPy/SciPy to pyproject.toml (~5 min)
- [ ] Step 6: Create systems directory structure (~5 min)

### Estimated Time
30-45 minutes total

### End-of-Day Checkpoint
- [ ] Can import Protocol
- [ ] NumPy and SciPy installed and working
- [ ] Systems directory created
- [ ] Git commit: "feat: add ODESystem protocol and dependencies"

### Notes


---

## Day 2 (Tuesday): Implement Test Systems

### Goal
Complete Steps 7-8 (Lorenz and Pendulum systems)

### Tasks
- [ ] Complete any incomplete steps from Monday
- [ ] Step 7: Implement Lorenz system (~30 min)
  - Create `src/logic/systems/lorenz.py`
  - Implement `f(t, y)` method with proper equations
  - Add parameter validation
  - Test with simple initial conditions
- [ ] Step 8: Implement Pendulum system (~30 min)
  - Create `src/logic/systems/pendulum.py`
  - Implement `f(t, y)` method
  - Add parameter validation
  - Test with simple initial conditions
- [ ] Verify both systems work with test scripts
- [ ] Update `src/logic/systems/__init__.py` to export both

### Estimated Time
1.5-2 hours

### End-of-Day Checkpoint
- [ ] Lorenz system implements ODESystem protocol
- [ ] Pendulum system implements ODESystem protocol
- [ ] Both systems pass basic smoke tests
- [ ] Git commit: "feat: implement Lorenz and Pendulum ODE systems"

### Notes


---

## Day 3 (Wednesday): Generic Solver

### Goal
Complete Step 9 (Generic solver wrapper)

### Tasks
- [ ] Step 9: Implement solve_ode() function (~45 min)
  - Create `src/logic/solver.py`
  - Wrap `scipy.integrate.solve_ivp`
  - Add error handling with `SolverConvergenceError`
  - Add logging statements
  - Type annotations with Protocol
- [ ] Test with Lorenz system
  - Verify trajectories look reasonable
  - Check logging output
- [ ] Test with Pendulum system
  - Test damped oscillation behavior
  - Verify convergence to equilibrium
- [ ] Debug any issues

### Estimated Time
2-3 hours

### End-of-Day Checkpoint
- [ ] `solve_ode()` successfully integrates Lorenz system
- [ ] `solve_ode()` successfully integrates Pendulum system
- [ ] Logging shows convergence info
- [ ] Error handling works
- [ ] Git commit: "feat: add generic ODE solver wrapper"

### Notes


---

## Day 4 (Thursday): Testing Infrastructure

### Goal
Complete Steps 10-12 (Unit tests)

### Tasks
- [ ] Step 10: Create test directory structure (~5 min)
  - `mkdir -p tests/unit`
  - `touch tests/unit/__init__.py`
- [ ] Step 11: Write tests for systems (~1 hour)
  - Create `tests/unit/test_systems.py`
  - Test Lorenz initialization, shape, known values
  - Test Pendulum initialization, shape, equilibrium
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
| 1 (Sun) | Foundation Infrastructure | ⏳ In Progress | |
| 2 (Mon) | Test Systems | 🔜 Not Started | |
| 3 (Tue) | Generic Solver | 🔜 Not Started | |
| 4 (Wed) | Testing Infrastructure | 🔜 Not Started | |
| 5 (Thu) | Quality Checks | 🔜 Not Started | |
| 6 (Fri) | Glucose-Insulin Models | 🔜 Not Started | |
| 7 (Sat) | Demo + Documentation | 🔜 Not Started | |
| 8 (Sun) | **Decision Point** | 🔜 Not Started | |

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

## Reflections

### What Went Well


### What Was Challenging


### What I Learned


### What I'd Do Differently


---

**Last Updated:** 2026-01-12
**Sprint Start:** Monday, 2026-01-12
**Sprint End:** Sunday, 2026-01-19
**Status:** Active
