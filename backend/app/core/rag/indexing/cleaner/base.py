from abc import ABC


class Cleaner(ABC):

    @classmethod
    def clean(content: str, process_rule: dict):
        # 根据自定义规则，清除内容里的不需要内容，比如email，url等
        pass
