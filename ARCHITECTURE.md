# Architecture Decision Records

> **Purpose:** Document significant design choices and their rationale
> **Scope:** Phase 1 implementation decisions (ODE solver + visualization)
> **Last Updated:** 2026-01-17

**Note:** This file documents WHAT was decided and WHY. For WHEN and HOW implementation progressed, see notes/SPRINT_TRACKING.md. For future architecture (Phases 2-3), see notes/PHASE2_3_LEAN_BRIDGE.md.

---

## ADR #1: Strategy + Factory Pattern for Visualization

**Decision:** Implement extensible plotting architecture using Strategy + Factory patterns instead of simple plotting functions.

**Alternatives Considered:**
1. **Simple plotting functions** (plot_2d, plot_3d)
   - Pro: Fast implementation, minimal code
   - Con: Not extensible, duplicates logic across functions
2. **Single class with if/else branching**
   - Pro: Centralized, easy to understand
   - Con: Violates Open/Closed Principle, grows complex
3. **Strategy + Factory pattern** [CHOSEN]
   - Pro: Extensible, testable, demonstrates OOP mastery
   - Con: More upfront time investment

**Rationale:**
- Enables future visualization types (bifurcation diagrams, Poincaré sections) without modifying existing code
- Demonstrates production-grade OOP design for portfolio
- Factory provides single entry point despite multiple plotter implementations
- Visual validation more intuitive than numerical logs for solver correctness

**Trade-offs Accepted:**
- 3-4 hour investment vs 30 min for simple functions
- Schedule slippage (Day 3 extended into Days 4-5)
- Worth it: Stronger architectural foundation, deep OOP learning

**Impact:**
- Visualization layer extensible via Open/Closed Principle
- Portfolio demonstrates design pattern mastery
- Factory automatically selects correct plotter based on data dimensionality

---

## ADR #2: Validation Script Over Notebook

**Decision:** Use standalone Python script (examples/validate_plotting.py) instead of Jupyter notebook for architecture validation.

**Alternatives Considered:**
- Jupyter notebook (interactive, markdown explanations)
- Interactive matplotlib with plt.show() (immediate feedback)

**Rationale:**
- Version control friendly (text-based, no JSON metadata)
- Reproducible (no execution order issues)
- Runnable in CI/CD
- Faster iteration during development
- Clear entry point for validation

**Future Consideration:**
May create notebook later for glucose-insulin demos where step-by-step explanation adds value.

---

## ADR #3: PlotterFactory Registry - int Keys Now, Enum Later

**Decision:** Use int keys (dimensionality) for factory registry in Phase 1, defer Enum refactoring to future sprint.

**Problem:**
int keys create semantic collision - multiple plot types (phase portraits, bifurcation diagrams, time series) can share same dimensionality (2D) but require different plotters.

**Alternatives Considered:**
1. **String keys** ('phase_2d', 'bifurcation')
   - Pro: Flexible, human-readable
   - Con: No type safety, typo-prone
2. **Enum keys** (PlotType.PHASE_2D, PlotType.BIFURCATION)
   - Pro: Type-safe, IDE autocomplete, explicit semantics
   - Con: Requires import, more verbose
3. **Hierarchical registries** (separate per plot family)
   - Pro: Clear separation
   - Con: More complexity, multiple factories

**Decision Rationale:**
- YAGNI: Phase 1 only needs phase portraits (2D, 3D)
- Behind schedule: Simple int keys unblock current work
- Documented technical debt for future refactoring
- Current implementation sufficient for Phase 1 scope

**Future Refactoring Plan:**
```python
class PlotType(Enum):
    PHASE_2D = "phase_2d"
    PHASE_3D = "phase_3d"
    BIFURCATION = "bifurcation"
```

---

## ADR #4: Solver Method Selection + Auto-Fallback

**Decision:** Add `method` and `auto_fallback` parameters to solve_ode() for robust handling of stiff systems.

