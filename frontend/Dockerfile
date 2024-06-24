# 定义 Python 版本变量
ARG NODE_VERSION=21.6.2

# 第一阶段
FROM node:${NODE_VERSION} AS builder


# 切换到 root 用户以进行安装
USER root

# 设置工作目录
WORKDIR /app

COPY . /app

# 安装依赖库
RUN npm i

# 执行 Next.js 的静态资源编译
RUN npm run build:docker


# 第二阶段
FROM node:${NODE_VERSION} AS runner

# 设置工作目录
WORKDIR /app

ENV NODE_ENV=production

# # 切换到 root 用户
USER root

# RUN addgroup --gid 1001 --system nodejs
# RUN adduser --system nextjs --uid 1001
# USER nextjs

COPY --from=builder /app/.next /app/.next
COPY --from=builder /app/node_modules /app/node_modules
COPY --from=builder /app/package.json /app/package.json
COPY --from=builder /app/public /app/public


# 暴露3000端口
EXPOSE 3000

# 启动nextjs
# CMD ["tail", "-f", "/dev/null"]
CMD npm start
