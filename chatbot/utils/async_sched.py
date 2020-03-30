from asyncio import create_task, sleep


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

    def reset(self, new_timeout=None):
        if self.task is not None:
            self.cancel()
        if new_timeout is not None:
            self.timeout = new_timeout
        self.run()

    def cancel(self):
        self.task.cancel()
