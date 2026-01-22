import Lean.Data.Json
import Lean.Data.Json.FromToJson
import Mathlib.Data.Real.Basic

-- DIAGNOSTIC CHECKS (remove after fixing)
#check Lean.FromJson
#check Lean.ToJson
#check Lean.Json.FromJson
#check Float
#check (5.0 : Float)
#check (↑(5.0 : Float) : Real)
#check instDecidableEqFloat

-- Input schema structures
structure InitialCondition where
    t0 : Float
    x0 : Float
    deriving FromJson

structure Interval where
    tmin : Float
    tmax : Float
    deriving FromJson

structure Parameters where
    lambda : Float
    deriving FromJson

structure DecayInput where
    system_type : String
    initial_condition : InitialCondition
    interval : Interval
    parameters : Parameters
    deriving FromJson
    
-- Output schema (structured errors)
structure VerificationResult where
    success : Bool
    message : String
    error_code : Option String
    details : Option String
    deriving ToJson

-- Validation logic (hardcoded Phase 3A checks for POC)
noncomputable def validateDecayInput (input : DecayInput) : IO VerificationResult := do
    -- Test Real conversion with x0 (learn pattern for parametric)
    let x0_real : Real := ↑input.initial_condition.x0
    
    -- Remaining fields use Float for now (validate pattern first)
    let t0 := input.initial_condition.t0
    let tmin := input.interval.tmin
    let tmax :=  input.interval.tmax
    let lambda := input.parameters.lambda

    -- Float comparison for t0 first
    if t0 ≠ 0.0 then
        return {
            success := false,
            message := "t0 must be 0.0 (Phase 3A constraint)",
            error_code := some "VALIDATION_ERROR",
            details := some s!"Expected 0.0, got {t0}"
        }
    else if x0_real ≠ 5 then -- Real comparison (testing)
        return {
            success := false,
            message := "x0 must be 5.0 (Phase 3A constraint)",
            error_code := some "VALIDATION_ERROR",
            details := some s!"Expected 5.0, got {input.initial_condition.x0}"
        }
    else if tmin ≠ -0.1 then
        return {
            success := false,
            message := "tmin must be -0.1 (Phase 3A constraint)",
            error_code := some "VALIDATION_ERROR",
            details := some s!"Expected -0.1, got {tmin}"
        }
    else if tmax ≠ 0.1 then
        return {
            success := false,
            message := "tmax must be 0.1 (Phase 3A constraint)",
            error_code := some "VALIDATION_ERROR",
            details := some s!"Expected 0.1, got {tmax}"
        }
    else if lambda ≠ 1.0 then
        return {
            success := false,
            message := "lambda must be 1.0 (Phase 3A constraint)",
            error_code := some "VALIDATION_ERROR",
            details := some s!"Expected 1.0, got {input.parameters.lambda}"
        }
     else 
        -- All checks pass - proof exists via decay_picard_specific
        return {
            success := true,
            message := "Verified by decay_picard_specific theorem",
            error_code := none,
            details := some "Phase 3A: x0=5, t∈[-0.1,0.1], λ=1"
        }

-- Helper for structured error output
def printError (code : String) (details : String) : IO Unit := do
    let result : VerificationResult := {
        success := false,
        message := s!"Verification failed: {code}",
        error_code := some code,
        details := some details
    }
    IO.println (Lean.toJson result).compress

-- Main executable (stdin -> stdout with error handling)
def main : IO Unit := do
    try
        let stdin ← IO.getStdin
        let inputStr ← stdin.readToEnd

        -- Parse JSON (returns Except)
        match Lean.Json.parse inputStr with
        | Except.error e =>
            printError "PARSE_ERROR" s!"Invalid JSON: {e}"
        | Except.ok json =>
            -- Deserialize (returns Except)
            match Lean.fromJson? json (α := DecayInput) with
            | Except.error e =>
                printError "PARSE_ERROR" s!"Invalid schema: {e}"
            | Except.ok input =>
                let result ← validateDecayInput input
                IO.println (Lean.toJson result).compress
     catch e =>
        -- Catch unexpected IO errors
        printError "INTERNAL_ERROR" (toString e)

        






