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

## Phase 2: Python-Lean Bridge Architecture

### ADR #10: Symbolic Equation Strategy - Mixin Pattern

**Decision:** Add symbolic equation capabilities to ODE systems via `SymbolicMixin` class with lazy symbolic generation using sympy.

**Alternatives Considered:**

1. **Modify existing classes in-place** (add `to_symbolic()` method directly to LorenzSystem)
   - Pro: Simple, direct, no additional classes
   - Con: Violates Open/Closed Principle, couples numerical computation to symbolic representation
   - Con: Forces all systems to have symbolic support even if unused

2. **Wrapper classes** (SerializableLorenzSystem wraps LorenzSystem)
   - Pro: Clean separation of concerns
   - Con: Boilerplate code duplication for each system
   - Con: Dual class hierarchy (LorenzSystem vs SerializableLorenzSystem)
   - Con: Violates DRY principle

3. **Mixin Pattern** [CHOSEN]
   - Pro: Composable via multiple inheritance
   - Pro: Backward compatible (existing code unchanged)
   - Pro: Single class definition (no wrappers)
   - Pro: Reusable across all systems
   - Con: Requires understanding multiple inheritance
   - Con: Mixin methods added to class namespace

**Architecture:**

```python
# src/logic/lean_bridge/symbolic.py

class SymbolicMixin:
    """Mixin adding symbolic equation capabilities to ODE systems."""

    def get_symbolic_equations(self) -> dict[str, sp.Expr]:
        """Lazy generation with caching."""
        if not hasattr(self, '_symbolic_cache'):
            self._symbolic_cache = self._build_symbolic_equations()
        return self._symbolic_cache

    def get_state_variables(self) -> list[str]:
        """Return state variable names."""
        return self._state_var_names

    def _build_symbolic_equations(self) -> dict[str, sp.Expr]:
        """Override in subclass."""
        raise NotImplementedError


# Usage in existing systems:
class LorenzSystem(SymbolicMixin):
    _state_var_names = ['x', 'y', 'z']

    def f(self, t, y):
        # Numerical implementation UNCHANGED
        ...

    def _build_symbolic_equations(self):
        x, y, z = sp.symbols('x y z')
        return {
            'x': self.sigma * (y - x),
            'y': x * (self.rho - z) - y,
            'z': x * y - self.beta * z
        }
```

**Rationale:**
- **Backward compatible:** Existing numerical code sees no changes (LorenzSystem still works identically)
- **On-demand generation:** Symbolic equations only created when explicitly requested (no overhead for solver)
- **Cacheable:** Lazy evaluation via `_symbolic_cache` prevents regeneration on repeated calls
- **Extensible:** Other systems inherit mixin, implement one method (`_build_symbolic_equations()`)
- **Testable:** Can mock `_build_symbolic_equations()`, verify symbolic output independently

**Trade-offs Accepted:**
- **Complexity:** Mixin pattern less familiar than direct method addition
- **Mitigation:** Excellent documentation, simple mixin implementation (no state, no complex logic)
- **Namespace pollution:** Mixin adds 3 methods to each system class
- **Mitigation:** All methods prefixed appropriately (`get_*`, `_build_*`)

**Impact:**
- Enables Lean bridge without modifying Phase 1 solver
- Future systems automatically get symbolic support by inheriting mixin
- JSON serialization can extract symbolic equations for Lean formalization

---

### ADR #11: JSON Serialization Schema

**Decision:** Create `ODESystemMetadata` dataclass capturing system type, parameters, state variables, and symbolic equations for Lean bridge communication.

**JSON Schema:**

```json
{
  "system_type": "LorenzSystem",
  "state_dim": 3,
  "state_variables": ["x", "y", "z"],
  "parameters": {
    "sigma": 10.0,
    "rho": 28.0,
    "beta": 2.6666666666666665
  },
  "equations": {
    "x": "sigma*(y - x)",
    "y": "x*(rho - z) - y",
    "z": "x*y - beta*z"
  }
}
```

