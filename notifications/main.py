import asyncio
import signal


from scheduler.scheduler import NotificationScheduler


class NotificationService:

    def __init__(self):
        self.scheduler = NotificationScheduler()
        self.is_running = False

    async def startup(self):
        self.scheduler.start()
        self.is_running = True

    async def shutdown(self):
        self.scheduler.stop()
        self.is_running = False

    async def run_forever(self):
        await self.startup()
        try:
            while self.is_running:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            await self.shutdown()


async def main():
    service = NotificationService()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig,
            lambda: asyncio.create_task(service.shutdown())
        )
    try:
        await service.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        await service.shutdown()


if __name__ == "__main__":
    asyncio.run(main())