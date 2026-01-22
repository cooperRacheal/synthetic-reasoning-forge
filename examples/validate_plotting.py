"""Visual validation for ODE plotting infrastructure.

Tests the plotting API with 1D time-series, 2D phase portraits and 3D attractors
to verify the Strategy+Factory pattern implementation works correctly.

Output
------
examples/output/lorenz_chaotic_3d.png     : Lorenz chaotic attractor 3D (σ=10, ρ=28, β=8/3)
examples/output/lorenz_chaotic_2d.png     : Lorenz chaotic x-y projection
examples/output/lorenz_stable_3d.png      : Lorenz stable fixed point 3D (σ=10, ρ=0.5, β=8/3)
examples/output/lorenz_stable_2d.png      : Lorenz stable x-y projection
examples/output/lorenz_convective_3d.png  : Lorenz convective cells 3D (σ=10, ρ=5, β=8/3)
examples/output/lorenz_convective_2d.png  : Lorenz convective x-y projection
examples/output/pendulum.png              : Damped pendulum phase portrait (2D, b=0.5)
examples/output/decay.png                 : Exponential decay time-series (1D, lambda=1.0) with analytic overlay

Usage
------
python examples/validate_plotting.py
"""

import numpy as np

from src.logic import solve_ode
from src.logic.systems import DampedPendulum, DecaySystem, LorenzSystem
from src.logic.plotting import plot_ode, PlotConfig

# Set plot configuration for all plots
config = PlotConfig(figsize=(12, 10), dpi=200, show_grid=True)

# LORENZ SYSTEM VALIDATION

print("Generating Lorenz system plots...")

# Chaotic regime (butterfly attractor)
lorenz_chaotic = LorenzSystem(10, 28, 8/3)
sol_lorenz_chaotic = solve_ode(lorenz_chaotic, (0, 40), [1.0, 1.0, 1.0])

plot_ode(
    sol_lorenz_chaotic.t,
    sol_lorenz_chaotic.y,
    labels=['x', 'y', 'z'],
    title='Lorenz Attractor (chaotic system)',
    config=config,
    save_path='examples/output/lorenz_chaotic_3d.png'
)
print("  ✓ lorenz_chaotic_3d.png")

# Stable fixed point (ρ < 1, spirals to origin)
lorenz_stable = LorenzSystem(10, 0.5, 8/3)
sol_lorenz_stable = solve_ode(lorenz_stable, (0, 20), [1.0, 1.0, 1.0])

plot_ode(
    sol_lorenz_stable.t,
    sol_lorenz_stable.y,
    labels=['x', 'y', 'z'],
    title='Lorenz Attractor (stable system)',
    config=config,
    save_path='examples/output/lorenz_stable_3d.png'
)
print("  ✓ lorenz_stable_3d.png")

# Convective cells (1 < ρ < 24.74, bi-stable)
lorenz_convective = LorenzSystem(10, 5, 8/3)
sol_lorenz_convective = solve_ode(lorenz_convective, (0, 30), [1.0, 1.0, 1.0])

plot_ode(
    sol_lorenz_convective.t,
    sol_lorenz_convective.y,
    labels=['x', 'y', 'z'],
    title='Lorenz Attractor (convective system)',
    config=config,
    save_path='examples/output/lorenz_convective_3d.png'
)
print("  ✓ lorenz_convective_3d.png")

# 2D PROJECTIONS (x-y plane)

print("\nGenerating 2D projections...")

plot_ode(
    sol_lorenz_chaotic.t,
    sol_lorenz_chaotic.y[:2, :],
    labels=['x', 'y'],
    title='Lorenz Attractor (chaotic 2D projection)',
    config=config,
    save_path='examples/output/lorenz_chaotic_2d.png'
)
print("  ✓ lorenz_chaotic_2d.png")

plot_ode(
    sol_lorenz_stable.t,
    sol_lorenz_stable.y[:2, :],
    labels=['x', 'y'],
    title='Lorenz Attractor (stable 2D projection)',
    config=config,
    save_path='examples/output/lorenz_stable_2d.png'
)
print("  ✓ lorenz_stable_2d.png")

plot_ode(
    sol_lorenz_convective.t,
    sol_lorenz_convective.y[:2, :],
    labels=['x', 'y'],
    title='Lorenz Attractor (convective 2D projection)',
    config=config,
    save_path='examples/output/lorenz_convective_2d.png'
)
print("  ✓ lorenz_convective_2d.png")

# DAMPED PENDULUM VALIDATION

print("\nGenerating damped pendulum plot...")

# Biologically relevant parameters (human limb swing dynamics)
# b=0.5 represents natural limb damping with muscle viscosity
pendulum = DampedPendulum(damping=0.5)
sol_pendulum = solve_ode(pendulum, (0, 20), [np.pi/4, 0.0])

plot_ode(
    sol_pendulum.t,
    sol_pendulum.y,
    labels=['theta (rad)', 'omega (rad/s)'],
    title='Damped Pendulum - Human Limb Swing (b=0.5)',
    config=config,
    save_path='examples/output/pendulum.png'
)
print("  ✓ pendulum.png")

# DECAY SYSTEM VALIDATION (1D time-series)

print("\nGenerating Decay system plot...")

# Plot with 1D plotter (factory auto-selects OneDimensionalPlotter)
decay = DecaySystem(lambda_=1.0)
sol_decay = solve_ode(decay, (0, 5), [5.0])
fig = plot_ode(
    sol_decay.t,
    sol_decay.y,
    labels=['Time (s)', 'x(t)'],
    title='Exponential Decay (λ=1.0)',
    config=config,
    save_path='examples/output/decay.png'
)

# Overlay analytic solution for validation
ax = fig.axes[0]
x_analytic = 5.0 * np.exp(-1.0 * sol_decay.t)
ax.plot(sol_decay.t, x_analytic, 'r--', linewidth=2, label='Analytic', alpha=0.7)
ax.legend()
fig.savefig('examples/output/decay.png', dpi=200)

print("  ✓ decay.png")

print("\nValidation complete! 8 plots generated in examples/output/")
