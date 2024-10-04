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
