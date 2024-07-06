# event_manager.py

from celery import Celery
from typing import Callable, Dict


class EventManager:
    def __init__(self, broker_url: str):
        self.celery_app = Celery('event_manager', broker=broker_url, backend=broker_url)
        self.callbacks: Dict[str, Callable] = {}

    def register_callback(self, event_name: str, callback: Callable):
        """注册事件回调函数"""
        self.callbacks[event_name] = callback

    def dispatch_event(self, event_name: str, *args, **kwargs):
        """触发事件并执行回调"""
        if event_name in self.callbacks:
            self.celery_app.send_task('tasks.handle_event', args=[event_name, *args], kwargs=kwargs)

    def event_completed(self, event_name: str, *args, **kwargs):
        """事件完成后的回调执行"""
        if event_name in self.callbacks:
            callback = self.callbacks[event_name]
            callback(*args, **kwargs)