**Alternatives Considered:**

1. **Minimal schema** (just equations and parameters)
   - Pro: Smaller payload
   - Con: Lean cannot reconstruct system type or validate dimensionality

2. **Verbose schema** (include Jacobian, equilibria, stability analysis)
   - Pro: Rich metadata for Lean
   - Con: Premature - Phase 2 doesn't need this yet
   - Con: Couples serialization to analysis results

3. **Five-field schema** [CHOSEN]
   - Pro: Self-contained (Lean can reconstruct system)
   - Pro: Extensible (add fields later without breaking)
   - Pro: Minimal but sufficient
   - Con: Slightly verbose for simple cases

**Implementation:**

```python
# src/logic/lean_bridge/serialization.py

@dataclass
class ODESystemMetadata:
    """JSON-serializable metadata for ODE systems."""

    system_type: str  # Class name (e.g., "LorenzSystem")
    state_dim: int  # Dimension of state space
    state_variables: list[str]  # Variable names (e.g., ['x', 'y', 'z'])
    parameters: dict[str, float]  # Numeric parameters
    equations: dict[str, str]  # Symbolic equations (sympy → string)

    def to_json(self) -> dict[str, Any]:
        """Convert to JSON-compatible dict."""
        return asdict(self)

    @classmethod
    def from_ode_system(cls, system: Any) -> "ODESystemMetadata":
        """Extract metadata from system implementing SymbolicODESystem."""
        symbolic_eqs = system.get_symbolic_equations()
        state_vars = system.get_state_variables()

        equations_str = {
            var: _sympy_to_lean_string(expr)
            for var, expr in symbolic_eqs.items()
        }

        parameters = _extract_parameters(system)

        return cls(
            system_type=type(system).__name__,
            state_dim=len(state_vars),
            state_variables=state_vars,
            parameters=parameters,
            equations=equations_str
        )
```

**Rationale:**
- **Self-contained:** All information needed for Lean formalization
- **Type-safe:** Dataclass provides structure validation
- **Round-trip capable:** JSON serializable and deserializable
- **Extensible:** Can add fields (equilibria, Jacobian, etc.) without breaking existing code
- **Lean-compatible:** String equations can be parsed by Lean subprocess

**Trade-offs Accepted:**
- **Sympy → String conversion:** May not perfectly match Lean syntax initially
- **Mitigation:** Phase 2.5 will refine `_sympy_to_lean_string()` with Lean parser feedback
- **Parameter extraction fragility:** Relies on introspection (may grab wrong attributes)
- **Mitigation:** Whitelist numeric public attributes only, add manual override option if needed

**Future Extensions:**
- Add `equilibria: list[NDArray]` field
- Add `jacobian: dict[str, dict[str, str]]` field (symbolic Jacobian matrix)
- Add `metadata: dict[str, Any]` for custom annotations

---

### ADR #12: LeanProofRequest API

**Decision:** Create `LeanProofRequest` dataclass packaging mathematical conjectures for Lean verification, with method to generate Lean-compatible JSON.

**Architecture:**

```python
# src/logic/lean_bridge/proof_request.py

@dataclass
class LeanProofRequest:
    """Package mathematical conjecture for Lean verification."""

    system1: ODESystemMetadata
    system2: ODESystemMetadata
    conjecture_type: str  # "structural_isomorphism", "stability_equivalence", etc.
    parameter_correspondence: dict[str, str]  # e.g., {'k1/k3': 'Kp'}

    def to_lean_json(self) -> dict[str, Any]:
        """Generate JSON payload for Lean subprocess."""
        return {
            "system1": self.system1.to_json(),
            "system2": self.system2.to_json(),
            "conjecture": {
                "type": self.conjecture_type,
                "parameter_correspondence": self.parameter_correspondence,
                "hypothesis": self._generate_hypothesis_string()
            }
        }

    def _generate_hypothesis_string(self) -> str:
        """Generate human-readable hypothesis."""
        if self.conjecture_type == "structural_isomorphism":
            return (
                f"There exists a diffeomorphism φ: ℝ^{self.system1.state_dim} → "
                f"ℝ^{self.system2.state_dim} such that the dynamics are conjugate"
            )
        return f"Conjecture of type {self.conjecture_type}"


# Factory function
def create_structural_isomorphism_request(
    system1: Any,
    system2: Any,
    param_map: dict[str, str]
) -> LeanProofRequest:
    """Create structural isomorphism conjecture."""
    return LeanProofRequest(
        system1=ODESystemMetadata.from_ode_system(system1),
        system2=ODESystemMetadata.from_ode_system(system2),
        conjecture_type="structural_isomorphism",
        parameter_correspondence=param_map
    )
```

