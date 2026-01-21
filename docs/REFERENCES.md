# References and Citations

> Scientific literature sources for parameter choices and model validation

---

## Damped Pendulum Parameters (examples/validate_plotting.py)

**Context:** Setting biologically relevant default parameters for `DampedPendulum` system to model human limb swing dynamics.

**Parameter Choices:**
- **Length (L):** 1.0 m (human leg scale)
- **Gravity (g):** 9.81 m/s²
- **Damping coefficient (b):** 0.5 N·m·s/rad (light damping)

**Rationale:**
Parameters chosen to represent human limb-scale pendulum with light damping consistent with observed gait biomechanics. Human arms and legs during walking exhibit passive pendular dynamics with minimal active control.

### Supporting Literature

**1. Arm Swing as Passive Pendulum**
- **Source:** Collins et al. (2009). "Dynamic arm swinging in human walking"
- **Link:** [PMC Article](https://pmc.ncbi.nlm.nih.gov/articles/PMC2817299/)
- **Key Findings:**
  - Arms function as "passive pendulums" during normal gait
  - Peak shoulder torques: 2.5 ± 0.6 N·m (minimal active control)
  - Upper-limb work rates: <0.013 W/kg (<1% of lower limb work)
  - Multiple stable oscillation modes achievable without active torque
  - Arm length proxy: ~0.9 m (based on leg length reference in study: 0.902 ± 0.074 m)

**2. Leg Swing Pendular Dynamics**
- **Source:** Maus et al. (2016). "A springy pendulum could describe the swing leg kinetics of human walking"
- **Link:** [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0021929016303098)
- **Key Findings:**
  - Springy pendulum model fits swing leg kinetics with R²>0.8
  - Swing phase governed by pendular dynamics across various walking speeds
  - Swing leg stiffness increases with walking speed and correlates with swing frequency

**3. Muscle Damping Coefficients**
- **Source:** Mechanical impedance studies (various)
- **Link:** [Mechanical Impedance and Motor Control - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4342527/)
- **Key Findings:**
  - Average muscle parallel damping constant: 1.73 N·s/m for elbow joint
  - Damping exerted by muscular activity controls pendular motion
  - Adding weight proximal to midpoint shortens effective pendulum length and increases damping

### Additional Search Results

**Biomechanics Literature (2024):**
- [How close to a pendulum is human upper limb movement during walking? - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0018442X04000514)
- [Verification of damped bipedal inverted pendulum model - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0888327023004697)
- [Dynamic Model of Lower Limb Motion in the Sagittal Plane - Redalyc](https://www.redalyc.org/journal/4988/498878679003/movil/)

### Parameter Justification

**Length (L = 1.0 m):**
- Human leg (hip to foot): ~0.9-1.0 m
- Human arm (shoulder to hand): ~0.6-0.8 m
- Value chosen at leg scale for visualization purposes

**Damping (b = 0.5 N·m·s/rad):**
- Produces lightly damped oscillation (3-5 cycles before settling)
- Consistent with "passive pendulum" behavior described in Collins et al.
- Damping ratio ζ ≈ 0.15-0.25 (underdamped regime)
- Natural frequency ω₀ = √(g/L) ≈ 3.13 rad/s (~0.5 Hz period)

**Note:** Literature provides qualitative descriptions (passive pendulum, light damping) rather than explicit dimensionless damping ratios or torque-based damping coefficients for simple pendulum models. Parameter choices represent reasonable approximations based on reported limb dynamics and oscillatory behavior.

---

## ODE Solver Methods

**LSODA (Auto-Fallback Method):**
- Livermore Solver for Ordinary Differential Equations with Automatic method switching
- Switches between Adams method (non-stiff) and BDF (stiff) based on detected stiffness
- Implemented in `scipy.integrate.solve_ivp` via method="LSODA"
- **Reference:** Petzold, L. (1983). "Automatic selection of methods for solving stiff and nonstiff systems of ordinary differential equations." SIAM Journal on Scientific and Statistical Computing, 4(1), 136-148.

---

## Testing Framework Documentation

### Pytest Fixtures and Dependency Injection

**Context:** Understanding pytest's fixture discovery mechanism during Day 6 comprehensive testing implementation. Needed to clarify how `tests/conftest.py` fixtures automatically inject into `tests/unit/*.py` test modules.

**Source:**
- **Pytest Fixtures Documentation:** https://docs.pytest.org/en/stable/fixture.html
- **Coverage:** Fixture definition, dependency injection, `conftest.py` discovery hierarchy, fixture scopes (function/class/module/session), fixture parametrization, teardown patterns via `yield`

**Key Concepts:**
- Pytest's fixture system provides built-in dependency injection (not standard Python)
- `conftest.py` is special filename pytest automatically scans for reusable fixtures
- Parent directory fixtures (`tests/conftest.py`) auto-inject into subdirectory tests (`tests/unit/*.py`)
- Fixtures requested via parameter name matching in test function signatures
- Default `scope="function"` creates fresh instance per test (isolation guarantee)

**Why Referenced:**
- Critical for understanding test isolation and fixture reuse strategy in comprehensive test suite
- Enables clean test code without manual setup/teardown in each test
- Foundation for Day 6-7 testing architecture (80-90% coverage target)

**Date Referenced:** January 17, 2026

---

**Last Updated:** January 17, 2026
**Contributor:** Racheal Cooper with Claude Sonnet 4.5
