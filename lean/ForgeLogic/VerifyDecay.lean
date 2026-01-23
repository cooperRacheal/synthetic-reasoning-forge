import Lean.Data.Json
import Lean.Data.Json.FromToJson
import Mathlib.Data.Real.Basic


-- Custom JSON instance for Rat ({"numerator": int, "denominator": int}) representation
-- Lean's Rat type has numerator : Int and denominator : Nat fields
-- We serialize as JSON objects with these fields for exact arithmetic

-- From Json: Parse JSON -> Rat
instance : Lean.FromJson Rat where
    fromJson? json := do
        -- Extract "numerator" field from JSON object
        let numJson <- json.getObjVal? "num"
        -- Extract "denominator" field from JSON object
        let denJson <- json.getObjVal? "den"
        -- Parse numerator as Int (can be negative)
        let num : Int <- Lean.fromJson? numJson
        -- Parse denominator as Nat (always positive)
        let den : Nat <- Lean.fromJson? denJson
        -- Construct Rat via division (Int / Nat -> Rat)
        return num / den

-- ToJson: Serialize Rat -> JSON
instance : Lean.ToJson Rat where
    toJson r := Lean.Json.mkObj [
        ("num", Lean.toJson r.num),
        ("den", Lean.toJson r.den)
    ]

-- Input schema structures (Rat-based for exact arithmetic)
structure InitialCondition where
    t0 : Rat
    x0 : Rat
    deriving Lean.FromJson

structure Interval where
    tmin : Rat
    tmax : Rat
    deriving Lean.FromJson

structure Parameters where
    lambda : Rat
    deriving Lean.FromJson

structure DecayInput where
    system_type : String
    initial_condition : InitialCondition
    interval : Interval
    parameters : Parameters
    deriving Lean.FromJson

-- Output schema (structured errors)
structure VerificationResult where
    success : Bool
    message : String
    error_code : Option String
    details : Option String
    deriving Lean.ToJson

-- Validation logic (hardcoded Phase 3A checks for POC)
-- Pure Rat comparisons (computable I/O layer)
def validateDecayInput (input : DecayInput) : IO VerificationResult := do
    let t0 := input.initial_condition.t0
    let x0 := input.initial_condition.x0
    let tmin := input.interval.tmin
    let tmax := input.interval.tmax
    let lambda := input.parameters.lambda
    -- Rat comparisons (decidable equality)
    if t0 ≠ 0 then
        return {
            success := false,
            message := "t0 must be 0 (Phase 3A constraint)",
            error_code := some "VALIDATION_ERROR",
            details := some s!"Expected 0, got {t0}"
        }
    else if x0 ≠ 5 then
        return {
            success := false,
            message := "x0 must be 5 (Phase 3A constraint)",
            error_code := some "VALIDATION_ERROR",
            details := some s!"Expected 5, got {x0}"
        }
    else if tmin ≠ -1/10 then
        return {
            success := false,
            message := "tmin must be -0.1 (Phase 3A constraint)",
            error_code := some "VALIDATION_ERROR",
            details := some s!"Expected -1/10, got {tmin}"
        }
    else if tmax ≠ 1/10 then
        return {
            success := false,
            message := "tmax must be 0.1 (Phase 3A constraint)",
            error_code := some "VALIDATION_ERROR",
            details := some s!"Expected 1/10, got {tmax}"
        }
    else if lambda ≠ 1 then
        return {
            success := false,
            message := "lambda must be 1 (Phase 3A constraint)",
            error_code := some "VALIDATION_ERROR",
            details := some s!"Expected 1, got {lambda}"
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

-- Kernel test: Verify Rat->Real coercion works (not used in I/O layer)
#check (5 : Rat)
#check ((5 : Rat) : Real)      -- Automatic coercion
#check ((-1/10 : Rat) : Real)  -- Fractional coercion

-- Verify coercion is computable in type system (will be used in proof layer)
example : Real := (5 : Rat)
example : Real := (-1/10 : Rat)






