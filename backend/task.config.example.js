module.exports = {
    apps: [
        {
            name: "brainx-web-api", // 进程名称
            script: "bash", // 指定解释器为 bash
            args: "-c 'uvicorn app.main:app --host=0.0.0.0 --port=8000'", // 执行 Uvicorn 命令
            cwd: "./", // 项目根目录
            autorestart: true, // 是否自动重启
            watch: false, // 是否监听文件变化
            max_memory_restart: "2G", // 内存超过 1G 时重启
            env: {
                PATH: "C:\\ProgramData\\Anaconda3\\envs\\brainx\\Scripts;$PATH",  // windows 确保 pm2 加载 Conda 环境路径
                // PATH: "/opt/anaconda3/envs/brainx/bin:$PATH", // 确保 pm2 加载 Conda 环境路径
                NODE_ENV: "develop", // 环境变量
            },
            max_size: '10M', // 最大日志文件大小
            log_rotate: {
                max_logs: 30,  // 保留30个日志文件
            },
            // out_file: "./logs/brainx-web-api-out.log", // 输出日志文件
            // error_file: "./logs/brainx-web-api-error.log", // 错误日志文件
        },
        {
            name: "brainx-worker-default", // 进程名称
            script: "bash", // 指定解释器为 bash
            args: "-c 'celery -A app.service.task.celery_worker worker -n brainx@worker_default --loglevel=info -P gevent'", // 执行 Celery 命令
            cwd: "./", // 项目根目录
            autorestart: true, // 是否自动重启
            watch: false, // 是否监听文件变化
            max_memory_restart: "2G", // 内存超过 1G 时重启
            env: {
                PATH: "C:\\ProgramData\\Anaconda3\\envs\\brainx\\Scripts;$PATH",  // windows 确保 pm2 加载 Conda 环境路径
                // PATH: "/opt/anaconda3/envs/brainx/bin:$PATH", // 确保 pm2 加载 Conda 环境路径
                NODE_ENV: "develop", // 环境变量
            },
            max_size: '10M', // 最大日志文件大小
            log_rotate: {
                max_logs: 30,  // 保留30个日志文件
            },
        },
        {
            name: "brainx-worker-rag", // 进程名称
            script: "bash", // 指定解释器为 bash
            args: "-c 'celery -A app.service.task.celery_worker worker -Q rag_queue -n brainx@worker_rag --loglevel=info -P gevent'", // Celery 参数
            cwd: "./", // 项目根目录
            autorestart: true, // 是否自动重启
            watch: false, // 是否监听文件变化
            max_memory_restart: "2G", // 内存超过 1G 时重启
            env: {
                PATH: "C:\\ProgramData\\Anaconda3\\envs\\brainx\\Scripts;$PATH",  // windows 确保 pm2 加载 Conda 环境路径
                // PATH: "/opt/anaconda3/envs/brainx/bin:$PATH", // linux 确保 pm2 加载 Conda 环境路径
                NODE_ENV: "production", // 环境变量
            },
            max_size: '10M', // 最大日志文件大小
            log_rotate: {
                max_logs: 30,  // 保留30个日志文件
            },
        },
    ],
};