**Usage Example:**

```python
from src.logic.systems import LorenzSystem, DampedPendulum
from src.logic.lean_bridge import create_structural_isomorphism_request

lorenz = LorenzSystem(sigma=10.0, rho=28.0, beta=8/3)
pendulum = DampedPendulum(length=1.0, damping=0.5)

request = create_structural_isomorphism_request(
    lorenz, pendulum,
    param_map={'sigma/beta': 'damping/mass'}
)

lean_json = request.to_lean_json()
# Future: subprocess_runner.verify(lean_json)
```

**Rationale:**
- **Clean API:** Factory functions provide intuitive conjecture creation
- **Type-safe:** Dataclass ensures required fields present
- **JSON-serializable:** Ready for subprocess communication (Phase 2.5)
- **Extensible:** Add new conjecture types without breaking existing code
- **Testable:** Mock Lean subprocess, verify JSON structure

**Conjecture Types Planned:**
- `"structural_isomorphism"` - Diffeomorphism conjugating dynamics
- `"stability_equivalence"` - Same stability properties
- `"parameter_correspondence"` - Mathematical relationship between parameters
- `"conservation_law"` - Preserved quantities

**Future Extensions:**
- Add `@dataclass` field for Lean timeout
- Add `@dataclass` field for proof strategy hints
- Add `verify()` method calling Lean subprocess

---

### ADR #13: Module Structure - src/logic/lean_bridge/

**Decision:** Create new subpackage `src/logic/lean_bridge/` for Lean bridge components, keeping Phase 1 solver/systems unchanged.

**Directory Structure:**

```
src/logic/lean_bridge/
├── __init__.py          # Public API exports
├── symbolic.py          # SymbolicMixin, SymbolicODESystem protocol
├── serialization.py     # ODESystemMetadata, JSON conversion
└── proof_request.py     # LeanProofRequest, factory functions
```

**Public API (`lean_bridge/__init__.py`):**

```python
from src.logic.lean_bridge.symbolic import SymbolicMixin, SymbolicODESystem
from src.logic.lean_bridge.serialization import ODESystemMetadata
from src.logic.lean_bridge.proof_request import (
    LeanProofRequest,
    create_structural_isomorphism_request
)

__all__ = [
    "SymbolicMixin",
    "SymbolicODESystem",
    "ODESystemMetadata",
    "LeanProofRequest",
    "create_structural_isomorphism_request",
]
```

**Alternatives Considered:**

1. **Add to existing src/logic/solver.py**
   - Pro: Fewer files
   - Con: Couples solver to Lean bridge (violates Single Responsibility)
   - Con: Module grows too large

