This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Main Structure

目录参考结构: https://nextjs.org/learn/dashboard-app/getting-started


834 / 5,000
翻译结果
翻译结果
* /app：包含应用程序的所有路由、组件和逻辑，这是您主要工作的地方。
* /app/utils：包含应用程序中使用的函数，例如可重用的实用函数和数据获取函数。
* /app/styles：包含应用程序的所有通用样式。
* /app/components：包含应用程序的所有 UI 组件，例如卡片、表格和表单。 为了节省时间，我们为您预先设计了这些组件的样式。
* /public：包含应用程序的所有静态资源，例如图像。
* /scripts：包含一个播种脚本，您将在后面的章节中使用它来填充数据库。
* 配置文件：您还会注意到应用程序根目录下的配置文件，例如 next.config.mjs。 大多数这些文件是在您使用 create-next-app 启动新项目时创建和预配置的。 在本课程中您不需要修改它们。