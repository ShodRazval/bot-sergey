import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def remind():
    print('Иди нахуй, сука')


# def init_tasks():
#     scheduler = AsyncIOScheduler()
#     scheduler.add_job(job, "interval", seconds=3)
#
#     scheduler.start()
#
#     asyncio.get_event_loop().run_forever()
