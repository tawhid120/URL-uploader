"""Tests that Pyrogram dispatcher uses the correct event loop.

The Pyrogram Client is created at module-import time, so its
Dispatcher stores whatever ``asyncio.get_event_loop()`` returns at
that point.  When uvicorn later starts a **new** event loop, the
lifespan must patch ``dispatcher.loop`` before calling ``bot.start()``
so that handler-registration tasks actually execute.
"""

import asyncio
from collections import OrderedDict

import pytest


def _run_coroutine(coro):
    """Run a coroutine on the current event loop (test-safe)."""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)


class TestDispatcherLoopPatch:
    """Verify the lifespan patches the dispatcher loop before start."""

    def test_import_time_loop_differs_from_asyncio_run(self):
        """asyncio.run() creates a new event loop, different from the
        loop returned by get_event_loop() at import time."""
        manual_loop = asyncio.new_event_loop()
        try:
            # A loop created manually is never the same object as the one
            # returned by get_event_loop() for the main thread.
            assert manual_loop is not asyncio.get_event_loop()
        finally:
            manual_loop.close()

    def test_dashboard_imports_asyncio(self):
        """bot.dashboard must import asyncio for the loop patch."""
        import bot.dashboard as dashboard

        assert hasattr(dashboard, "asyncio")

    def test_lifespan_patches_loop(self):
        """The lifespan source must assign bot.dispatcher.loop before start."""
        import inspect
        from bot.dashboard import _get_app

        app = _get_app()
        # Find the lifespan in the app
        lifespan = app.router.lifespan_context
        src = inspect.getsource(lifespan)

        # The source should set dispatcher.loop before calling start
        loop_patch_idx = src.find("dispatcher.loop")
        start_idx = src.find("bot.start()")
        assert loop_patch_idx != -1, "lifespan must patch bot.dispatcher.loop"
        assert start_idx != -1, "lifespan must call bot.start()"
        assert loop_patch_idx < start_idx, (
            "dispatcher.loop must be patched BEFORE bot.start() is called"
        )

    def test_lifespan_imports_handlers_before_start(self):
        """The lifespan should import handlers so direct uvicorn startup works."""
        import inspect
        from bot.dashboard import _get_app

        app = _get_app()
        lifespan = app.router.lifespan_context
        src = inspect.getsource(lifespan)

        import_idx = src.find("import bot.handlers.commands.start")
        start_idx = src.find("bot.start()")
        assert import_idx != -1, "lifespan must import handler modules"
        assert start_idx != -1, "lifespan must call bot.start()"
        assert import_idx < start_idx, "handlers must be imported BEFORE bot.start()"

    def test_add_handler_on_correct_loop_registers(self):
        """Simulates that patching the loop allows add_handler tasks to run."""

        async def _test():
            groups = OrderedDict()

            async def add_to_groups(name):
                if 0 not in groups:
                    groups[0] = []
                groups[0].append(name)

            loop = asyncio.get_running_loop()
            loop.create_task(add_to_groups("start_handler"))
            loop.create_task(add_to_groups("help_handler"))
            await asyncio.sleep(0)  # yield so tasks run
            assert "start_handler" in groups[0]
            assert "help_handler" in groups[0]

        _run_coroutine(_test())

    def test_add_handler_on_wrong_loop_does_not_register(self):
        """Without the loop patch, tasks on a different loop are never executed
        on the current loop."""
        other_loop = asyncio.new_event_loop()
        groups = OrderedDict()

        async def add_to_groups(name):
            if 0 not in groups:
                groups[0] = []
            groups[0].append(name)

        async def _test():
            # Simulate add_handler using a DIFFERENT loop
            other_loop.create_task(add_to_groups("start_handler"))
            await asyncio.sleep(0)
            # Handlers are NOT in groups because other_loop isn't running
            assert len(groups) == 0

        try:
            _run_coroutine(_test())
        finally:
            other_loop.close()
