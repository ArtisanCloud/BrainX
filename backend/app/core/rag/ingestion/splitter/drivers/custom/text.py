import base64
import json
from typing import List
import re
import uuid


class TextSplitter:
    def __init__(self, max_length: int = 800, overlap: int = 50):
        self.max_length = max_length
        self.overlap = overlap
        self.placeholder_pattern = re.compile(r'\[(Image|Table) id=([^\s]+)(?: [^\]]+)?\]')
        self.separate = "\n\n"

    def merge_blocks_into_text(self, blocks: List[Block]) -> str:
        """
        将 Blocks 合并成一个长文本，根据需要插入换行符。

        :param blocks: List of Block objects.
        :return: Merged text.
        """
        merged_text = ""
        join = "\n"
        for block in blocks:
            if block.type == BlockType.TEXT.value:
                # 在文本块之间插入换行符
                merged_text += block.text.strip() + join
            elif block.type == BlockType.IMAGE.value:
                # 处理图片块
                placeholder_image = f"[Image id={block.block_id}]"
                merged_text += placeholder_image + join
            elif block.type == BlockType.TABLE.value:
                # 处理表格块
                placeholder_table = f"[Table id={block.block_id}]"
                merged_text += placeholder_table + join

        return merged_text

    def split_text_into_segments(self, text: str) -> List[str]:
        """
        将长文本分割成多个段落，每个段落的长度不超过 max_length 字符。
        先按照风格符进行分割，确保风格符不会被破坏，然后对每个分割后的片段进行最大长度限制。

        :param text: 长文本
        :return: 文本段落列表
        """

        # print(text)
        split_parts = text.split(self.separate)
        # print(split_parts)
        [part.strip() for part in split_parts if part.strip()]
        # print(split_parts)

        # 处理每个分割后的片段
        final_segments = []
        for part in split_parts:
            if len(part) > self.max_length:
                final_segments.extend(self.split_large_segment(part))
            else:
                final_segments.append(part.strip())

        # 这里需要添加一个重新优化过程，将极小的segment做合并处理
        # to be do

        return final_segments

    def find_last_placeholder_before(self, text: str, start: int, end: int) -> int:
        """
        查找从 start 到 end 范围内最后一个通配符的位置，并返回其结束位置。
        如果没有找到，则返回end。
        """
        last_match_end = end
        for match in self.placeholder_pattern.finditer(text, start, end):
            # print("match", match.end())
            last_match_end = match.end()

        return last_match_end

    def split_large_segment(self, segment: str) -> List[str]:
        """
        对超长的文本片段进行分割，以确保每个分段的长度不超过 max_length，
        并且在分段之间添加 overlap 的重叠部分。处理通配符以避免被分割。

        :param segment: 超长文本片段
        :return: 文本段落列表
        """
        result = []
        start = 0
        segment_length = len(segment)
        # print(segment)

        while start < segment_length:
            # 判断当前分段的结束位置，start为动态起始位置
            end = min(start + self.max_length, segment_length)
            print("~~~~~~~~~", start, end, segment_length)

            # Pro功能
            # 这里需要限制正则表达式查找范围，确保不会切断通配符
            original_end = end
            split_point = end
            # 如果当前结束位置，还未超过最后文本位置，则需要做二次切割
            if end < original_end:
                # 优先在换行符处进行分割
                split_point = segment.rfind('\n', start, end)
                if split_point == -1 or split_point <= start:
                    split_point = end
                print("split point end ", split_point)

                # 更新起始点，考虑重叠部分
                new_start = split_point - self.overlap

            # 如果当前结束位置已经达到了最后的文本位置，则不需要再切割
            else:
                new_start = split_point

            # 添加分割结果到segment
            result.append(segment[start:split_point].strip())

            # 确保 start 始终向前移动，防止死循环
            if new_start <= start:
                new_start = split_point
            start = new_start

        return result


    @staticmethod
    def get_block_by_id(blocks: List[Block], block_id: str) -> Block | None:
        """
        根据 block_id 从 blocks 列表中获取对应的 Block 对象。
        """
        for block in blocks:
            if block.block_id == block_id:
                return block
        return None

    def split(self, blocks: List[Block]) -> List[DocumentSegment]:
        """
        将 Blocks 分解成 DocumentSegment 列表。

        :param blocks: List of Block objects.
        :return: List of DocumentSegment objects.
        """
        # 先将blocks合并成一块
        str_content = self.merge_blocks_into_text(blocks)
        # print(str_content)

        # 再分割成多个段落
        segments_text_list = self.split_text_into_segments(str_content)
        print(segments_text_list)

        # 生成 DocumentSegment 列表
        document_segments = []
        for segment_text in segments_text_list:
            segment_id = str(uuid.uuid4())
            nodes = []

            # 将当前的segment的text给到node
            text_node = DocumentNode(
                node_id=str(uuid.uuid4()), node_type=BlockType.TEXT.value,
                segment_uuid=segment_id,
                content=segment_text
            )
            nodes.append(text_node)

            # 检查多媒体的占位符，需要额外生成nodes
            for match in self.placeholder_pattern.finditer(segment_text):
                # print("match: ", match)
                placeholder_type = match.group(1)
                block_id = match.group(2)
                block = self.get_block_by_id(blocks, block_id)
                node_id = str(uuid.uuid4())

                if block and placeholder_type == "Image":
                    # block.image 是二进制数据
                   pass
                elif block and placeholder_type == "Table":
                    # 处理表格，将列表数据转换为 JSON 字符串
                    pass
                else:
                    continue
                # print("node:", node.node_type, node.node_id)
                # nodes.append(node)

            document_segment = DocumentSegment(
                segment_id=segment_id,
                content=segment_text,
                nodes=nodes,
                status=1,  # 示例数据
                position=0,  # 示例数据
                page_number=1,  # 示例数据
                word_count=len(segment_text.split()),  # 示例数据
                token_count=0,  # 示例数据
                keywords="",
                hit_count=0,  # 示例数据
                index_node_id='',  # 示例数据
                index_node_hash='',  # 示例数据
                error_message=''  # 示例数据
            )
            document_segments.append(document_segment)

        return document_segments
