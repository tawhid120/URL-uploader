"""Tests for bot.logging_config module."""

import logging

from bot.logging_config import MemoryLogHandler, setup_logging, memory_handler


class TestMemoryLogHandler:
    def test_emit_stores_formatted_message(self):
        handler = MemoryLogHandler(capacity=10)
        handler.setFormatter(logging.Formatter("%(message)s"))
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="hello %s", args=("world",), exc_info=None,
        )
        handler.emit(record)
        logs = handler.get_logs()
        assert len(logs) == 1
        assert logs[0] == "hello world"

    def test_capacity_limit(self):
        handler = MemoryLogHandler(capacity=3)
        handler.setFormatter(logging.Formatter("%(message)s"))
        for i in range(5):
            record = logging.LogRecord(
                name="test", level=logging.INFO, pathname="", lineno=0,
                msg="msg-%d", args=(i,), exc_info=None,
            )
            handler.emit(record)
        logs = handler.get_logs()
        assert len(logs) == 3
        assert logs[0] == "msg-2"
        assert logs[-1] == "msg-4"

    def test_get_logs_count(self):
        handler = MemoryLogHandler(capacity=10)
        handler.setFormatter(logging.Formatter("%(message)s"))
        for i in range(10):
            record = logging.LogRecord(
                name="test", level=logging.INFO, pathname="", lineno=0,
                msg="line-%d", args=(i,), exc_info=None,
            )
            handler.emit(record)
        assert len(handler.get_logs(count=3)) == 3
        assert handler.get_logs(count=3)[0] == "line-7"

    def test_clear(self):
        handler = MemoryLogHandler(capacity=10)
        handler.setFormatter(logging.Formatter("%(message)s"))
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="data", args=(), exc_info=None,
        )
        handler.emit(record)
        assert len(handler.get_logs()) == 1
        handler.clear()
        assert len(handler.get_logs()) == 0

    def test_empty_handler_returns_empty(self):
        handler = MemoryLogHandler(capacity=5)
        assert handler.get_logs() == []


class TestMemoryHandlerSingleton:
    def test_shared_instance_exists(self):
        assert isinstance(memory_handler, MemoryLogHandler)
        assert memory_handler.buffer.maxlen == 1000


class TestSetupLogging:
    def test_does_not_raise(self):
        # setup_logging should be idempotent and not raise
        setup_logging()

    def test_root_logger_has_handlers(self):
        setup_logging()
        root = logging.getLogger()
        assert len(root.handlers) >= 1

    def test_uvicorn_access_level(self):
        setup_logging()
        uv_logger = logging.getLogger("uvicorn.access")
        assert uv_logger.level >= logging.WARNING
