"""Python client for Lean verification via subprocess."""

import json
import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from src.logic.lean_bridge.exceptions import (
    LeanExecutableNotFoundError,
    LeanExecutionError,
    LeanResponseParseError,
    LeanTimeoutError,
)

logger = logging.getLogger(__name__)

@dataclass
class VerificationResult:
    """Result from Lean verification."""

    success: bool
    message: str
    error_code: Optional[str] = None
    details: Optional[str] = None

    @classmethod
    def from_json(cls, json_str: str) -> "VerificationResult":
        """Parse VerificationResult from JSON string."""
        try: 
            data = json.loads(json_str)
            return cls(
                success=data["success"],
                message=data["message"],
                error_code=data.get("error_code"),
                details=data.get("details"),
            )

        except (json.JSONDecodeError, KeyError) as e: 
            raise LeanResponseParseError(json_str, str(e))

class LeanClient:
    """Client for Lean verification with comprehensive error handling."""

    def __init__(
        self,
        lean_dir: Path,
        default_timeout: float = 10.0,
        log_io: bool = False,
    ) -> None:
        """Initialize Lean client."""
        self.lean_dir = lean_dir
        self.executable = lean_dir / ".lake" / "build" / "bin" / "verify_decay"
        self.default_timeout = default_timeout
        self.log_io = log_io

    def verify_decay(
        self, json_input: str, timeout: Optional[float] = None
    ) -> VerificationResult:
        """Verify decay system via Lean subprocess."""
        # Check executable exists
        if not self.executable.exists():
            raise LeanExecutableNotFoundError(self.executable, self.lean_dir)

        # Use default timeout if not specified
        timeout = timeout or self.default_timeout

        # Log input if debugging
        if self.log_io:
            logger.debug(f"Lean input: {json_input}")

        try: 
            # Run subprocess with timeout
            result = subprocess.run(
                [str(self.executable)],
                input=json_input,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False, # Handle exit codes manually
                cwd=str(self.lean_dir),
            )

            # Log output if debugging
            if self.log_io:
                logger.debug(f"Lean stdout: {result.stdout}")
                logger.debug(f"Lean stderr: {result.stderr}")
                logger.debug(f"Lean exit code: {result.returncode}")

            # Check exit code
            if result.returncode != 0:
                raise LeanExecutionError(
                    result.returncode, result.stderr, json_input
                )

            # Parse and return result
            return VerificationResult.from_json(result.stdout.strip())
            
        except subprocess.TimeoutExpired as e:
            logger.error(f"Lean verification timed out after {timeout}s")
            raise LeanTimeoutError(timeout, json_input) from e            
