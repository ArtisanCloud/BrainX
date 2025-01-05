import sys

from app.logger.log import clean_old_logs


# 执行脚本参考：
# PYTHONPATH=./ python app/scripts/clean_logs.py logs 90

if __name__ == "__main__":
    log_directory = sys.argv[1]  # 从命令行参数获取日志目录
    days_to_keep = int(sys.argv[2])  # 从命令行参数获取保留天数
    clean_old_logs(log_directory, days_to_keep)