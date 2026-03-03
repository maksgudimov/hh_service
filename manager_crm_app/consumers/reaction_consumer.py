import os
import asyncio
import signal
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path
from os import environ as environment

import aio_pika

from consumers.reaction_handler import ReactionMessageHandlerMQ
from configs import database_connection

env_path = os.path.join(Path(__file__).parent.parent.parent, ".env")
load_dotenv(override=True, dotenv_path=env_path)


class ReactionConsumerMQ:
    def __init__(
            self,
            amqp_url: str,
            queue_name: str,
            prefetch_count: int = 10
    ):
        self.amqp_url = amqp_url
        self.queue_name = queue_name
        self.prefetch_count = prefetch_count
        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.queue: Optional[aio_pika.Queue] = None
        self.consumer_tag: Optional[str] = None
        self._shutdown_event = asyncio.Event()

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(
                self.amqp_url,
                timeout=30
            )
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=self.prefetch_count)
            self.queue = await self.channel.declare_queue(
                self.queue_name,
                durable=True,
                auto_delete=False
            )
        except Exception as e:
            raise e

    async def process_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            try:
                async with database_connection.session() as session:
                    handler = ReactionMessageHandlerMQ(session)
                    success = await handler.process_message(message.body)
                    if success:
                        # автоматически message.ack()
                        pass
                    else:
                        raise Exception("failed")
            except Exception as e:
                # автоматически message.reject(requeue=True)
                pass

    async def start_consuming(self):
        """Запуск потребления сообщений"""
        if not self.queue:
            await self.connect()

        self.consumer_tag = await self.queue.consume(self.process_message)
        await self._shutdown_event.wait()

    async def stop(self):
        self._shutdown_event.set()
        if self.consumer_tag and self.queue:
            await self.queue.cancel(self.consumer_tag)
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

    async def run(self):
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(self.stop()))
        try:
            await self.start_consuming()
        except Exception as e:
            await self.stop()

RABBITMQ_URL = environment.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
QUEUE_NAME = environment.get("QUEUE_NAME", "reactions_queue")

consumer = ReactionConsumerMQ(
        amqp_url=RABBITMQ_URL,
        queue_name=QUEUE_NAME,
        prefetch_count=10
)