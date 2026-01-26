"""Error handling tests for Python-Lean bridge."""

import json
from pathlib import Path
from unittest.mock import Mock, patch
import subprocess

import pytest
from src.logic.lean_bridge import (
    LeanClient,
    LeanExecutableNotFoundError,
    LeanExecutionError,
    LeanResponseParseError,
    LeanTimeoutError,
)

@pytest.fixture
def lean_dir() -> Path:
    """Path to Lean project directory."""
    repo_root = Path(__file__).parent.parent.parent
    return repo_root / "lean"

@pytest.fixture
def lean_client(lean_dir: Path) -> LeanClient:
    """LeanClient instance."""
    return LeanClient(lean_dir)

class TestExecutableErrors:
    """Test error related to Lean executable."""

    def test_executable_not_found(self, tmp_path: Path) -> None: 
        """Test LeanExecutableNotFoundError with executable missing."""
        # Create client pointing to directory without executable
        client = LeanClient(tmp_path)

        with pytest.raises(LeanExecutableNotFoundError) as exc_info:
            client.verify_decay("{}")

        assert "lake build" in str(exc_info.value)
        assert exc_info.value.executable_path == tmp_path / ".lake" / "build" / "bin" / "verify_decay"
        assert exc_info.value.lean_dir == tmp_path

class TestLeanParseErrors:
    """Test Lean's error handling for malformed input."""

    def test_malformed_json_input(self, lean_client: LeanClient) -> None:
        """Test that lean returns PARSE_ERROR for malformed JSON."""

        # Send invalid JSON
        result = lean_client.verify_decay("not json at all")

        assert result.success is False
        assert result.error_code == "PARSE_ERROR"

    def test_invalid_json_schema(self, lean_client: LeanClient) -> None:
        """Test that Lean returns PARSE_ERROR for wrong schema."""
        bad_schema = json.dumps({"wrong": "schema"})
        result = lean_client.verify_decay(bad_schema)

        assert result.success is False
        assert result.error_code == "PARSE_ERROR"

    def test_missing_required_field(self, lean_client: LeanClient) -> None:
        """Test PARSE_ERROR when field missing."""
        # Valid structure but missing "parameters"
        incomplete = json.dumps({
            "system_type" : "decay",
            "initial_condition": {"t0": {"num": 0, "den": 1}, "x0": {"num": 5, "den": 1}},
            "interval": {"tmin": {"num": -1, "den": 10}, "tmax": {"num": 1, "den": 10}}
        })
        result = lean_client.verify_decay(incomplete)

        assert result.success is False
        assert result.error_code == "PARSE_ERROR"
        
class TestMockedSubprocessErrors:
    """Test error paths that require mocking subprocess."""

    def test_timeout_error(self, lean_dir: Path) -> None:
        client = LeanClient(lean_dir, default_timeout=0.001)

        with patch("src.logic.lean_bridge.client.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(
                cmd=["verify_decay"], timeout=0.001
            )

            with pytest.raises(LeanTimeoutError) as exc_info:
                client.verify_decay("{}")

            assert exc_info.value.timeout == 0.001
            assert exc_info.value.input_json == "{}"

    def test_lean_execution_error_nonzero_exit(self, lean_dir: Path) -> None:
        """Test LeanExecutionError when Lean crashes."""
        client = LeanClient(lean_dir)

        with patch("src.logic.lean_bridge.client.subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.returncode = 1
            mock_result.stdout = ""
            mock_result.stderr = "Lean crashed!"
            mock_run.return_value = mock_result

            with pytest.raises(LeanExecutionError) as exc_info:
                client.verify_decay("{}")

            assert exc_info.value.exit_code == 1
            assert "crashed" in exc_info.value.stderr.lower()

    def test_unparseable_json_response(self, lean_dir: Path) -> None:
        """Test LeanResponseParseError with Lean returns bad JSON."""
        client = LeanClient(lean_dir)

        with patch("src.logic.lean_bridge.client.subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "Not JSON"
            mock_result.stderr = ""
            mock_run.return_value = mock_result

            with pytest.raises(LeanResponseParseError) as exc_info:
                client.verify_decay("{}")

            assert exc_info.value.raw_output == "Not JSON"
            
    def test_io_logging_captures_subprocess_io(
        self, lean_dir: Path, caplog: pytest.LogCaptureFixture
    ) -> None: 
        """Test that log_io=True captures input/output/stderr."""
        import logging

        client = LeanClient(lean_dir, log_io=True)

        with caplog.at_level(logging.DEBUG):
            # Mock successful subprocess run
            with patch("src.logic.lean_bridge.client.subprocess.run") as mock_run:
                mock_result = Mock()
                mock_result.returncode = 0
                mock_result.stdout = '{"success":true,"message":"test","error_code":null,"details":null}'
                mock_result.stderr = ""
                mock_run.return_value = mock_result

                # Call with test input
                client.verify_decay('{"test": "input"}')

        assert "Lean input:" in caplog.text 
        assert "Lean stdout:" in caplog.text
        assert "Lean stderr:" in caplog.text
        assert "Lean exit code:" in caplog.text
        assert '{"test": "input"}' in caplog.text
