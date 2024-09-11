import os

from app.core.rag.ingestion.extractor.drivers.word_doc.doc import DocDataExtractor


def test_extract_doc():
    # 获取当前文件所在目录的路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建文档的绝对路径
    doc_path = os.path.join(current_dir, "m102_driver_v3.docx")

    # 创建 DocDataExtractor 实例
    extractor = DocDataExtractor(file_input=doc_path)

    # 调用 extract 方法
    blocks = extractor.extract()

    # 进行测试断言
    assert isinstance(blocks, list), "Blocks should be a list"
    assert len(blocks) == 15, "Blocks should not be empty"
