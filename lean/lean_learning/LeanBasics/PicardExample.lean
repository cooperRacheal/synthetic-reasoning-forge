import Mathlib.Analysis.ODE.PicardLindelof
import Mathlib.Data.Real.Basic

/-!
# Picard-Lindelöf Theorem for Exponential Decay Equation

This file proves that the 1D exponential decay ODE dx/dt= -x satisfies the
Picard-Lindelöf (Cauchy-Lipschitz) theorem, guaranteeing the existence and uniqueness
of solutions.

## Main Results:
    - decay_picard_specific : Concrete proof for IC x(0)=5 on the interval of t [-0.1,0.1]

## Picard-Lindelöf Conditions
To prove existence/uniqueness, we must show the RHS function satisfies:
1. **lipschitzOnWith K**: Lipschitz continuous with constant K in state variable (x)
uniformly over t
2. **continuousOn**: continuous in time variable (t) for each fixed x
in state ball
3. **norm_le L**: Bounded by L on the domain (time x state)
4. **mul_max_le**: Consistency condition L * max(tmax-t0, t0-tmin) \le a - r
-/

-- RHS of decay equation f(t,x) = -x
def decay_rhs : Real -> Real -> Real := fun _t x => -x

-- Helper: proof that 0 ∈ [-0.1,0.1]
def t0_in_interval : (0 : Real) ∈ Set.Icc (-0.1) 0.1 := by norm_num

/--
Concrete example: For x(0) = 5 on interval [-0.1, 0.1], the decay equation
satisfies Picard-Lindelöf with parameters:
- a = 1 (state ball radius around x0)
- r = 0 (solution contained in the full ball, no safety margin)
        (Note: full ball, a-r = a)
- L = 6 (norm bound: |f(t,x)| \le 6 for x in [4,6])
- K = 1 (Lipschitz constant: |f(t,x) - f(t,y)| \le 1 * |x - y|)
-/

theorem decay_picard_specific:
        ∃ (a r L K : NNReal),
        IsPicardLindelof decay_rhs ⟨0, t0_in_interval⟩ 5 a r L K := by
    use 1, 0, 6, 1
    constructor

    -- Case 1: Lipschitz continuity with K = 1
    case lipschitzOnWith =>
        intro t ht_in y hy_in z hz_in
        simp [decay_rhs]

    -- Case 2: Continuity in time (constant function)
    case continuousOn =>
        intro x hx
        simp [decay_rhs]
        exact continuousOn_const

    -- Case 3: Norm bound |f(t,x)| ≤ 6
    case norm_le =>
      intro t ht x hx
      simp only [decay_rhs]
      rw [norm_neg, Real.norm_eq_abs]
      have h : |x - 5| ≤ 1 := by
        have := Metric.mem_closedBall.mp hx
        simpa [Real.dist_eq] using this
      calc |x| = |(x - 5) + 5| := by ring_nf
           _ ≤ |x - 5| + |5| := abs_add_le _ _
           _ = |x - 5| + 5 := by norm_num
           _ ≤ 1 + 5 := by linarith [h]
           _ = 6 := by norm_num

    -- Case 4: Consistency condition 6 * 0.1 ≤ 1
    case mul_max_le =>
        simp
        norm_num
