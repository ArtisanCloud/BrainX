# 使用指定 Python 版本的 slim 镜像作为运行环境
FROM python:3.12-slim AS runner

# 设置工作目录为 /app
WORKDIR /app

# 更新 apt 软件包列表并安装必要的依赖工具库
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    iputils-ping \
    make \
    gcc \
    python3-dev \
    libpq-dev \
    python3-tk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 复制项目文件到工作目录
COPY . /app/

# 安装 Poetry
RUN pip install poetry==1.8.2

## 安装项目依赖项
RUN poetry cache clear --all pypi && \
    poetry install --no-dev

# 安装 NLTK
RUN pip install nltk

# 执行下载脚本，确保 NLTK 数据被正确下载
RUN python /app/docker/scripts/download_nltk_data.py

ENTRYPOINT ["poetry", "run"]

# 使用指定 Python 版本的 slim 镜像作为运行环境
FROM python:3.12-slim AS runner

# 设置工作目录为 /app
WORKDIR /app

# 更新 apt 软件包列表并安装必要的依赖工具库
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    iputils-ping \
    make \
    gcc \
    python3-dev \
    libpq-dev \
    python3-tk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 复制项目文件到工作目录
COPY . /app/

# 安装 Poetry
RUN pip install poetry==1.8.2

## 安装项目依赖项
RUN poetry cache clear --all pypi && \
    poetry install --no-dev

# 安装 NLTK
RUN pip install nltk

# 执行下载脚本，确保 NLTK 数据被正确下载
RUN python /app/docker/scripts/download_nltk_data.py

ENTRYPOINT ["poetry", "run"]

