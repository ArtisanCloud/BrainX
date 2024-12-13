from pika import BasicProperties, DeliveryMode
from pika.channel import Channel
from pika.exceptions import AMQPConnectionError, ConnectionClosed

import json
import time
from app.logger import logger

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
            f"Demo Received channel number: {ch.channel_number} decoded message: {body}"
        )
        try:
            # 消息反序列化
            event = json.loads(body)
            start_time = time.time()
            end_time = time.time()

            # 处理事件逻辑
            logger.info(f"Demo Received event: {event}")
            logger.info(f"Demo Time taken to process: {end_time - start_time:.2f} seconds")

            # 确认消息已处理
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"消息解析异常：{e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

        except Exception as e:
            logger.error(f"处理消息时发生异常：{e}")
            ch.basic_ack(delivery_tag=method.delivery_tag)