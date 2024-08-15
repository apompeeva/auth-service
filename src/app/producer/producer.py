from aiokafka import AIOKafkaProducer
import asyncio
from app.config import KAFKA_BOOTSTRAP_SERVERS, PRODUCE_TOPIC
import brotli

event_loop = asyncio.get_event_loop()  # ???
file_encoding = "utf-8"
file_compression_quality = 1


class Producer(object):
    def __init__(self):
        self.__producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            loop=event_loop,
        )
        self.__produce_topic = PRODUCE_TOPIC

    async def start(self) -> None:
        await self.__producer.start()

    async def stop(self) -> None:
        await self.__producer.stop()

    async def compress(self, message: str) -> bytes:
        """Compress message before sending to Kafka."""

        return brotli.compress(
            bytes(message, file_encoding),
            quality=file_compression_quality,
        )

    async def haelth_check(self) -> bool:
        """Checks if Kafka is available by fetching all metadata from the Kafka client."""
        try:
            await self.__producer.client.fetch_all_metadata()
        except Exception as exc:
            pass  # logging.error(f'Kafka is not available: {exc}')
        else:
            return True
        return False

    async def send_and_wait(self, message: str) -> None:
        await self.__producer.send_and_wait(
            topic=self.__produce_topic,
            value=self.compress(message),
        )


def get_producer() -> Producer:
    return Producer()


producer = get_producer()
