"""Integration tests for Python-Lean bridge."""

import json
from pathlib import Path

import pytest

from src.logic.lean_bridge import DecaySerializer, LeanClient
from src.logic.systems.decay import DecaySystem

@pytest.fixture
def lean_dir() -> Path:
    """Path to Lean project directory."""
    repo_root = Path(__file__).parent.parent.parent
    return repo_root / "lean"

@pytest.fixture
def lean_client(lean_dir: Path) -> LeanClient: 
    """LeanClient instance."""
    return LeanClient(lean_dir)

@pytest.fixture
def phase3a_system() -> DecaySystem:
    """DecaySystem with Phase 3A parameters."""
    return DecaySystem(lambda_=1.0)

@pytest.fixture
def phase3a_serializer(phase3a_system: DecaySystem) -> DecaySerializer:
    """DecaySerializer from Phase 3A system."""
    return DecaySerializer(phase3a_system)

class TestDecaySerializer: 
    """Test serializer validation and Rat formatting."""

    def test_rejects_wrong_lambda(self) -> None:
        """Test that serializer rejects lambda != 1.0."""
        wrong = DecaySystem(lambda_=2.0)
        with pytest.raises(ValueError, match="lambda=1.0"):
            DecaySerializer(wrong)

    def test_validates_t0(self, phase3a_serializer: DecaySerializer) -> None:
        """Test that serializer validates t0=0.0."""
        with pytest.raises(ValueError, match="t0=0.0"):
            phase3a_serializer.to_json(t0=1.0, x0=5.0, tmin=-0.1, tmax=0.1)

    def test_validates_x0(self, phase3a_serializer: DecaySerializer) -> None:
        """Test that serializer validates x0=5.0."""
        with pytest.raises(ValueError, match="x0=5.0"):
            phase3a_serializer.to_json(t0=0.0, x0=10.0, tmin=-0.1, tmax=0.1)

    def test_validates_tmin(self, phase3a_serializer: DecaySerializer) -> None:
        """Test that serializer validates tmin=-0.1."""
        with pytest.raises(ValueError, match="tmin=-0.1"):
            phase3a_serializer.to_json(t0=0.0, x0=5.0, tmin=0.0, tmax=0.1)

    def test_validates_tmax(self, phase3a_serializer: DecaySerializer) -> None:
        """Test that serializer validates tmax=0.1."""
        with pytest.raises(ValueError, match="tmax=0.1"):
            phase3a_serializer.to_json(t0=0.0, x0=5.0, tmin=-0.1, tmax=0.2)

    def test_produces_valid_rat_json(
        self, phase3a_serializer: DecaySerializer) -> None:
        """Test that serializer produces valid Rat JSON."""
        json_str = phase3a_serializer.to_json(
            t0=0.0, x0=5.0, tmin=-0.1, tmax=0.1
        )
        data = json.loads(json_str)

        assert data["system_type"] == "decay"
        assert data["initial_condition"]["t0"] == {"num": 0, "den": 1}
        assert data["initial_condition"]["x0"] == {"num": 5, "den": 1}
        assert data["interval"]["tmin"] == {"num": -1, "den": 10}
        assert data["interval"]["tmax"] == {"num": 1, "den": 10}
        assert data["parameters"]["lambda"] == {"num": 1, "den": 1}
            
class TestLeanClient:
    """Test Lean client integration."""
    
    def test_phase3a_verification_succeeds(
        self, lean_client: LeanClient, phase3a_serializer: DecaySerializer
    ) -> None: 
        """Test that Phase 3A values verify successfully."""
        json_input = phase3a_serializer.to_json(
            t0=0.0, x0=5.0, tmin=-0.1, tmax=0.1
        )
        result = lean_client.verify_decay(json_input)
        assert result.success
        assert result.error_code is None
    
    def test_wrong_t0_rejected(self, lean_client: LeanClient) -> None:
        """Test that Lean rejects t0 != 0.0. for phase 3A."""            
        bad_json = json.dumps({
            "system_type": "decay",
            "initial_condition": {"t0": {"num": 1, "den": 1}, "x0": {"num": 5, "den": 1}},
            "interval": {"tmin": {"num": -1, "den": 10}, "tmax": {"num": 1, "den":  10}},
            "parameters": {"lambda": {"num": 1, "den": 1}},
        })
        result = lean_client.verify_decay(bad_json)
        assert not result.success
        assert result.error_code == "VALIDATION_ERROR"
        
    def test_wrong_x0_rejected(self, lean_client: LeanClient) -> None:
        """Test that Lean rejects x0 != 5.0 for phase 3A."""
        bad_json = json.dumps({
            "system_type": "decay",
            "initial_condition": {"t0": {"num": 0, "den":1}, "x0": {"num": 1, "den": 1}},
            "interval": {"tmin": {"num": -1, "den": 10}, "tmax": {"num": 1, "den": 10}},
            "parameters": {"lambda": {"num": 1, "den": 1}}
        })
        result = lean_client.verify_decay(bad_json)
        assert not result.success
        assert result.error_code == "VALIDATION_ERROR"

class TestEndToEnd:
    """Test complete flow."""

    def test_full_pipeline(
        self, lean_client: LeanClient, phase3a_system: DecaySystem
    ) -> None: 
        """Test DecaySystem -> JSON -> Lean -> Result."""
        serializer = DecaySerializer(phase3a_system)
        json_input = serializer.to_json(t0=0.0, x0=5.0, tmin=-0.1, tmax=0.1)
        result = lean_client.verify_decay(json_input)
        assert result.success is True
        assert result.error_code is None
        assert result.details is not None # verifies Lean returns details
        
