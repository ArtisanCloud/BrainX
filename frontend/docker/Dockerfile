ARG NODE_VERSION=22.14-alpine3.21

# 第一阶段：构建阶段
FROM node:${NODE_VERSION} AS builder

# 设置工作目录
WORKDIR /app

COPY . /app

RUN apk add python3 make gcc g++

# 执行 Next.js 的静态资源编译
RUN npm ci && npm run build:docker

# 第二阶段：运行阶段
FROM node:${NODE_VERSION} AS runner

# 设置工作目录
WORKDIR /app

ENV NODE_ENV=production

# # 切换到 root 用户
USER node

COPY --from=builder /app/.next /app/.next
COPY --from=builder /app/node_modules /app/node_modules
COPY --from=builder /app/package.json /app/package.json
COPY --from=builder /app/public /app/public
COPY --from=builder /app/docker/.env.docker /app/docker/.env.docker

# 暴露 3000 端口
EXPOSE 3000

# 启动 Next.js 应用
CMD ["npm", "run", "start:docker"]

#CMD ["/bin/sh"]
