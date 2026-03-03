import aio_pika
import json
from typing import Optional, Dict, Any
from datetime import datetime


class RabbitMQConfig:
    def __init__(
            self,
            url: str = "amqp://guest:guest@localhost/",
            queue_name: str = "reactions_queue",
            exchange_name: str = "",
            routing_key: str = "reactions_queue"
    ):
        self.url = url
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.routing_key = routing_key


class RabbitMQClient:
    def __init__(self, config: RabbitMQConfig):
        self.config = config
        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.queue: Optional[aio_pika.Queue] = None

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(self.config.url)
            self.channel = await self.connection.channel()

            self.queue = await self.channel.declare_queue(
                self.config.queue_name,
                durable=True,
                auto_delete=False
            )
        except Exception as e:
            pass

    async def publish_message(self, message_data: Dict[str, Any]) -> bool:
        if not self.channel:
            await self.connect()

        try:
            message_body = json.dumps(message_data, ensure_ascii=False, default=str)
            message = aio_pika.Message(
                body=message_body.encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                content_type="application/json",
                timestamp=datetime.now(),
                message_id=str(hash(frozenset(message_data.items())))
            )
            await self.channel.default_exchange.publish(
                message,
                routing_key=self.config.queue_name
            )
            return True
        except Exception as e:
            return False

    async def close(self):
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

# тут нужно из env подтянуть
rabbitmq_config = RabbitMQConfig(
    url="amqp://guest:guest@localhost/",
    queue_name="reactions_queue"
)
rabbitmq_client = RabbitMQClient(rabbitmq_config)
