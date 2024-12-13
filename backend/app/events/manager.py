from concurrent.futures import ThreadPoolExecutor
import time

import pika
import asyncio
from typing import Any

from app.config.config import settings
from app.events.demo.callback import callback
from app.events.publisher import EventPublisher
from app.events.consumer import EventConsumer
from app.logger import logger


class EventManager:
    _instance = None
    """管理多个队列的事件发布和多个消费者实例"""
    host: str = settings.event.host
    port: str = settings.event.port
    user: str = settings.event.user
    password: str = settings.event.password

    # 存储每个队列的发布者实例
    publishers: dict[str, EventPublisher] = {}
    # 存储每个队列的消费者列表
    consumers: dict[str, list[EventConsumer]] = {}
    # 存储每个队列的消费者任务
    consumer_tasks: dict[str, list[asyncio.Task]] = {}

    def __init__(self):
        self.consumer_tasks = {}

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EventManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.host = kwargs.get("host", settings.event.host)
            cls._instance.port = kwargs.get("port", settings.event.port)
            cls._instance.user = kwargs.get("user", settings.event.user)
            cls._instance.password = kwargs.get("password", settings.event.password)
            cls._instance.retry_attempts = kwargs.get("retry_attempts", 5)
            cls._instance.retry_delay = kwargs.get("retry_delay", 5)    
            cls._instance.publishers: dict[str, EventPublisher] = {}
            cls._instance.consumers: dict[str, list[EventConsumer]] = {}
            
            

            for queue in kwargs.get("queues", [settings.event.default_event_queue]):
                try:
                    # 按照队列名字，初始化发布者
                    cls._instance.publishers[queue] = EventPublisher(
                        queue=queue,
                    )
                    subscribers = []
                    cls._instance.consumers[queue] = subscribers
                except Exception as e:
                    logger.error(f"Failed to initialize queue {queue}: {e}")

        return cls._instance

    def add_consumer(self, queue: str, consumer: EventConsumer):
        """添加消费者到特定队列的管理器"""
        try:
            if queue not in self.consumers:
                self.consumers[queue] = []
            self.consumers[queue].append(consumer)
            # logger.info(f"Consumer added to queue {queue}: {consumer}")

            if queue not in self.consumer_tasks:
                self.consumer_tasks[queue] = []

        except Exception as e:
            logger.error(f"Failed to add consumer to queue {queue}: {e}")

    async def start_consumer(
        self, queue: str, consumer: EventConsumer, callback: Any | None = None
    ):
        """启动单个消费者的消息处理"""
        loop = asyncio.get_running_loop()
        try:
            task = loop.run_in_executor(None, consumer.start_consuming, callback)
            self.consumer_tasks[queue].append(task)
            logger.info(f"Task started consumer for queue: {queue}")
        except Exception as e:
            logger.error(f"Failed to start consumer for queue '{queue}': {e}")

    async def add_and_start_consumer(
        self, queue: str, consumer: EventConsumer, callback: Any | None = None
    ):
        """动态添加消费者并启动"""
        self.add_consumer(queue, consumer)

        await self.start_consumer(queue, consumer, callback)

    async def stop_consumer(self, queue: str):
        """停止特定队列的所有消费者任务"""
        if queue not in self.consumer_tasks:
            logger.warning(f"No active tasks for queue: {queue}")
            return

        for task in self.consumer_tasks[queue]:
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    logger.info(f"Task for queue '{queue}' has been cancelled")
        self.consumer_tasks[queue] = []
        logger.info(f"All consumers stopped for queue: {queue}")

    async def shutdown_all(self):
        try:
            """停止所有队列的消费者任务"""
            for queue in self.consumer_tasks.keys():
                await self.stop_consumer(queue)
        except Exception as e:
            logger.error(f"停止消费者任务异常：{e}")

        

    async def publish_event(self, queue: str, event: dict):
        """通过特定队列的发布者发布事件"""
        if queue not in self.publishers:
            logger.error(f"No publisher for queue: {queue}")
            return

        try:
            # print(self.publishers[queue])
            await self.publishers[queue].publish_event(event)
            # logger.info(f"Event published to queue {queue}: {event}")
        except Exception as e:
            logger.error(f"Failed to publish event to queue {queue}: {e}")

    


# 全局变量event_manager，表示事件管理器的引用
event_manager: EventManager | None = None
event_manager = EventManager.get_instance()


async def add_new_consumer(queue_name: str, callback: Any|None = None):
    """添加一个新的消费者任务"""
    global event_manager
    consumer = EventConsumer(
        queue=queue_name,
    )
    await event_manager.add_and_start_consumer(queue_name, consumer, callback)

async def stop_queue(queue_name: str):
    global event_manager
    await event_manager.stop_consumer(queue_name)
    
# 在应用启动时触发的事件
async def startup_events():
    # Global变量event_manager，防止重复创建
    global event_manager
    # print("event_manager:", event_manager)

    # 添加并启动 default_queue 的消费者
    default_queue = settings.event.default_event_queue
    
    await add_new_consumer(default_queue, callback)

    # 添加并启动其他队列的消费者
    for queue in settings.event.queues:
        await add_new_consumer(queue.name, callback)


async def shutdown_events():
    await event_manager.shutdown_all()
    logger.info("Shutting down Event Manager")
