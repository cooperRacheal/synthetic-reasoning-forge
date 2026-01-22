"""Custom exceptions for Python-Lean bridge."""

from pathlib import Path


class LeanBridgeError(Exception):
    """Base exception for Lean bridge errors."""
    pass

class LeanTimeoutError(LeanBridgeError):
    """Lean process exceeded time limit."""

    def __init__(self, timeout: float, input_json: str) -> None:
        self.timeout = timeout
        self.input_json = input_json
        super().__init__(
            f"Lean verification timed out after {timeout}s\n"
            f"input: {input_json[:200]}..."
        )

class LeanExecutableNotFoundError(LeanBridgeError):
    """Lean executable not found or not built."""

    def __init__(self, executable_path: Path, lean_dir: Path) -> None:
        self.executable_path = executable_path
        self.lean_dir = lean_dir
        super().__init__(
            f"Lean executable not found: {executable_path}\n"
            f"Run: cd {lean_dir} && lake build {executable_path.name}"
        )

class LeanExecutionError(LeanBridgeError):
    """Lean process crashed or returned non-zero exit code."""

    def __init__(self, exit_code: int, stderr: str, input_json: str) -> None:
        self.exit_code = exit_code
        self.stderr = stderr
        self.input_json = input_json
        super().__init__(
            f"Lean verification failed (exit code {exit_code})\n"
            f"stderr: {stderr}\n"
            f"input: {input_json[:200]}..."
        )

class LeanResponseParseError(LeanBridgeError):
    """Failed to parse JSON response from Lean."""

    def __init__(self, raw_output: str, parse_error: str) -> None:
        self.raw_output = raw_output
        self.parse_error = parse_error
        super().__init__(
            f"Invalid JSON response from Lean: {parse_error}\n"
            f"output: {raw_output[:200]}..."
        )

