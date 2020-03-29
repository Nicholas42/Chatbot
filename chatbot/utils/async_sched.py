from asyncio import create_task, sleep, CancelledError


class AsyncScheduler:
    def __init__(self, timeout, callback):
        self.timeout = timeout
        self.callback = callback
        self.task = None

    def run(self):
        self.task = create_task(self.wait())

    async def wait(self):
        await sleep(self.timeout)
        return self.callback()

    async def reset(self, new_timeout=None):
        if self.task is not None:
            await self.cancel()
        if new_timeout is not None:
            self.timeout = new_timeout
        self.run()

    async def cancel(self):
        self.task.cancel()
        try:
            return await self.task()
        except CancelledError:
            pass
