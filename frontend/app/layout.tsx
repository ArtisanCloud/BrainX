import "@/app/styles/globals.scss";
import { inter } from "@/app/styles/fonts";
import { AntdRegistry } from "@ant-design/nextjs-registry";
import { HeroUIProvider } from "@heroui/react";
import { NotificationProvider } from "./components/notification";
import GlobalLoader from "./components/global-loading"; // 导入 GlobalLoader 组件
import { metadata } from "./meta"; // 导入 metadata
import "@/i18n";
import GlobalPanel from "@/app/components/global-panel";

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${inter.className} antialiased`}>
        <AntdRegistry>
          <NotificationProvider>
            {" "}
            {/* 全局 context holder */}
            <HeroUIProvider>
              <GlobalLoader />{" "}
              {/* 根据 loading 状态决定是否显示 GlobalLoader */}
              {children}
              <GlobalPanel />
            </HeroUIProvider>
          </NotificationProvider>
        </AntdRegistry>
        ,
      </body>
    </html>
  );
}