**Problem:**
Hardcoded RK45 method fails on stiff systems (widely separated timescales).

**Implementation:**
```python
solve_ode(system, t_span, y0, method="RK45", auto_fallback=True)
```

**Cascading Error Handling:**
1. Try user-specified method
2. If fails AND auto_fallback=True AND method ≠ LSODA → retry with LSODA
3. If still fails → raise SolverConvergenceError

**Rationale:**
- Robustness: Handles stiff systems automatically (glucose-insulin models likely stiff)
- User control: Advanced users can specify method explicitly
- Smart default: LSODA auto-detects stiffness, handles 90% of edge cases
- Guard clause (method ≠ LSODA) prevents infinite retry loop

**Trade-offs:**
- Added complexity vs hardcoded method
- Worth it: Handles broader class of systems, demonstrates numerical methods understanding

---

## ADR #5: Defer Solver Plotting Integration

**Decision:** Keep current two-step workflow (solve → plot separately), defer one-step integration as optional convenience feature.

**Current Workflow (Retained):**
```python
sol = solve_ode(system, t_span, y0)
plot_phase_portrait(sol.t, sol.y, save_path='output.png')
```

**Proposed Workflow (Deferred):**
```python
sol = solve_ode(system, t_span, y0, plot=True, save_path='output.png')
```

**Rationale for Deferral:**
- Separation of concerns: Solver focused on solving, plotter on visualization
- Behind schedule: Focus on core functionality
- Minimal value: Convenience feature, not critical
- Coupling concern: Integration couples solver to plotting layer

**Trade-offs:**
- Current: Clean separation, testable in isolation, can plot experimental data without solver
- Proposed: One line instead of two (minor convenience)
- Decision: Clean architecture > convenience under time pressure

---

## ADR #6: Data Flow - Plotters Operate on Solution Arrays

**Decision:** Plotters consume pre-computed solution arrays (t, y), not ODESystem objects.

**Architecture:**
```
ODESystem → solve_ode() → Solution (t, y) → plot_phase_portrait(t, y)
```

**NOT:**
```
ODESystem → plot_phase_portrait(system, t_span, y0)  [plotter calls solver]
```

**Rationale:**

1. **Decoupling - Reusable across contexts:**
   - ODE solver output
   - Experimental data (no system!)
   - Bifurcation analysis (multiple systems)

2. **Performance - Avoid redundant computation:**
   - Solve once, visualize multiple ways
   - No recomputation when changing plot styles

3. **Testing - Synthetic data:**
   - Test plotter without running expensive solver
   - Use fake arrays for unit tests

**Analogy:**
Data analysis pipeline doesn't re-run statistical model for each visualization - it visualizes pre-computed results.

---

## ADR #7: Textbook/Biologically Relevant Defaults

**Decision:** Add scientifically meaningful default parameters to ODE systems, document literature sources.

**LorenzSystem Defaults (Dimensionless):**
- σ = 10, ρ = 28, β = 8/3
- Classic Lorenz 1963 parameters producing butterfly attractor

**DampedPendulum Defaults:**
- L = 1.0 m, m = 1.0 kg, b = 0.2 N·m·s/rad, g = 9.81 m/s²
- Textbook values for standard pendulum

**Validation Script:** Uses b = 0.5 for biological relevance (human limb swing).

**Literature Documentation:** notes/REFERENCES.md
- Collins et al. (2009): Arms as passive pendulums during gait
- Maus et al. (2016): Springy pendulum model for leg swing

**Rationale:**
- Reproducibility: Systems usable out-of-box
- Educational value: Defaults represent canonical literature values
- Portfolio rigor: Demonstrates research beyond arbitrary numbers
- Biological context: Validation uses physiologically relevant parameters

---

## ADR #8: matplotlib as Main Dependency (Not Dev-Only)

**Decision:** Add matplotlib>=3.8,<4.0 to project.dependencies (not dev dependencies).

**Alternatives:**
- Dev dependencies only
- Optional visualization dependencies

