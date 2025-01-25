from app.core.ai_model.schema.base import MultilingualField


def test_multilingual_field():
    # 测试传入只有 en_US 的情况
    data = {"en_US": "Hello"}
    field = MultilingualField(**data)
    assert field.en_US == "Hello"
    assert field.zh_CN == "Hello"  # zh_CN 应该默认为 en_US 的值

    # 测试传入 zh_CN 和 en_US 都有的情况
    data = {"en_US": "Hello", "zh_CN": "你好"}
    field = MultilingualField(**data)
    assert field.en_US == "Hello"
    assert field.zh_CN == "你好"  # zh_CN 使用传入的值

    # 测试传入没有 zh_CN 的情况，应该自动使用 en_US 的值
    data = {"en_US": "Hello", "zh_CN": None}
    field = MultilingualField(**data)
    assert field.en_US == "Hello"
    assert field.zh_CN == "Hello"  # zh_CN 应该从 en_US 继承

    print("All tests passed.")


# 运行测试
test_multilingual_field()
