"""Unit tests for logger configuration."""

import logging

from src.logic.logger import get_logger


class TestLogger:
    """Test logger configuration and behavior."""

    def test_returns_logger_instance(self):
        """get_logger returns logging.Logger instance."""
        logger = get_logger("Test")
        assert isinstance(logger, logging.Logger)

    def test_logger_has_correct_name(self):
        """Logger name matches input parameter."""
        logger = get_logger("test.module")
        assert logger.name == "test.module"

    def test_no_duplicate_handlers(self):
        """Calling get_logger multiple times doesn't add duplicate handlers."""
        logger1 = get_logger("Test")
        handler_count1 = len(logger1.handlers)
        logger2 = get_logger("Test")
        handler_count2 = len(logger2.handlers)
        assert handler_count1 == handler_count2
