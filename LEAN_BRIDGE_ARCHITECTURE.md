# Python-Lean Bridge Architecture

> **Purpose:** Technical reference for the long-term goal of connecting Python ODE solver to Lean 4 formal verification.
>
> **Context:** This document explains how the glucose-insulin minimal models will eventually connect to Lean for proving mathematical equivalences between biological and control systems.
>
> **Status:** Phase 1 (Python foundation) in progress. This is a forward-looking architectural design document.

---

## Table of Contents

1. [The Big Picture](#the-big-picture)
2. [Three-Phase Architecture](#three-phase-architecture)
3. [How Python Connects to Lean](#how-python-connects-to-lean)
4. [The Glucose-Insulin Example](#the-glucose-insulin-example)
5. [Technical Challenges](#technical-challenges)
6. [Lean 4 Ecosystem](#lean-4-ecosystem)
7. [Project Timeline](#project-timeline)
8. [Key Insight](#key-insight)

---

## The Big Picture

### What You're Building

This project creates a **computational proof assistant** that:

1. **Discovers** numerical similarities between biological and control systems (Python)
2. **Conjectures** structural analogies based on those similarities (Python heuristics)
3. **Proves** those analogies are mathematically rigorous (Lean 4)

### The Central Goal

**Formally prove** that biological regulation systems (like glucose-insulin homeostasis) are **mathematically equivalent** to classical control systems (like PID controllers).

This bridges:
- **Systems Biology** (glucose-insulin kinetics)
- **Control Theory** (PID controllers, state-space models)
- **Formal Methods** (Lean 4 theorem proving)

---

## Three-Phase Architecture

### Phase 1: Python Numerical Foundation (Current)

**What you're building now:**

```python
# Python side: Numerical computation
glucose_system = GlucoseMinimalModel(k1=0.026, k2=0.025, k3=0.025)
pid_controller = PIDControllerSystem(Kp=1.0, Ki=0.1, Kd=0.01)

# Solve both systems numerically
glucose_trajectory = solve_ode(glucose_system, (0, 180), y0_glucose)
pid_trajectory = solve_ode(pid_controller, (0, 180), y0_pid)

# Compute similarity metrics
structural_similarity = compare_phase_portraits(glucose_trajectory, pid_trajectory)
stability_similarity = compare_lyapunov_exponents(glucose_system, pid_controller)
```

**Output:** "Hey, these two systems behave similarly! They might be mathematically related."

**Status:** Steps 1-16 of current plan.

---

### Phase 2: Python-Lean Bridge (JSON Communication)

**Subprocess interface for communication:**

```python
# src/logic/lean_bridge.py

class LeanProofRequest:
    """Package a conjecture for Lean to prove."""

    def __init__(self, system1: ODESystem, system2: ODESystem, conjecture_type: str):
        self.system1 = system1
        self.system2 = system2
        self.conjecture_type = conjecture_type  # "structural_isomorphism", "stability_equivalence", etc.

    def to_lean_json(self) -> dict:
        """Convert to Lean-compatible JSON."""
        return {
            "system1": {
                "odes": self._extract_symbolic_equations(self.system1),
                "parameters": self.system1.parameters,
                "state_dim": 3
            },
            "system2": {
                "odes": self._extract_symbolic_equations(self.system2),
                "parameters": self.system2.parameters,
                "state_dim": 3
            },
            "conjecture": {
                "type": self.conjecture_type,
                "hypothesis": "There exists a diffeomorphism φ: ℝ³ → ℝ³ such that..."
            }
        }

# Usage:
conjecture = LeanProofRequest(glucose_system, pid_controller, "structural_isomorphism")
lean_result = lean_subprocess.verify(conjecture.to_lean_json())
```

**Key Components:**

1. **JSON Schema** for goal-state passing
2. **Subprocess runner** with timeout/memory limits
3. **Exception mapping** for Lean errors
4. **Symbolic extraction** (sympy → Lean)

**Status:** Future work (Weeks 3-5).

---

### Phase 3: Lean Formal Verification

**On the Lean side:**

```lean
-- lean/ForgeLogic.lean

import Mathlib.Analysis.ODE.Basic
import Mathlib.Topology.MetricSpace.Basic

namespace MinimalModels

-- Define the glucose minimal model as a formal system
structure GlucoseMinimalModel where
  k1 : ℝ
  k2 : ℝ
  k3 : ℝ
  Gb : ℝ
  Ib : ℝ
  k1_pos : 0 < k1
  k2_pos : 0 < k2
  k3_pos : 0 < k3

def glucose_ode (sys : GlucoseMinimalModel) (t : ℝ) (state : ℝ × ℝ) : ℝ × ℝ :=
  let (G, X) := state
  let dG := sys.k1 * (sys.Gb - G) - X * G
  let dX := sys.k2 * (I t - sys.Ib) - sys.k3 * X  -- I(t) is insulin input
  (dG, dX)

-- Define a control system (e.g., PID controller)
structure PIDController where
  Kp : ℝ
  Ki : ℝ
  Kd : ℝ

def pid_ode (sys : PIDController) (t : ℝ) (state : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  -- ... PID controller ODEs
  sorry

-- The big theorem: structural isomorphism between glucose regulation and PID control
theorem glucose_pid_isomorphism
  (glucose : GlucoseMinimalModel)
  (pid : PIDController)
  (h_params : glucose.k1 / glucose.k3 = pid.Kp)  -- parameter correspondence
  : ∃ φ : (ℝ × ℝ) → (ℝ × ℝ × ℝ),  -- diffeomorphism
      Bijective φ ∧
      (∀ t state, φ (glucose_ode glucose t state) = pid_ode pid t (φ state)) :=
by
  -- Lean will either prove this or fail
  sorry  -- You fill this in!

end MinimalModels
```

**Status:** Future work (Weeks 6-10).

---

## How Python Connects to Lean

### The Complete Workflow

#### Step 1: Python Numerical Discovery

```python
# Scan through parameter space
for glucose_params in parameter_space:
    glucose_sys = GlucoseMinimalModel(**glucose_params)

    for pid_params in control_parameter_space:
        pid_sys = PIDController(**pid_params)

        # Numerical similarity check
        if systems_appear_similar(glucose_sys, pid_sys):
            print(f"Found candidate analogy!")
            print(f"  Glucose k1={glucose_params['k1']}, k3={glucose_params['k3']}")
            print(f"  PID Kp={pid_params['Kp']}")
            print(f"  Ratio k1/k3 = {glucose_params['k1']/glucose_params['k3']}")
            print(f"  PID Kp = {pid_params['Kp']}")

            # Send to Lean for formal verification
            conjecture = ConjectureBuilder.structural_isomorphism(
                glucose_sys, pid_sys,
                parameter_map={"k1/k3": "Kp"}
            )

            lean_result = lean_bridge.verify_conjecture(conjecture)

            if lean_result.proven:
                print("✓ PROVEN! This is a genuine mathematical equivalence!")
            else:
                print("✗ Conjecture failed. Not a true isomorphism.")
```

#### Step 2: Lean Verification

Lean kernel receives:

```json
{
  "system1": {
    "name": "GlucoseMinimalModel",
    "odes": ["dG/dt = k1*(Gb - G) - X*G", "dX/dt = k2*(I - Ib) - k3*X"],
    "parameters": {"k1": 0.026, "k2": 0.025, "k3": 0.025, "Gb": 92, "Ib": 11}
  },
  "system2": {
    "name": "PIDController",
    "odes": ["de/dt = r - y", "du/dt = Kp*e + Ki*integral_e + Kd*de/dt"],
    "parameters": {"Kp": 1.04, "Ki": 0.1, "Kd": 0.01}
  },
  "conjecture": {
    "type": "structural_isomorphism",
    "parameter_correspondence": {"k1/k3": "Kp"},
    "coordinate_transformation": "φ(G, X) = (G - Gb, X, ∫X dt)"
  }
}
```

Lean attempts to prove:

1. **Existence of diffeomorphism φ:** Is there a smooth, invertible coordinate transformation?
2. **Commutativity:** Does φ preserve the dynamics? (φ ∘ f₁ = f₂ ∘ φ)
3. **Parameter correspondence:** Do k1/k3 and Kp play analogous mathematical roles?

---

## Why This Architecture is Powerful

### Bridging Numerical and Symbolic Worlds

| Python (Numerical) | Lean (Symbolic) |
|-------------------|-----------------|
| `solve_ivp()` gives you trajectories | Proves theorems about **all** trajectories |
| `np.array([279.0, 0.0])` | `state : ℝ × ℝ` |
| Floating-point approximations | Exact real numbers |
| "These look similar" | "These are provably equivalent" |
| Find patterns in data | Prove universal mathematical truths |

### The Division of Labor

**Python's job:**
- Fast numerical experimentation
- Parameter estimation from real data
- Pattern recognition across systems
- Generate plausible conjectures

**Lean's job:**
- Rigorous mathematical proof
- Guarantee correctness for all cases
- Catch false patterns Python might miss
- Provide certified results

---

## The Glucose-Insulin Example

### From Van Riel Paper

The glucose minimal model (equations 9-10):

```
dG/dt = k₁(Gb - G) - X·G
dX/dt = k₂(I - Ib) - k₃·X
```

Where:
- **G(t):** Plasma glucose concentration [mg/dL]
- **X(t):** Interstitial insulin activity [1/min]
- **I(t):** Plasma insulin level [µU/mL] (input)
- **k₁ = SG:** Glucose effectiveness
- **k₂, k₃:** Insulin kinetics parameters
- **SI = k₂/k₃:** Insulin sensitivity

### The Control Theory Analogy

This is structurally similar to a **feedback control system**:

```
de/dt = r - y           (error dynamics)
du/dt = Kp·e + Ki·∫e    (controller output)
```

Where:
- **Glucose effectiveness (SG = k₁):** Feed-forward term (open-loop control)
- **Insulin sensitivity (SI = k₂/k₃):** Feedback gain (closed-loop control)
- **Pancreatic responsivity (φ₁, φ₂):** Controller response characteristics

### What You'll Prove

**Conjecture:** Under coordinate transformation φ: (G, X) → (e, u, ∫u), the glucose minimal model is **structurally isomorphic** to a PID controller when:

```
k₁/k₃ = Kp  (proportional gain)
k₂ = Ki     (integral gain)
```

**Python discovers this numerically:**
```python
glucose_settling_time ≈ pid_settling_time
glucose_overshoot ≈ pid_overshoot
glucose_stability_margin ≈ pid_stability_margin
```

**Lean proves it formally:**
```lean
theorem glucose_is_pid_controller : ...
```

---

## Technical Challenges

### Challenge 1: Symbolic Equation Extraction

**Problem:** Your Python ODE systems are **numerical functions**, not symbolic expressions.

```python
# This is numerical:
def f(self, t: float, y: NDArray) -> NDArray:
    return np.array([self.k1 * (self.Gb - y[0]) - y[1] * y[0],
                     self.k2 * (I_func(t) - self.Ib) - self.k3 * y[1]])

# Lean needs symbolic:
"dG/dt = k1*(Gb - G) - X*G"
```

**Solution:** Use `sympy` to maintain symbolic representations:

```python
import sympy as sp

class GlucoseMinimalModel:
    def __init__(self, k1, k2, k3, Gb, Ib):
        # Numerical parameters (for scipy)
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3

        # Symbolic equations (for Lean export)
        G, X, t = sp.symbols('G X t')
        I = sp.Function('I')(t)
        self.symbolic_odes = [
            sp.Eq(sp.Derivative(G, t), k1 * (Gb - G) - X * G),
            sp.Eq(sp.Derivative(X, t), k2 * (I - Ib) - k3 * X)
        ]

    def f(self, t, y):
        # Numerical implementation for scipy
        return np.array([...])

    def to_lean_string(self) -> str:
        """Convert sympy → Lean syntax."""
        return "dG/dt = k1 * (Gb - G) - X * G"
```

**Trade-off:** Maintaining both numerical and symbolic versions adds complexity, but enables the bridge.

---

### Challenge 2: Lean Type Conversion

**Problem:** Python `float` ≠ Lean `ℝ` (real numbers).

Python floats are **finite-precision approximations**:
```python
0.1 + 0.2  # 0.30000000000000004 (not exactly 0.3!)
```

Lean reals are **mathematically exact**:
```lean
(0.1 : ℝ) + (0.2 : ℝ) = (0.3 : ℝ)  -- Provably true
```

**Solution:**

1. **Use rational numbers** for parameters when possible:
```python
k1 = Fraction(26, 1000)  # Exact: 26/1000 instead of 0.026
```

2. **Add tolerance bounds** for theorems:
```lean
theorem glucose_stability
  (glucose : GlucoseMinimalModel)
  (h_k1 : 0.01 < glucose.k1 ∧ glucose.k1 < 0.05)  -- bounds instead of exact value
  : is_stable glucose_ode :=
```

3. **Prove for parameter classes**, not specific values:
```lean
-- Prove for all insulin sensitivities in normal range
theorem normal_glucose_regulation
  (SI : ℝ)
  (h_SI_normal : 2.1e-4 < SI ∧ SI < 18.2e-4)  -- From Van Riel paper
  : converges_to_basal glucose_ode :=
```

---

### Challenge 3: The "Gap" Problem

**The ε-δ Gap between Numerical and Formal Proof:**

**Python says:** "Numerically, these systems reach equilibrium at the same rate (within 1% error)."

**Lean asks:** "Prove it for **ALL** initial conditions and **ALL** parameter values in the specified range, with **zero** error."

**Your approach:**

1. **Python finds numerical evidence** (parameter estimation, trajectory comparison)
2. **Python generates a conjecture** with specific parameter ranges and error bounds
3. **Lean attempts formal proof** using Mathlib's ODE theory
4. **If Lean succeeds** → **Certified result** (publishable theorem!)
5. **If Lean fails** → Either:
   - Refine the conjecture (tighten bounds, add constraints)
   - Discover it was a false pattern (Python was fooled by numerical coincidence)

**This is the scientific method for mathematics!**

---

### Challenge 4: Handling Time-Dependent Inputs

**Problem:** Glucose model has time-dependent insulin input I(t) from interpolated data.

```python
# Python: interpolated insulin signal
I_func = interp1d(time_samples, insulin_measurements)
```

**Lean needs a formal representation:**

```lean
-- Option 1: Assume I is continuous
variable (I : ℝ → ℝ) (h_I_cont : Continuous I)

-- Option 2: Piecewise linear (matches Python's interp1d)
def I_piecewise (data : List (ℝ × ℝ)) : ℝ → ℝ := ...

-- Option 3: Abstract as "any bounded continuous input"
variable (I : ℝ → ℝ) (h_I_bounded : ∀ t, |I t| ≤ M)
```

**Solution:** Prove theorems that work for **classes of inputs**, not specific data.

---

## Lean 4 Ecosystem

### Mathlib4 Components You'll Use

```lean
import Mathlib.Analysis.ODE.Gronwall        -- ODE existence/uniqueness theorems
import Mathlib.Analysis.ODE.PicardLindelof  -- Solution theory
import Mathlib.Topology.MetricSpace.Basic   -- Phase space topology
import Mathlib.Analysis.Calculus.Deriv      -- Derivatives and differentiability
import Mathlib.Geometry.Manifold.Diffeomorph -- Coordinate transformations
import Mathlib.Data.Real.Basic              -- Real number properties
import Mathlib.Analysis.SpecialFunctions.Exp -- Exponentials (for stability)
import Mathlib.Tactic.Ring                  -- Algebraic simplification
```

### What Lean Can Prove

✅ **Stability:** "This equilibrium point is asymptotically stable"
```lean
theorem glucose_basal_stable : asymptotically_stable (Gb, 0) glucose_ode
```

✅ **Existence/Uniqueness:** "Solutions exist and are unique for all initial conditions"
```lean
theorem glucose_solution_exists : ∀ y0, ∃! sol, is_solution glucose_ode y0 sol
```

✅ **Structural Equivalence:** "These two systems have the same qualitative dynamics"
```lean
theorem glucose_pid_equivalent : topologically_conjugate glucose_ode pid_ode
```

✅ **Parameter Relationships:** "When k1/k3 = Kp, these systems are isomorphic"
```lean
theorem parameter_correspondence (h : k1 / k3 = Kp) : isomorphic_systems ...
```

✅ **Conservation Laws:** "This quantity is conserved along trajectories"
```lean
theorem energy_conserved : ∀ t, energy (sol t) = energy (sol 0)
```

✅ **Boundedness:** "Glucose never goes negative or infinite"
```lean
theorem glucose_bounded : ∀ t, 0 ≤ G t ∧ G t ≤ G_max
```

### What Lean Cannot Easily Do

❌ **Numerical computation** (Python's job)
❌ **Parameter fitting to data** (Python's job)
❌ **Plotting trajectories** (Python's job)
❌ **Stochastic ODEs** (Mathlib support is limited)

---

## Visualization Architecture

### Design Decision: Strategy Pattern for Extensible Plotting

**Context:**
Phase 1 requires visualization of ODE trajectories for validation. Initial needs are 2D (pendulum) and 3D (Lorenz) phase portraits, but future phases require bifurcation diagrams, Poincaré sections, and higher-dimensional projections.

**Architecture Choice:**
Implemented Strategy + Factory pattern with abstract base class instead of simple conditional logic.

**Structure:**
```
src/logic/plotting/
├── __init__.py          # Public API: plot_phase_portrait()
├── base.py              # PhasePortraitPlotter ABC (abstract interface)
├── plotters.py          # TwoDimensionalPlotter, ThreeDimensionalPlotter
├── factory.py           # PlotterFactory (registry-based creation)
└── config.py            # PlotConfig dataclass (styling configuration)
```

**Key Components:**

1. **Abstract Base Class** (`base.py`):
```python
from abc import ABC, abstractmethod

class PhasePortraitPlotter(ABC):
    @abstractmethod
    def plot(self, t: NDArray, y: NDArray, **kwargs) -> plt.Figure:
        """Render phase portrait for specific dimensionality."""
```

2. **Concrete Strategies** (`plotters.py`):
- `TwoDimensionalPlotter` - For systems like damped pendulum
- `ThreeDimensionalPlotter` - For systems like Lorenz attractor
- Future: `BifurcationPlotter`, `PoincareSectionPlotter`, `HighDimensionalProjectionPlotter`

3. **Factory Registry** (`factory.py`):
```python
class PlotterFactory:
    _registry = {
        2: TwoDimensionalPlotter,
        3: ThreeDimensionalPlotter,
    }

    @classmethod
    def create(cls, n_dim: int) -> PhasePortraitPlotter:
        """Select plotter based on state dimensionality."""
```

4. **Public API** (`__init__.py`):
```python
def plot_phase_portrait(t, y, config=None, save_path=None):
    """Generic plotting function - automatically selects appropriate plotter."""
    plotter = PlotterFactory.create(y.shape[0])
    return plotter.plot(t, y, config=config, save_path=save_path)
```

**Integration with Solver:**
```python
def solve_ode(system, t_span, y0, method="RK45", plot=False, save_path=None):
    sol = scipy.integrate.solve_ivp(...)

    if plot:
        from src.logic.plotting import plot_phase_portrait
        plot_phase_portrait(sol.t, sol.y, save_path=save_path)

    return sol
```

**Benefits:**
- **Open/Closed Principle:** Add new visualization types without modifying existing code
- **Extensibility:** Register new plotters (bifurcation, Poincaré) by implementing interface
- **Maintainability:** Each plotter has single responsibility
- **Testability:** Mock plotters in unit tests

**Trade-offs:**
- More upfront complexity (5 files vs 1)
- Steeper learning curve
- Justified by: Planned bifurcation work, learning OOP, production-grade infrastructure

---

## Project Timeline

### Phase 1: ODE Solver (Current) — Weeks 1-2

**Deliverables:**
- [x] Exception handling (`exceptions.py`)
- [x] Logging (`logger.py`)
- [x] Protocol definition (`protocols.py`)
- [x] NumPy/SciPy/Matplotlib dependencies
- [x] Generic ODE solver (`solver.py`)
- [x] Lorenz and Pendulum test systems
- [x] Visualization architecture (Strategy pattern)
- [ ] Plotting implementation (base, plotters, factory)
- [ ] Unit tests with 80%+ coverage
- [ ] Glucose-insulin minimal models
- [ ] Parameter estimation (`scipy.optimize.least_squares`)

**Milestone:** Can fit glucose minimal model to FSIGT data from Van Riel paper.

---

### Phase 2: Python-Lean Bridge — Weeks 3-5

**Deliverables:**
- [ ] JSON schema for goal-state passing
- [ ] Lean subprocess runner with timeout/memory limits
- [ ] Exception mapping for Lean errors (tactic timeout, kernel panic, etc.)
- [ ] Symbolic equation extraction using `sympy`
- [ ] `LeanProofRequest` class
- [ ] `LeanProofResult` parser
- [ ] Integration tests (Python ↔ Lean communication)

**Milestone:** Python can send a simple ODE system to Lean and receive verification result.

---

### Phase 3: Lean Formalization — Weeks 6-10

**Deliverables:**
- [ ] Formalize `GlucoseMinimalModel` structure in Lean
- [ ] Formalize `PIDController` structure in Lean
- [ ] Prove basic properties (existence, uniqueness, boundedness)
- [ ] Define `structurally_isomorphic` predicate
- [ ] Prove simple isomorphism: exponential decay ↔ first-order system
- [ ] **Big Theorem:** Prove `glucose_pid_isomorphism`

**Milestone:** First formal proof of biological-control equivalence.

---

### Phase 4: Automated Discovery — Weeks 11-15

**Deliverables:**
- [ ] Heuristics for detecting structural similarities
- [ ] Parameter space search algorithms
- [ ] Automated conjecture generation
- [ ] Mathlib namespace traversal (find relevant existing theorems)
- [ ] Multiple system comparisons (glucose vs. multiple controllers)
- [ ] Statistical analysis of proof success rates

**Milestone:** System automatically discovers and proves new analogies.

---

## Key Insight

### Why This Project Matters

The glucose-insulin model **IS ALREADY** a control system!

**From Van Riel paper:**
- **Glucose effectiveness (SG):** Feed-forward term (open-loop control)
- **Insulin sensitivity (SI):** Feedback gain (closed-loop control)
- **Pancreatic responsivity (φ₁, φ₂):** Controller response characteristics

**But biologists and control engineers don't talk to each other.**

Your project will **formally prove** what interdisciplinary researchers intuitively suspect:

> **Biological regulation IS control theory, and control theory IS biological regulation.**

They are the **same mathematical structure** expressed in different notation.

### Broader Impact

Once you prove glucose-insulin ≅ PID controller:

1. **Medical Applications:**
   - Design better artificial pancreas algorithms
   - Transfer insights from decades of control theory to diabetes treatment
   - Formally verify safety of closed-loop insulin delivery

2. **Systems Biology:**
   - Use control theory tools to analyze other regulatory networks
   - Gene regulation, hormone cascades, immune response, etc.
   - Discover universal principles across biology

3. **Control Theory:**
   - Learn from evolution's 500-million-year optimization process
   - Biologically-inspired robust controllers
   - Adaptive control strategies from living systems

4. **Formal Methods:**
   - Demonstrate Lean 4 for hybrid systems verification
   - Bridge numerical simulation and formal proof
   - Portfolio-worthy demonstration of advanced software engineering

---

## Summary

### The Architecture in One Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         PHASE 1: Python                          │
│                                                                   │
│  ┌────────────┐         ┌──────────────┐      ┌──────────────┐ │
│  │  Glucose   │────────▶│ solve_ode()  │─────▶│ Trajectories │ │
│  │   Model    │         │  (scipy)     │      │   & Data     │ │
│  └────────────┘         └──────────────┘      └──────────────┘ │
│         │                                              │         │
│         │                                              ▼         │
│         │                                      ┌──────────────┐ │
│         │                                      │  Similarity  │ │
│         │                                      │   Metrics    │ │
│         │                                      └──────────────┘ │
│         │                                              │         │
│         ▼                                              ▼         │
│  ┌────────────┐                              ┌──────────────┐   │
│  │    PID     │                              │  Conjecture  │   │
│  │ Controller │◀─────────────────────────────│  Generator   │   │
│  └────────────┘                              └──────────────┘   │
│                                                       │          │
└───────────────────────────────────────────────────────┼──────────┘
                                                        │
                                              JSON      │
                                                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 2: Bridge Layer                         │
│                                                                   │
│   Python float → Lean ℝ                                          │
│   NumPy arrays → Lean vectors                                    │
│   Numerical functions → Symbolic ODEs (sympy)                    │
│   Trajectories → ∀ initial conditions                            │
│                                                                   │
│   ┌──────────────────────────────────────────────────────┐      │
│   │ {                                                    │      │
│   │   "system1": "dG/dt = k1*(Gb-G) - X*G",            │      │
│   │   "system2": "de/dt = Kp*e + Ki*∫e",               │      │
│   │   "conjecture": "structural_isomorphism"           │      │
│   │ }                                                    │      │
│   └──────────────────────────────────────────────────────┘      │
│                                                        │         │
└────────────────────────────────────────────────────────┼─────────┘
                                                         │
                                                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PHASE 3: Lean 4                             │
│                                                                   │
│   theorem glucose_pid_isomorphism :                              │
│     ∃ φ : (ℝ × ℝ) → (ℝ × ℝ × ℝ),                                │
│       Bijective φ ∧                                              │
│       (∀ t state,                                                │
│         φ (glucose_ode t state) =                                │
│         pid_ode t (φ state))                                     │
│   := by                                                          │
│     -- Formal proof using Mathlib                                │
│     ...                                                          │
│                                                                   │
│   ✓ PROVEN ─────────────────────▶  Certified Result             │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Next Steps

1. **Complete Phase 1** (Steps 4-16 of current plan)
2. **Add glucose-insulin models** (Phase 1.5)
3. **Design JSON schema** for Python-Lean communication
4. **Start learning Lean 4** (work through Mathlib ODE examples)
5. **Formalize first simple system** in Lean

---

**Last Updated:** 2026-01-14
**Author:** Claude Sonnet 4.5 (architecture design)
**Project:** Synthetic Reasoning Forge
**Status:** Pre-Alpha (Phase 1 in progress - Day 3 visualization architecture)
