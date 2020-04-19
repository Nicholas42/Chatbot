import asyncio
import sys

from chatbot.runner import Runner


async def main(*args,**kwargs):
    r = Runner(*args, **kwargs)
    await r.wait_running()


if __name__ == "__main__":
    local = len(sys.argv) > 1 and sys.argv[1] == "local"
    asyncio.get_event_loop().run_until_complete(main(local=local))
