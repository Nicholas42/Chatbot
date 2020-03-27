import asyncio

from chatbot.runner import Runner


async def main():
    r = Runner()
    await r.wait_running()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
