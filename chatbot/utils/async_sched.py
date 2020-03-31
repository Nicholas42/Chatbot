from asyncio import create_task, sleep
from datetime import timedelta


class AsyncScheduler:
    def __init__(self, timeout, callback):
        self.timeout = None
        self._set_timeout(timeout)
        self.callback = callback
        self.task = None

    def _set_timeout(self, new_timeout):
        if isinstance(self.timeout, timedelta):
            new_timeout = new_timeout.seconds
        self.timeout = new_timeout

    def run(self):
        self.task = create_task(self.wait())

    async def wait(self):
        await sleep(self.timeout)
        return self.callback()

    def reset(self, new_timeout=None):
        if self.task is not None:
            self.cancel()
        if new_timeout is not None:
            self._set_timeout(new_timeout)
            self.run()

    def cancel(self):
        self.task.cancel()
        self.task = None
