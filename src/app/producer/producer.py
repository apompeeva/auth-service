import logging

import brotli
from aiokafka import AIOKafkaProducer

from app.config import KAFKA_HOST, KAFKA_PORT, PRODUCE_TOPIC

file_encoding = 'utf-8'
file_compression_quality = 1


class Producer:
    """Kafka продюсер."""

    def __init__(self):
        """Инициализация продюсера."""
        self.__producer = AIOKafkaProducer(
            bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}',
        )
        self.__produce_topic = PRODUCE_TOPIC

    async def start(self) -> None:
        """Запуск продюсера."""
        await self.__producer.start()

    async def stop(self) -> None:
        """Остановка продюсера."""
        await self.__producer.stop()

    async def compress(self, message: str) -> bytes:
        """Сжатие сообщения перед отправкой в ​​Kafka."""
        return brotli.compress(
            bytes(message, file_encoding),
            quality=file_compression_quality,
        )

    async def health_check(self) -> bool:
        """Проверяет, доступен ли Kafka, получая все метаданные от клиента Kafka."""
        try:
            await self.__producer.client.fetch_all_metadata()
        except Exception as exc:
            logging.error(f'Kafka is not available: {exc}')
        else:
            return True
        return False

    async def send_and_wait(self, message: str) -> None:
        """Отправка сообщения в топик Kafka."""
        await self.__producer.send_and_wait(
            topic=self.__produce_topic,
            value=await self.compress(message),
        )


def get_producer() -> Producer:
    """Получение экземпляра класса Producer."""
    return Producer()


producer = get_producer()
