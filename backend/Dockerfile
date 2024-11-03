# 定义 Python 版本变量
ARG PYTHON_IMAGE
ARG PYTHON_VERSION

# 使用指定 Python 版本的 slim 镜像作为运行环境
FROM ${PYTHON_IMAGE}:${PYTHON_VERSION} AS runner

# 设置工作目录为 /app
WORKDIR /app

# 更新 apt 软件包列表并安装必要的依赖工具库
RUN apt-get update && apt-get install -y curl iputils-ping make gcc python3-dev libpq-dev python3-tk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 复制项目文件到工作目录
COPY . /app/

# 安装 Poetry
RUN pip install poetry==1.8.2

# 安装项目依赖项
RUN poetry install --no-dev

# 设置代理服务器并安装 NLTK 及其依赖包
#ARG HOST_PROXY
#ENV http_proxy=${HOST_PROXY}
#ENV https_proxy=${HOST_PROXY}
#RUN pip install nltk && \
#    python -m nltk.downloader -d /app/_internal/llama_index/core/_static/nltk_cache stopwords punkt
## 清除代理设置
#ENV http_proxy=''
#ENV https_proxy=''

# 暴露应用程序使用的端口
EXPOSE 8000

