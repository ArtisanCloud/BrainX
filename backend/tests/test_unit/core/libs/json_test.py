import pytest

from app.core.libs.json import sanitize_json


def test_valid_json():
    content = '''
    {
        "key1": "value1",
        "key2": 123
    }
    '''
    result = sanitize_json(content)
    expected = '{"key1":"value1","key2":123}'
    assert result == expected


def test_json_with_trailing_comma():
    content = '''
    {
        "key1": "value1",
        "key2": 123,
    }
    '''
    result = sanitize_json(content)
    expected = '{"key1":"value1","key2":123}'
    assert result == expected


def test_json_with_comments():
    content = '''
    {
        "key1": "value1",  // 注释内容
        "key2": 123 /* 块注释 */
    }
    '''
    result = sanitize_json(content)
    expected = '{"key1":"value1","key2":123}'
    assert result == expected


def test_json_with_code_block_format():
    content = '''
    ```json
    {
        "key1": "value1",
        "key2": 123
    }
    ```
    '''
    result = sanitize_json(content)
    expected = '{"key1":"value1","key2":123}'
    assert result == expected


def test_invalid_json():
    content = '''
    {
        "key1": "value1",
        "key2": 123,
    }
    '''
    result = sanitize_json(content)
    assert isinstance(result, str)  # 确保返回的是字符串
    assert result == '{"key1":"value1","key2":123}'


def test_dict_input():
    content = {"key1": "value1", "key2": 123}
    result = sanitize_json(content)
    expected = '{"key1":"value1","key2":123}'
    assert result == expected


def test_json_with_code_block_comments():
    json_content = '''```json
    {
        "key": "value", // 这是一个注释
        "arr": [1, 2, 3, /* 这是一个多行注释 */]
    }
    ```'''
    result = sanitize_json(json_content)
    expected = '{"key":"value","arr":[1,2,3]}'
    assert result == expected



def test_sanitize_json_with_json_block():
    content = "```json {\"name\": \"John\", \"age\": 30, \"city\": \"New York\"} ```"
    
    # 调用函数
    result = sanitize_json(content)
    
    # 期望结果为合法的JSON字符串
    expected = '{"name":"John","age":30,"city":"New York"}'
    
    # 验证结果
    assert result == expected, f"Test failed: {result}"
    
    print("Test 1 passed: handle '''json{}''' correctly.")


def test_sanitize_json_with_plain_json_block():
    content = """{
    "title": "VMI - Consignment 物流协议",
    "requirement_list": [
        {
            "id": "001",
            "content": "供应商应负责管理库存，确保合同产品的及时交付",
            "content_en": "The supplier shall be responsible for managing the inventory and ensuring timely delivery of contract products",
            "priority": 1,
            "category": "物流协议",
            "sub_category": "库存管理"
        }
    ]
}
"""
    
    # 调用函数
    result = sanitize_json(content)
    
    # 期望结果为合法的JSON字符串
    expected = '{"title":"VMI - Consignment 物流协议","requirement_list":[{"id":"001","content":"供应商应负责管理库存，确保合同产品的及时交付","content_en":"The supplier shall be responsible for managing the inventory and ensuring timely delivery of contract products","priority":1,"category":"物流协议","sub_category":"库存管理"}]}'

    # 验证结果
    assert result == expected, f"Test failed: {result}"
    
    print("Test passed: handle plain JSON block correctly.")


