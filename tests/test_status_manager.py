import time
from proxy.status_manager import StatusManager
import pytest
import asyncio


def test_uptime():
    manager = StatusManager()
    time.sleep(2)
    assert manager.uptime == "0d 0h 0m 2s"


@pytest.mark.asyncio
async def test_request_increment():
    manager = StatusManager()

    class DummyClass:
        status_manager = manager

        @StatusManager.increment_request
        async def dummy_coro(self):
            return "Hello"

    dummy = DummyClass()

    assert manager.request_count == 0
    await dummy.dummy_coro()
    assert manager.request_count == 1


def test_get_status():
    manager = StatusManager()
    status = manager.get_status()
    assert "uptime" in status
    assert "processed_requests" in status
