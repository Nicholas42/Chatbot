from asyncio import create_task, sleep
from datetime import timedelta, datetime


class AsyncScheduler:
    def __init__(self, timeout, callback):
        self.timeout = None
        self._set_timeout(timeout)
        self.callback = callback
        self.task = None

    def _set_timeout(self, new_timeout=None):
        if isinstance(new_timeout, datetime):
            new_timeout = new_timeout - datetime.now()
        if isinstance(new_timeout, timedelta):
            new_timeout = new_timeout.seconds

        if new_timeout is not None and new_timeout < 0:
            new_timeout = None

        self.timeout = new_timeout

    def run(self):
        if self.timeout is not None:
            self.task = create_task(self.wait())

    async def wait(self):
        await sleep(self.timeout)
        return self.callback()

    def reset(self, new_timeout=None):
        if self.task is not None:
            self.cancel()
        self._set_timeout(new_timeout)
        self.run()

    def cancel(self):
        self.task.cancel()
        self.task = None
