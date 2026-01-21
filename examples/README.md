# examples/

> Validation scripts and demonstration outputs for ODE solver + visualization architecture

## Files

### validate_plotting.py

**Purpose:** Visual validation script demonstrating ODE solver + plotting architecture

**Systems Tested:**
- **Lorenz System** (3 regimes)
  - Chaotic (σ=10, ρ=28, β=8/3) - Classic butterfly attractor
  - Stable (σ=10, ρ=10, β=8/3) - Convergence to fixed point
  - Convective (σ=10, ρ=20, β=8/3) - Limit cycle behavior

- **Damped Pendulum**
  - Biologically relevant parameters (b=0.5 N·m·s/rad, human limb scale)
  - Demonstrates damped oscillation to equilibrium

**Outputs:** 7 plots saved to `examples/output/`

**Usage:**
```bash
python examples/validate_plotting.py
```

---

## output/

Pre-generated visualization outputs demonstrating solver and plotting architecture. These PNG files are **tracked in git** for documentation and demonstration purposes.

### Tracked Outputs (7 files)

**Lorenz System:**
- `lorenz_chaotic_3d.png` - 3D butterfly attractor
- `lorenz_chaotic_2d.png` - 2D x-y projection
- `lorenz_stable_3d.png` - 3D stable fixed point
- `lorenz_stable_2d.png` - 2D projection
- `lorenz_convective_3d.png` - 3D limit cycle
- `lorenz_convective_2d.png` - 2D projection

**Damped Pendulum:**
- `pendulum.png` - Phase portrait showing damped spiral to equilibrium

### Note on Binary Files

These PNG files are tracked in git to provide visual documentation of expected output. They demonstrate:
- Correct solver behavior across different dynamical regimes
- Factory pattern automatically selecting 2D vs 3D plotters
- Strategy pattern extensibility for visualization

If regenerating plots frequently becomes an issue, consider moving to external documentation hosting.

---

**Last Updated:** 2026-01-21
**Script:** Day 6 (Jan 17, 2026) - Visual validation suite
