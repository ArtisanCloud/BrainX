from app.core.brainx.entity.base import I18nObject


def test_multilingual_field():
    # 测试传入只有 en_US 的情况
    data = {"en_US": "Hello"}
    field = I18nObject(**data)
    assert field.en_US == "Hello"
    assert field.zh_Hans == "Hello"  # zh_Hans 应该默认为 en_US 的值

    # 测试传入 zh_Hans 和 en_US 都有的情况
    data = {"en_US": "Hello", "zh_Hans": "你好"}
    field = I18nObject(**data)
    assert field.en_US == "Hello"
    assert field.zh_Hans == "你好"  # zh_Hans 使用传入的值

    # 测试传入没有 zh_Hans 的情况，应该自动使用 en_US 的值
    data = {"en_US": "Hello", "zh_Hans": None}
    field = I18nObject(**data)
    assert field.en_US == "Hello"
    assert field.zh_Hans == "Hello"  # zh_Hans 应该从 en_US 继承

    print("All tests passed.")


# 运行测试
test_multilingual_field()
