from typing import Any, Tuple
import pika
import json
import time
from app.config.config import settings
from pika import BasicProperties, DeliveryMode
from pika.channel import Channel
from pika.exceptions import AMQPConnectionError, ConnectionClosed
from app.logger import logger


class EventConsumer:
    def __init__(
        self,
        queue: str = settings.event.default_event_queue,
        retry_attempts: int = 5,
        retry_delay: int = 5,
    ):
        self.queue = queue
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay  # 重试间隔，单位为秒

    def get_event_channel(self) -> Tuple[Channel | None, Any]:
        """建立与 RabbitMQ 的连接和频道，支持重试"""
        attempt = 0
        while attempt < self.retry_attempts:
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=settings.event.host,
                        port=settings.event.port,
                        credentials=pika.PlainCredentials(
                            username=settings.event.user,
                            password=settings.event.password,
                        ),
                    )
                )
                channel = connection.channel()
                channel.queue_declare(queue=self.queue, durable=True)
                return channel, connection
            except AMQPConnectionError as e:
                attempt += 1
                logger.warning(
                    f"RabbitMQ连接异常，重试 {attempt}/{self.retry_attempts}：{e}"
                )
                time.sleep(self.retry_delay)  # 等待一段时间再重试
        # 如果超过最大重试次数，抛出异常
        logger.error(f"无法连接到 RabbitMQ，已重试 {self.retry_attempts} 次")
        raise Exception("RabbitMQ连接失败")

    @staticmethod
    def callback(
        ch: Channel,
        method: DeliveryMode,
        properties: BasicProperties,
        body: str | bytes,
    ):
        """处理接收到的消息"""
        # logger.info(f"Received message: {body}")
        # logger.info(f"channel is : {ch}")
        # logger.info(f"method is: {method}")
        # logger.info(f"properties are: {properties}")
        # logger.info(f"Received message: {body}")

        # 模拟处理任务，根据消息中的点号数量休眠相应的时间
        # time.sleep(body.count(b"."))
        body.decode("utf-8")
        logger.info(
            f"Received channel number: {ch.channel_number} decoded message: {body}"
        )
        try:
            # 消息反序列化
            event = json.loads(body)
            start_time = time.time()
            end_time = time.time()

            # 处理事件逻辑
            logger.info(f"Received event: {event}")
            logger.info(f"Time taken to process: {end_time - start_time:.2f} seconds")

            # 确认消息已处理
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"消息解析异常：{e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

        except Exception as e:
            logger.error(f"处理消息时发生异常：{e}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self, callback: Any | None = None):
        # print("callback:", callback)
        """开始消费消息"""
        connection = None
        channel = None
        try:
            # 获取连接和频道
            channel, connection = self.get_event_channel()

            # 设置消费队列
            if callback is None:
                callback = self.callback
            channel.basic_consume(queue=self.queue, on_message_callback=callback)

            logger.info(
                f"Waiting for queue '{self.queue}' events. To exit press CTRL+C"
            )
            channel.start_consuming()
        except AMQPConnectionError as e:
            logger.error(f"连接到RabbitMQ时发生致命错误：{e}")
        except Exception as e:
            logger.error(f"消费消息时发生意外错误：{e}")
        finally:
            # 清理资源
            self.close_connection(channel, connection)

    @classmethod
    def close_connection(cls, channel, connection):
        """关闭连接和频道"""
        if channel and not channel.is_closed:
            try:
                channel.close()
            except Exception as e:
                logger.error(f"关闭频道时发生异常：{e}")
        if connection and not connection.is_closed:
            try:
                connection.close()
            except Exception as e:
                logger.error(f"关闭 RabbitMQ 连接异常：{e}")