**Rationale:**
- Visualization is core validation workflow, not optional
- Future work (glucose-insulin parameter fitting) requires plotting
- Version >=3.8 ensures numpy 2.x compatibility
- Standard in scientific Python stack (numpy, scipy, matplotlib trinity)

---

## ADR #9: Plotter Testing Strategy - Integration First, Mocking Later

**Decision:** Test plotters using integration approach (call plot(), verify returns Figure) rather than comprehensive matplotlib mocking. Defer mocking enhancement to future phase if needed.

**Alternatives Considered:**

1. **Option 1: Comprehensive matplotlib mocking** (pytest-mock/unittest.mock)
   - Pro: Isolates plotter logic from matplotlib, verifies exact method calls
   - Con: Brittle (tight coupling to matplotlib API), complex test setup, high maintenance
   - Tests: Mock `plt.subplots()`, `ax.plot()`, `ax.set_xlabel()`, etc. Verify called with correct parameters.

2. **Option 2: Integration testing** [CHOSEN for Phase 1]
   - Pro: Simple, fast to write, tests actual behavior, less brittle
   - Con: Doesn't verify internal matplotlib calls, slower tests (creates actual figures)
   - Tests: Call `plot()` with synthetic data, verify returns `plt.Figure`, verify file saved if `save_path` provided

**Rationale:**
- **Time pressure:** Day 6 testing sprint - Option 2 delivers coverage faster
- **Brittleness concern:** Mocking matplotlib tightly couples tests to implementation details (if we refactor plotting code but maintain behavior, mocked tests would break)
- **Sufficient coverage:** Option 2 validates plotters produce figures and respect parameters (file saving, config)
- **Portfolio value:** Demonstrates pragmatic testing trade-offs under schedule constraints

**Current tests (Option 2):**
- `test_2d_plotter_returns_figure` - Verify returns matplotlib Figure object
- `test_3d_plotter_returns_figure` - Same for 3D
- `test_2d_plotter_default_labels` - Call without labels, verify no error
- `test_3d_plotter_default_labels` - Same for 3D
- `test_2d_plotter_saves_file` - Provide save_path, verify file created
- `test_3d_plotter_saves_file` - Same for 3D

**Future enhancement (Option 1):**
If production issues arise from untested matplotlib interactions, or for portfolio polish demonstrating mocking expertise, add comprehensive mocking tests that verify:
- Correct matplotlib methods called (`plot()`, `set_xlabel()`, `legend()`, etc.)
- Parameters passed correctly (line width, colors, marker sizes from PlotConfig)
- Conditional logic (markers only shown if `config.show_markers=True`)

**Trade-off:** Pragmatic coverage now, detailed verification deferred.

---

## Future Enhancements

### Solver Timeout Parameter

**Consider adding:** Wall-clock timeout parameter to `solve_ode()` to prevent indefinite execution in production scenarios.

**Motivation:**
- Pathological systems (e.g., finite-time singularities) or stiff problems may cause solver hangs
- Current mitigation: `auto_fallback=True` helps but doesn't guarantee termination
- Production use cases may require hard timeout constraints

**Proposed API:**
```python
solve_ode(system, t_span, y0, method="RK45", auto_fallback=True, timeout=30.0)
```

**Implementation Challenges:**
- scipy's solve_ivp has no built-in wall-clock timeout
- Signal-based timeouts (signal.alarm) not portable to Windows
- Threading-based interrupts may not work reliably with C-level numerical code
- Process-based timeout (concurrent.futures) adds serialization/overhead complexity

**Current Workaround:**
Users can wrap `solve_ode()` calls in their own timeout mechanism if needed.

**Decision:** Deferred to future phase due to complexity vs. benefit trade-off and scipy API limitations.

### Additional Test Coverage (If Needed)

**Consider adding:** Error message validation, logging output tests, numerical accuracy tests against analytical solutions.

**Deferred test types:**

