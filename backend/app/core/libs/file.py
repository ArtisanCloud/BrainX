import os


def get_project_path() -> str:
    # 获取当前脚本的目录
    current_path = os.path.dirname(os.path.abspath(__file__))
    # print(current_path)
    # 向上两级目录以到达项目根目录
    project_root = os.path.abspath(os.path.join(current_path, '../..'))

    return project_root
