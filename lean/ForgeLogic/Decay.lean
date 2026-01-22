import Mathlib.Analysis.ODE.PicardLindelof
import Mathlib.Data.Real.Basic

/-!
# Parametric Picard-Lindelöf for Exponential Decay

Generalizes Phase 3A fixed proof to arbitrary (lambda, t0, x0, interval).
-/

def decay_rhs (lambda : Real) : Real -> Real -> Real := fun _t x => -lambda * x

theorem decay_picard_parametric
  (lambda : Real) (h_lambda_pos : 0 < lambda)
  (t0 x0 : Real) (tmin tmax : Real)
  (h_interval : tmin ≤ t0 ∧ t0 ≤ tmax)
  (h_order : tmin < tmax)
  : ∃ (a r L K : NNReal),
    IsPicardLindelof (decay_rhs lambda) ⟨t0, Set.mem_Icc.mpr h_interval⟩ x0 a r L K := by
  -- Compute parametric values
  let a_val : NNReal := ⟨abs x0 + 1, by positivity⟩
  let L_val : NNReal := ⟨lambda * (2 * abs x0 + 1), by positivity⟩
  let k_val : NNReal := ⟨lambda, le_of_lt h_lambda_pos⟩
  let r_val : NNReal := ⟨max (t0 - tmin) (tmax - t0), by {
    apply le_max_iff.mpr
    left
    linarith [h_interval.1]
  }⟩
  use a_val, r_val, L_val, k_val
  constructor
  case lipschitzOnWith =>
    intro t ht_in y hy_in z hz_in
    simp [decay_rhs]
    refine LipschitzWith.edist_le_mul ?_ y z
    refine LipschitzWith.of_le_add_mul k_val ?_
    intro x y
    calc lambda * x
      ≤ lambda * (y + dist x y) := by {
          apply mul_le_mul_of_nonneg_left _ (le_of_lt h_lambda_pos)
          linarith [abs_sub_le_iff.mp (le_refl (dist x y))]
      }
      _ = lambda * y + lambda * dist x y := by ring
      _ ≤ lambda * y + ↑k_val * dist x y := by simp [k_val]
  case continuousOn =>
    intro x hx
    apply Continuous.continuousOn
    simp [decay_rhs]
    exact continuous_const
  case norm_le =>
    intro t ht x hx
    simp only [decay_rhs]
    rw [norm_mul]
    rw [norm_neg, Real.norm_eq_abs, abs_of_pos h_lambda_pos]
    sorry
  case mul_max_le =>
    simp
    sorry -- TODO: will also fail with hardcoded values
