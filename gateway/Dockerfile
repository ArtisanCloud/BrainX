FROM nginx:latest

# Remove any existing config files
RUN rm /etc/nginx/conf.d/* 

# 拷贝构建产物到nginx容器中
COPY /nginx/nginx.conf /etc/nginx/nginx.conf



# RUN mkdir -p /var/log/nginx/server
# RUN touch /var/log/nginx/server/access.log
# RUN touch /var/log/nginx/server/error.log

# RUN mkdir -p /var/log/nginx/web
# RUN touch /var/log/nginx/web/access.log
# RUN touch /var/log/nginx/web/error.log

RUN mkdir -p /var/log/nginx/server
RUN mkdir -p /var/log/nginx/web
RUN chmod -R 777 /var/log/nginx

# 暴露80端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]
