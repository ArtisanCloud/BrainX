import logging
import requests
import json
import time

class LokiHandler(logging.Handler):
    def __init__(self, url, labels=None):
        super().__init__()
        self.url = url  # Loki 的推送地址
        self.labels = labels or {}  # 默认标签

    def emit(self, record):
        try:
            # 构建日志消息
            log_entry = self.format(record)
            timestamp = int(time.time() * 1e9)  # 转换为纳秒

            # 动态更新 level 标签
            labels_with_level = self.labels.copy()
            labels_with_level["level"] = record.levelname.lower()  # INFO -> info, ERROR -> error

            # 构建 Loki 的日志格式
            payload = {
                "streams": [
                    {
                        "stream": labels_with_level,
                        "values": [[str(timestamp), log_entry]],
                    }
                ]
            }

            # 发送日志到 Loki
            headers = {"Content-Type": "application/json"}
            response = requests.post(self.url, data=json.dumps(payload), headers=headers)

            # 检查响应
            if response.status_code != 204:
                print(f"Failed to send logs to Loki: {response.status_code}, {response.text}")
            
        except Exception as e:
            print(f"Error sending logs to Loki: {e}")