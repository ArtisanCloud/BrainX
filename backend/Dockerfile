# 定义 Python 版本变量
ARG PYTHON_IMAGE
ARG PYTHON_VERSION


# 第一阶段：使用指定 Python 版本的 slim 镜像作为构建器
FROM ${PYTHON_IMAGE}:${PYTHON_VERSION} AS builder

# 切换到 root 用户以进行安装
USER root

# 设置工作目录为 /app
WORKDIR /app

# 更新 apt 软件包列表并安装必要的依赖工具库
RUN apt-get update && apt-get install -y gcc python3-dev libpq-dev python3-tk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# 安装 Poetry
# RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN pip install poetry==1.8.2

COPY . /app/.
RUN echo "This is a test file" > tests.txt

# # 安装项目依赖项
RUN poetry install --only main

# 运行 PyInstaller 来构建应用程序
# RUN poetry run pyinstaller server.py --clean -y
RUN poetry run pyinstaller server.spec -y

# CMD ["tail", "-f", "/dev/null"]

# 第二阶段：使用指定 Python 版本的 slim 镜像作为运行环境
FROM ${PYTHON_IMAGE}:${PYTHON_VERSION} AS runner


# 设置工作目录为 /app
WORKDIR /app

# RUN apt-get update && apt-get install -y curl iputils-ping make
RUN apt-get update && \
    apt-get install -y curl iputils-ping make && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# 从构建器镜像中复制构建好的应用程序到当前镜像中
COPY --from=builder /app/dist /app/dist

# 赋予应用程序可执行权限
RUN chmod +x /app/dist/server/server



# 设置代理服务器并安装 NLTK 及其依赖包
ARG HOST_PROXY
ENV http_proxy=${HOST_PROXY}
ENV https_proxy=${HOST_PROXY}
RUN pip install nltk && \
    python -m nltk.downloader \
    -d /app/dist/server/_internal/llama_index/core/_static/nltk_cache \
    stopwords punkt
# 清除代理设置
ENV http_proxy=''
ENV https_proxy=''

# 暴露应用程序使用的端口
EXPOSE 8000 

# 定义容器启动时执行的默认命令
# CMD ["tail", "-f", "/dev/null"]
# CMD ["./dist/server/server"]
CMD ["make", "-f", "/app/Makefile","-C", "/app", "app-init"]


