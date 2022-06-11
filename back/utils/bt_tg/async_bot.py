import asyncio


async def run_each_1sec(counter):
    while True:
        counter += 1
        yield counter
