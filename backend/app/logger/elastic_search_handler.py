import logging

class ElasticSearchHandler(logging.Handler):
    """自定义日志处理器，将日志发送到 Elasticsearch"""

    def __init__(self, es_client, index="brianx_logs"):
        super().__init__()
        self.es_client = es_client
        self.index = index

    def emit(self, record):
        try:
            log_entry = self.format(record)
            document = {
                "@timestamp": record.created,
                "message": log_entry,
                "level": record.levelname,
                "logger": record.name,
                "module": record.module,
                "funcName": record.funcName,
                "lineNo": record.lineno,
            }
            self.es_client.index(index=self.index, document=document)
        except Exception as e:
            print(f"Error while sending log to Elasticsearch: {e}")

