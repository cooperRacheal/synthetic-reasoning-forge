# LeanBasics

> Learning exercises for Lean 4 theorem proving focused on ODE formalization

## Overview

This project contains structured learning exercises progressing from basic Lean 4 tactics to formal verification of ODE existence/uniqueness theorems using Mathlib's Picard-Lindelöf formalization.

**Sessions:** 4 learning sessions (4 hours) + 1 complete proof (10-11 hours)
**Status:** Phase 3A complete

---

## Files

### Learning Exercises

**Arithmetic.lean** - Session 1A: First Proofs
Basic proof tactics: `rfl` (reflexivity), `rw` (rewriting), `exact` (exact terms)

**ODETypes.lean** - Session 1B: Types & Structures
Dependent types, structures, `Fin n`, matrix notation. Implements `StateSpace` and `ODESystem` structures with simple harmonic oscillator example.

**Tactics.lean** - Session 2A: Core Tactics
6 fundamental tactics: `rfl`, `intro`, `exact`, `apply`, `rw`, `simp`. Hypothesis manipulation and tactic chaining.

**AnalysisTactics.lean** - Session 2B: Analysis Tactics
Automation for real analysis: `ring`, `norm_num`, `field_simp`, `fun_prop`, `have`. **Capstone:** Proved Lorenz system RHS continuous.

### Complete Proof

**PicardExample.lean** - Phase 3A: First Picard-Lindelöf Proof
Proves existence and uniqueness for exponential decay `dx/dt = -x` on interval `[-0.1, 0.1]` with IC `x(0)=5`. All 4 Picard-Lindelöf cases proven:
- Lipschitz continuity (K=1)
- Time continuity (constant RHS)
- Norm bound (L=6) via calc chains
- Consistency condition (6 * 0.1 ≤ 1)

---

## Dependencies

**Mathlib:** v4.26.0 (specified in `lakefile.toml`, locked in `lake-manifest.json`)
**Lean:** 4.26.0 (specified in `lean-toolchain`)

Key imports:
- `Mathlib.Analysis.ODE.PicardLindelof`
- `Mathlib.Data.Real.Basic`

---

## Building

```bash
# From lean/lean_learning directory
lake build

# Check specific file
lake env lean LeanBasics/PicardExample.lean
```

---

**Last Updated:** 2026-01-21
**Learning Path:** Days 7-9 (Jan 18-20, 2026)