2. **Create separate top-level package src/lean_bridge/**
   - Pro: Clear separation from logic
   - Con: Breaks existing src/logic/ organization
   - Con: Makes imports awkward

3. **Subpackage under src/logic/** [CHOSEN]
   - Pro: Isolated from solver/systems
   - Pro: Clean import structure (from src.logic.lean_bridge import ...)
   - Pro: Consistent with existing architecture (src/logic/plotting/, src/logic/systems/)

**Rationale:**
- **Isolation:** Lean bridge separate from numerical solver (can develop independently)
- **Minimal:** Each module has single responsibility
- **Importable:** Clean public API via `__init__.py`
- **Extensible:** Add subprocess_runner.py later without refactoring existing code
- **Testable:** Can test symbolic, serialization, proof_request modules independently

**Future Modules (Phase 2.5+):**
- `subprocess_runner.py` - Lean process management
- `exceptions.py` - Lean-specific error types (LeanTimeoutError, LeanVerificationError)
- `parsers.py` - Parse Lean output (proof/counterexample)

---

### ADR #14: Extending Systems - In-Place Mixin Inheritance

**Decision:** Extend existing `LorenzSystem` and `DampedPendulum` classes by adding `SymbolicMixin` to inheritance chain, rather than creating wrapper classes.

**Migration Pattern:**

**Before (Phase 1):**
```python
class LorenzSystem:
    def __init__(self, sigma=10.0, rho=28.0, beta=8/3):
        self.sigma = sigma
        self.rho = rho
        self.beta = beta

    def f(self, t, y):
        # Numerical implementation
        x_val, y_val, z_val = y
        dx_dt = self.sigma * (y_val - x_val)
        dy_dt = x_val * (self.rho - z_val) - y_val
        dz_dt = x_val * y_val - self.beta * z_val
        return np.array([dx_dt, dy_dt, dz_dt])
```

**After (Phase 2):**
```python
from src.logic.lean_bridge.symbolic import SymbolicMixin
import sympy as sp

class LorenzSystem(SymbolicMixin):
    _state_var_names = ['x', 'y', 'z']  # NEW: Class attribute

    def __init__(self, sigma=10.0, rho=28.0, beta=8/3):
        self.sigma = sigma
        self.rho = rho
        self.beta = beta

    def f(self, t, y):
        # Numerical implementation (UNCHANGED)
        x_val, y_val, z_val = y
        dx_dt = self.sigma * (y_val - x_val)
        dy_dt = x_val * (self.rho - z_val) - y_val
        dz_dt = x_val * y_val - self.beta * z_val
        return np.array([dx_dt, dy_dt, dz_dt])

    def _build_symbolic_equations(self) -> dict[str, sp.Expr]:
        """NEW: Generate symbolic equations."""
        x, y, z = sp.symbols('x y z')
        return {
            'x': self.sigma * (y - x),
            'y': x * (self.rho - z) - y,
            'z': x * y - self.beta * z
        }
```

**Alternatives Considered:**

1. **Wrapper classes** (create SerializableLorenzSystem)
   - Pro: Clean separation, no modification to existing classes
   - Con: Dual hierarchy, boilerplate, violates DRY
   - Con: Existing code must be updated to use wrappers

2. **Decorator pattern**
   - Pro: Flexible composition at runtime
   - Con: More complex, harder to type-check
   - Con: Overhead from delegation

3. **In-place mixin inheritance** [CHOSEN]
   - Pro: Single class definition (no wrappers)
   - Pro: Backward compatible (existing code unchanged)
   - Pro: DRY (no code duplication)
   - Con: Modifies existing classes

**Backward Compatibility Verification:**

```python
# All existing code continues working
lorenz = LorenzSystem(sigma=10.0, rho=28.0, beta=8/3)
assert lorenz.sigma == 10.0  # ✓ Parameter access
sol = solve_ode(lorenz, (0, 10), y0)  # ✓ Solver integration
assert sol.success  # ✓ No behavioral changes

# New symbolic capabilities available
equations = lorenz.get_symbolic_equations()  # ✓ New feature
assert 'x' in equations  # ✓ Returns dict of sympy expressions
```

**Rationale:**
- **Minimal disruption:** One line change (add mixin to inheritance)
- **Single source of truth:** No wrapper/wrapped dual classes
- **Composable:** Can add other mixins later (e.g., JacobianMixin, EquilibriaMixin)
- **Type-safe:** Mixin provides protocol interface

**Trade-offs Accepted:**
- **Modifies existing files:** Phase 1 systems lorenz.py and pendulum.py changed
- **Mitigation:** Changes minimal (inherit mixin, add one method), all Phase 1 tests must pass
- **Import dependency:** Systems now import from lean_bridge
- **Mitigation:** Lean_bridge has no dependencies on solver (clean separation)

**Testing Strategy:**
1. Run all Phase 1 tests → must pass unchanged
2. Add new tests for symbolic methods
3. Test JSON serialization independently
4. Integration test: solve_ode() → serialize → verify JSON

---

### ADR #15: JSON Bridge Architecture - Data Transport, Not Proof Generation

**Decision:** JSON serves as a **data serialization format** for communicating ODE system specifications to Lean. It does NOT generate or write Lean proofs. Lean proofs are **written once as parametric templates** in Lean code, and JSON provides the data these templates operate on.

**Critical Clarification:**

This ADR addresses a common architectural misconception: "JSON will generate/write Lean proofs automatically."

**Reality:** JSON is a **data pipe**, not a code generator.

---

#### What JSON DOES (Data Serialization)

**Python → JSON:** Serialize ODE system metadata

```python
# Python side
glucose_system = GlucoseMinimalModel(k1=0.026, k2=0.025, k3=0.025)

json_payload = {
    "system_type": "GlucoseMinimalModel",
    "state_dim": 2,
    "equations": ["dG/dt = k1*(Gb - G) - X*G", "dX/dt = k2*(I - Ib) - k3*X"],
    "parameters": {"k1": 0.026, "k2": 0.025, "k3": 0.025},
    "initial_condition": [92, 11],
    "time_interval": [0, 180]
}
```

**This is pure data** - no proof logic, no tactics, no theorems.

---

#### What Lean DOES (Apply Pre-Written Proofs)

**Lean side:** Parse JSON and apply **manually-written** proof templates

```lean
-- YOU WRITE THIS PROOF ONCE (manually, in Lean)
theorem glucose_satisfies_picard_lindelof
  (sys : GlucoseSystem)              -- Parsed from JSON
  (t₀ : ℝ) (x₀ : ℝ × ℝ)
  (tmin tmax : ℝ)
  (h_interval : tmin ≤ t₀ ∧ t₀ ≤ tmax)
  : ∃ (a r L K : ℝ≥0), IsPicardLindelof sys.rhs ⟨t₀, h_interval⟩ x₀ a r L K := by
  -- PROOF TACTICS (written once, work for any GlucoseSystem parameters)
  use compute_domain_radius sys, 0, compute_lipschitz_bound sys, compute_norm_bound sys
  constructor
  case lipschitzOnWith =>
    intro t ht
    apply lipschitz_of_polynomial_rhs
    -- Proof that polynomial RHS is Lipschitz
  case continuousOn =>
    intro x hx
    apply continuous_polynomial
    -- Proof that polynomial is continuous
  case norm_le =>
    intro t ht x hx
    apply norm_bound_on_closed_ball
    -- Proof that norm is bounded
  case mul_max_le =>
    simp [compute_consistency_inequality]
    -- Proof of L * Δt ≤ a - r
```

**Key insight:** This proof is **parametric** - works for any `GlucoseSystem` with any parameter values. JSON just provides the specific `k1`, `k2`, `k3` values.

---

#### What CAN'T Be Automated (Proof Construction)

**You CANNOT "generate Lean proofs from JSON"** because:

1. **Proofs require mathematical reasoning**
   - Each theorem type needs custom proof strategy
   - Tactics depend on mathematical structure (polynomial, Lipschitz, continuous)
   - No algorithm auto-discovers proof strategies

2. **Lean is a proof assistant, not an automated theorem prover**
   - You guide Lean through the proof steps
   - Lean verifies each step is valid
   - Lean doesn't "figure out" the proof for you

3. **Different systems need different proof templates**
   - Polynomial systems use `ring`, `continuity` tactics
   - Systems with singularities need different approach
   - Each system class needs human-written proof template

---

#### The Complete Workflow

**Phase 1: Python Numerical Discovery**

```python
# "These two systems look similar numerically"
similarity = compare_trajectories(glucose_system, pid_system)
if similarity > threshold:
    print("Candidate analogy detected!")
```

**Phase 2B: Python Serializes to JSON**

```python
# Send system data to Lean
request = LeanProofRequest(
    system=ODESystemMetadata.from_ode_system(glucose_system),
    proof_type="picard_lindelof",
    initial_condition=[92, 11],
    time_interval=[0, 180]
)

json_data = request.to_lean_json()  # Pure data, no proofs
```

**Phase 3: Lean Parses JSON + Applies Proof Template**

```lean
-- Parse JSON into Lean structures
def verify_from_json (json_str : String) : IO ProofResult := do
  let sys_data ← parse_ode_system_json json_str
  let sys := construct_glucose_system sys_data.parameters

  -- Apply pre-written proof template
  match prove_picard_lindelof sys sys_data.t0 sys_data.x0 with
  | some proof => return ⟨"success", some proof⟩
  | none => return ⟨"failed", none⟩
```

**Phase 4: Lean Returns JSON Result**

```json
{
  "proof_status": "success",
  "theorem": "glucose_satisfies_picard_lindelof",
  "constants_found": {"a": 10.5, "r": 0.0, "L": 15.2, "K": 1.0},
  "verification_time_ms": 342
}
```

**Or if proof fails:**

```json
{
  "proof_status": "failed",
  "error": "Lipschitz condition violated: RHS unbounded at x=0",
  "failed_field": "norm_le",
  "hint": "System may have singularity - check domain bounds"
}
```

---

#### What IS Automated vs Manual

| Component | Automated | Manual |
|-----------|-----------|--------|
| **Python → JSON serialization** | ✅ Yes | Configure schema once |
| **JSON → Lean parsing** | ✅ Yes | Write parser once |
| **Proof template application** | ✅ Yes | Write proof once per theorem type |
| **Proof tactic selection** | ❌ No | Human designs proof strategy |
| **Theorem statement writing** | ❌ No | Human formalizes mathematics |
| **Mathlib lemma discovery** | ❌ No | Human finds relevant theorems |

---

#### Analogy: Compiler vs Code Generator

**This architecture is like:**

**Compiler model** (what we're building):
- You write C code (parametric Lean proofs)
- Compiler applies it to different inputs (JSON data)
- Same compiled code works for many inputs

**NOT a code generator** (what we're NOT building):
- Automatically generates C code from requirements
- AI writes the program for you
- No human programming needed

**Similarly:**
- You write Lean proofs (parametric templates)
- JSON provides data to instantiate templates
- Same proof works for many parameter values

**We're NOT building:**
- Automatic proof generator from JSON
- AI that writes Lean proofs
- No human proving needed

---

#### Learning Path Connection (Phase 3A/3B)

**Why you're learning Lean deeply:**

1. **Write proof templates** (Phase 3)
   - `theorem decay_satisfies_picard_lindelof` (you wrote this)
   - `theorem lorenz_satisfies_picard_lindelof` (Phase 3B)
   - `theorem glucose_satisfies_picard_lindelof` (Phase 3C)

2. **Understand what Lean needs** (informs Phase 2B JSON schema)
   - What fields? (equations, parameters, domain)
   - What format? (symbolic strings, numeric values)
   - What constraints? (parameter bounds, time intervals)

3. **Know what's feasible** (realistic Phase 3 scope)
   - Well-definedness proofs: ✅ Feasible (Picard-Lindelöf)
   - Existence proofs: ✅ Feasible (apply Mathlib theorems)
   - Structural isomorphism: ⚠️ Hard (research-level)
   - Full stability analysis: ⚠️ Very hard (may need custom lemmas)

---

#### Alternatives Considered

**Alternative 1: Automated Theorem Proving (ATP)**

Use automated provers (Z3, Vampire, E) instead of Lean:
- Pro: Can find proofs automatically for some theorems
- Con: Limited to decidable fragments (first-order logic, SMT)
- Con: Can't handle analysis (reals, derivatives, ODEs)
- Con: No parametric proofs (re-prove for each parameter set)
- **Decision:** Not suitable for ODE verification

**Alternative 2: Proof Synthesis**

Generate Lean tactics from specifications:
- Pro: Less manual proof writing
- Con: No general synthesis algorithm exists
- Con: Research problem (active area of ML4TP)
- Con: Would require training data we don't have
- **Decision:** Beyond project scope

**Alternative 3: Interactive Proof Development** [CHOSEN]

Write Lean proofs manually, parameterize over system data:
- Pro: Works for complex analysis theorems
- Pro: Proofs reusable across parameter values
- Pro: Lean's ecosystem (Mathlib) provides lemmas
- Con: Requires learning Lean (Phase 3A/3B)
- Con: Each theorem type needs manual proof
- **Decision:** Only feasible approach for ODE verification

---

#### Rationale for This Architecture

**Why parametric proofs work:**

1. **Mathematical structure is reusable**
   - All polynomial ODEs are Lipschitz (same proof strategy)
   - All bounded continuous functions satisfy Picard-Lindelöf (same tactic)
   - Write proof once, works for entire system class

2. **Parameters are data, not logic**
   - `σ = 10` vs `σ = 15` doesn't change proof structure
   - Only changes numerical bounds in computation
   - JSON provides numbers, Lean applies reasoning

3. **Verification ≠ Proof discovery**
   - Lean **verifies** your proof is correct
   - You **construct** the proof using tactics
   - JSON **provides data**, not proof strategies

---

#### Impact on Phase 2B Design

**JSON schema must include:**

1. **System specification** (equations, parameters)
   - Lean parses into system structure
   - Used to instantiate parametric proofs

2. **Proof request metadata** (initial condition, time interval, domain)
   - Lean uses to compute bounds (a, r, L, K)
   - Not part of proof logic, just numerical inputs

3. **Verification configuration** (timeout, memory limits)
   - Controls Lean subprocess execution
   - Not related to mathematical content

**JSON schema does NOT include:**
- ❌ Proof tactics or strategies
- ❌ Lean code fragments
- ❌ Theorem statements
- ❌ Mathlib lemma names

---

#### Trade-offs Accepted

**Manual proof writing:**
- Con: Requires Lean expertise (Phase 3A learning investment)
- Con: Each system class needs proof template
- Pro: Proofs are verified, not heuristic
- Pro: Templates reusable across instances
- Pro: Correct by construction

**Parametric proof limitation:**
- Con: Can't handle arbitrary systems (only predefined classes)
- Con: Novel system types need new proof templates
- Pro: Common system classes well-supported (polynomial, smooth)
- Pro: Extensible (add new templates incrementally)

**No automated synthesis:**
- Con: Can't automatically verify arbitrary conjectures
- Con: Human bottleneck in proof development
- Pro: Realistic scope for PhD-level project
- Pro: Demonstrates understanding of formal methods
- Pro: Portfolio showcases manual theorem proving skill

---

#### Future Work (Beyond Current Scope)

**Potential enhancements:**

1. **Proof tactic library**
   - Common lemmas for ODE classes (polynomial_lipschitz, exponential_bounded)
   - Reusable sub-proofs as Lean functions
   - Reduces proof length, increases reusability

2. **Metaprogramming for boilerplate**
   - Lean macros to generate structure field proofs
   - Automate repetitive parts (not core logic)
   - Still requires human-designed proof strategy

3. **Proof repair on parameter changes**
   - If proof fails, suggest bound adjustments
   - "Increase domain radius to 15.0" (heuristic, not synthesis)
   - Helps debugging, doesn't write proofs

**None of these "generate proofs from JSON"** - they assist human proof development.

---

**Summary:** JSON is a data pipe between Python (numerical discovery) and Lean (formal verification). Proofs are manually written once as parametric templates in Lean, then reused across different parameter values provided via JSON. This architecture is realistic, feasible, and demonstrates deep understanding of both numerical methods and formal verification.

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

---

### ADR #16: Lean 4 Proof Methodology - Fixed Interval First

**Date:** 2026-01-20  
**Status:** Accepted  
**Context:** Phase 3A - First complete Picard-Lindelöf proof in Lean 4

**Decision:** Prove Picard-Lindelöf for decay equation on **fixed interval** `[-0.1, 0.1]` before attempting parametric generalization.

**Problem:**
- Need to prove existence/uniqueness for decay ODE: `dx/dt = -x`
- Picard-Lindelöf requires 4 conditions with parameters `a, r, L, K`
- Parameters must satisfy consistency: `L * max(tmax-t0, t0-tmin) ≤ a - r`
- Initial attempt with `[-1, 1]` interval **failed** consistency check

**Alternatives Considered:**

1. **Parametric proof directly** (write general theorem for any interval)
   - Pro: Most general, needed for JSON bridge ultimately
   - Con: Complex, requires parameter formulas, harder to debug
   - Con: Learning curve steep for first Lean proof

2. **Fixed interval approach** (prove for specific `[-0.1, 0.1]` first)
   - Pro: Concrete values simplify debugging
   - Pro: Validates proof structure before generalization
   - Pro: Can test all 4 tactic patterns independently
   - Con: Need second proof for parametric version

3. **Very small interval** (e.g., `[-0.01, 0.01]`)
   - Pro: Even easier to satisfy constraints
   - Con: Too restrictive, doesn't validate realistic use case

**Choice:** Alternative 2 (Fixed interval)

**Rationale:**
- First complete Lean proof from scratch - learning priority
- Concrete values make parameter constraints transparent
- Discovered consistency issue early (interval size matters!)
- Proof tactics transferable to parametric version
- Can extend to general theorem after validation

**Trade-offs:**
- Extra work to generalize later (acceptable for learning)
- Fixed interval less useful for JSON bridge (temporary limitation)

**Implementation Details:**

```lean
-- Helper: proof that 0 ∈ [-0.1, 0.1]
def t0_in_interval : (0 : Real) ∈ Set.Icc (-0.1) 0.1 := by norm_num

theorem decay_picard_specific :
    ∃ (a r L K : NNReal),
    IsPicardLindelof decay_rhs ⟨0, t0_in_interval⟩ 5 a r L K := by
  use 1, 0, 6, 1  -- Concrete values
  constructor
  case lipschitzOnWith => simp [decay_rhs]
  case continuousOn => intro x hx; simp [decay_rhs]; exact continuousOn_const
  case norm_le => ...  -- Triangle inequality calc chain
  case mul_max_le => simp; norm_num
```

**Parameters Chosen:**
- `a = 1`: State ball radius (x ∈ [4, 6])
- `r = 0`: Single IC, no neighborhood  
- `L = 6`: Norm bound (max |-x| = 6 on [4,6])
- `K = 1`: Lipschitz constant (slope of -x)

**Consistency Check:**
```
6 * max(0.1 - 0, 0 - (-0.1)) ≤ 1 - 0
6 * 0.1 ≤ 1
0.6 ≤ 1  ✅
```

**Lessons Learned:**
1. Picard-Lindelöf parameters tightly coupled (not independent)
2. Smaller intervals easier to satisfy (local vs global guarantees)
3. Concrete examples clarify abstract constraints
4. Fixed-case proof is scaffold for parametric generalization

**Next Phase:**
- Generalize to `decay_picard` (arbitrary t0, x0, interval)
- Compute `a, r, L` from interval size and IC
- This enables JSON bridge (Python provides t0, x0, interval)

**Status:** Phase 3A complete (Day 8) - ready for parametric generalization

---

