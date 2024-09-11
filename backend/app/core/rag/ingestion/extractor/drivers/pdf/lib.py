from fitz import Rect

from app.core.rag.ingestion.extractor.base import Block


def create_block(start, end, block_id, text=None, image=None, table=None, bbox: Rect = None,
                 page_number=None) -> Block | None:
    # 确保 text 不是 None
    if text is None:
        text = ""

    return Block(
        start=start,
        end=end,
        text=text,
        image=image,
        table=table,
        bbox=bbox,
        page_number=page_number,
        block_id=block_id,
    )


def merge_bboxes(
        bbox1: Rect,
        bbox2: Rect) -> Rect:
    """
    合并两个边界框。

    参数:
    bbox1 (Rect): 第一个边界框。
    bbox2 (Rect): 第二个边界框。

    返回:
    merged_bbox (list): 合并后的边界框。
    """
    if not bbox1:
        return bbox2
    if not bbox2:
        return bbox1
    x0 = min(bbox1.x0, bbox2.x0)
    y0 = min(bbox1.y0, bbox2.y0)
    x1 = max(bbox1.x1, bbox2.x1)
    y1 = max(bbox1.y1, bbox2.y1)
    return Rect(x0=x0, y0=y0, x1=x1, y1=y1)


# 定义一个比较函数，首先比较页面号，然后比较 bbox 的 Y 坐标
def compare_block(item: Block):
    return item.page_number, item.rect[1]


def bbox_to_rect(bbox):
    # 假设 bbox 是 [x0, y0, x1, y1]
    return Rect(bbox[0], bbox[1], bbox[2], bbox[3])


def rect_to_bbox(rect: Rect) -> list:
    # 假设 Rect 对象的坐标顺序是 [x0, y0, x1, y1]
    return [rect.x0, rect.y0, rect.x1, rect.y1]
