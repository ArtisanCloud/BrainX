import base64
import pika
import json
import time
from app.config.config import settings
from pika.exceptions import AMQPConnectionError
from app.logger import logger


class EventPublisher:
    def __init__(self,queue: str = settings.event.default_event_queue, retry_attempts: int = 5, retry_delay: int = 5):
        self.queue = queue
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay  # 重试间隔，单位为秒
        self.connection = None
        self.channel = None

    async def get_event_channel(self):
        """建立与 RabbitMQ 的连接和频道，支持重试"""
        attempt = 0
        while attempt < self.retry_attempts:
            if self.connection:
                print("self.connection:", self.connection)
                if self.connection.is_open:
                    print("self.connection.is_open:", self.connection.is_open)
                else:
                    print("self.connection is not open")
            else:
                print("self.connection is None")    

            try:
                if not self.connection or not self.connection.is_open:
                    self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                        host=settings.event.host,
                        port=settings.event.port,
                        credentials=pika.PlainCredentials(
                            username=settings.event.user,
                            password=settings.event.password
                        )
                    ))
                if not self.channel or not self.channel.is_open:
                    self.channel = self.connection.channel()
                    self.channel.queue_declare(queue=self.queue, durable=True)
                return self.channel, self.connection
            except AMQPConnectionError as e:
                attempt += 1
                logger.error(f"RabbitMQ连接异常，重试 {attempt}/{self.retry_attempts}：{e}")
                time.sleep(self.retry_delay)  # 等待一段时间再重试
        # 如果超过最大重试次数，抛出异常
        logger.critical(f"无法连接到 RabbitMQ，已重试 {self.retry_attempts} 次")
        raise Exception("RabbitMQ连接失败")

    async def publish_event(self, event: dict):
        """发布事件到队列"""
        try:
            # 获取连接和频道
            channel, connection = await self.get_event_channel()

            # 序列化事件并进行Base64编码
            message_body = json.dumps(event).encode('utf-8')

            # 发布消息到 RabbitMQ 队列
            channel.basic_publish(
                exchange='',
                routing_key=self.queue,
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # 消息持久化
                )
            )
            logger.info(f"成功发布事件: {event}")
        except Exception as e:
            logger.error(f"发布事件异常：{e}", exc_info=settings.log.exc_info)

    @classmethod
    def close_connection(cls, channel, connection):
        """关闭连接和频道"""
        if channel:
            try:
                channel.close()
            except AMQPConnectionError:
                logger.warning("关闭频道时发生连接异常")
        if connection:
            try:
                connection.close()
            except Exception as e:
                logger.error(f"关闭 RabbitMQ 连接异常：{e}")