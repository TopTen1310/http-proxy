from functools import wraps
from aiohttp import web
from datetime import datetime, timedelta
from typing import Dict, Union


class StatusManager:
    def __init__(self):
        self.start_time = datetime.utcnow()
        self.request_count = 0

    @classmethod
    def increment_request(cls, coro):
        @wraps(coro)
        async def wrapper(self, *args, **kwargs):  # note that 'self' is added
            self.status_manager.request_count += 1
            return await coro(self, *args, **kwargs)
        return wrapper

    @property
    def uptime(self) -> str:
        """
        Returns the uptime of the server as a formatted string.
        """
        delta: timedelta = datetime.utcnow() - self.start_time
        days, remainder = divmod(delta.seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{days}d {hours}h {minutes}m {seconds}s"

    def get_status(self) -> Dict[str, Union[str, int]]:
        """
        Retrieves the status of the server, including uptime and processed requests count.

        Returns:
            dict: A dictionary containing the server's uptime and processed requests count.
        """
        return {
            "uptime": self.uptime,
            "processed_requests": self.request_count
        }
