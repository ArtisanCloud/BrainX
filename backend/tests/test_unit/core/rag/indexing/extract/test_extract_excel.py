import os

from app.core.rag.ingestion.extractor.drivers.excel.excel import ExcelDataExtractor


def test_extract_doc():
    # 获取当前文件所在目录的路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建文档的绝对路径
    doc_path = os.path.join(current_dir, "shop_func.xlsx")

    # 创建 ExcelDataExtractor 实例
    extractor = ExcelDataExtractor(file_input=doc_path)

    # 调用 extract 方法
    blocks = extractor.extract()

    # 进行测试断言
    assert isinstance(blocks, list), "Blocks should be a list"
    assert len(blocks) == 1, "Blocks should not be empty"