1. **Error Message Validation** (TestErrorHandling)
   - Would verify: Exception messages contain method names, descriptive failure info
   - Skipped: Brittle (message wording changes break tests), low value (exception type sufficient), presentation not behavior

2. **Logging Output Tests** (TestLogging)
   - Would verify: Log statements present, fallback warnings emitted, method selection logged
   - Skipped: Brittle (log formatting changes break tests), observability not correctness, validated during manual testing

3. **Numerical Accuracy Tests** (TestNumericalAccuracy)
   - Would verify: Solutions match analytical reference (exponential decay, harmonic oscillator)
   - Skipped: Thin wrapper around scipy (trust upstream accuracy), system implementations simple (literature formulas), current tests validate wiring (IC preservation, endpoints)
   - Value: Medium for catching system equation bugs, but systems tests verify physical behavior

**When to add:** If production issues arise from missing validation, or for portfolio polish demonstrating numerical methods rigor.

**Current coverage (Day 6):** 8 behavioral tests validate solver correctness (convergence, method selection, error handling, auto-fallback).

### Mypy Strict Mode Type Checking

**Consider adding:** Full mypy strict mode compliance with type stubs for scipy and matplotlib.

**Current Status (Day 6):**
- Black ✅ (formatting passing)
- Ruff ✅ (linting passing)
- Mypy ❌ (7 errors with strict mode, deferred)

**Mypy Errors Found (mypy -p src.logic --strict):**

1. **Missing Type Stubs (1 error):**
   - `src/logic/solver.py:9` - Library stubs not installed for "scipy.integrate"
   - Fix: `pip install scipy-stubs` (may reveal additional scipy type issues)

2. **plt.Figure Type Not Recognized (4 errors):**
   - `src/logic/plotting/base.py:25` - Name "plt.Figure" is not defined
   - `src/logic/plotting/plotters.py:26, 122` - Name "plt.Figure" is not defined
   - `src/logic/plotting/__init__.py:73` - Name "plt.Figure" is not defined
   - Fix: Install matplotlib type stubs or add `from matplotlib.figure import Figure` and use `Figure` instead of `plt.Figure` in type hints

3. **Type Narrowing Issue (1 error):**
   - `src/logic/plotting/plotters.py:96` - Argument 1 to "set_aspect" of "_AxesBase" has incompatible type "str"; expected "Literal['auto', 'equal'] | float"
   - Current: `ax.set_aspect(config.aspect)` where `config.aspect: str`
   - Fix: Change PlotConfig.aspect type hint to `Literal["auto", "equal"] | float` or add runtime type narrowing

4. **Signature Mismatch (1 error):**
   - `src/logic/plotting/__init__.py:132` - Unexpected keyword argument "config" for "plot" of "PhasePortraitPlotter"
   - Root cause: Base class `PhasePortraitPlotter.plot()` signature missing `config` parameter
   - Fix: Add `config: PlotConfig | None = None` to abstract method signature in `base.py:17`

**Why Deferred:**
- **Time pressure:** Day 6 testing sprint focused on test coverage (95% achieved)
- **Dependency complexity:** scipy-stubs and matplotlib type stubs may introduce new type errors requiring investigation
- **Diminishing returns:** Black + Ruff already catch formatting and common linting issues
- **Current quality sufficient:** Type hints exist and are mostly correct, mypy strict mode catches edge cases

**When to Add:**
- **Before Phase 2:** Lean integration will benefit from strict type checking (subprocess communication, JSON serialization)
- **Portfolio polish:** Demonstrates understanding of Python type system and professional tooling
- **Production readiness:** Strict type checking valuable for team collaboration and refactoring safety

**Estimated effort:** 1-2 hours (install stubs, fix 7 errors, address any new errors revealed by stubs)

**Workaround:**
Current quality target runs `black` + `ruff` only. Mypy commented out in Makefile with reference to this documentation.

---

## Timeline Reference

See SPRINT_TRACKING.md for detailed timeline of when these decisions were made and how implementation progressed.
