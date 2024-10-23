"use client";

import React, { createContext, useContext, useCallback } from 'react';
import { message } from 'antd';

// 创建 NotificationContext
const NotificationContext = createContext<{
  msgSuccess: (content: string) => void;
  msgError: (content: string) => void;
  msgWarn: (content: string) => void;
} | null>(null);

// NotificationProvider 组件
const NotificationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [messageApi, contextHolder] = message.useMessage();

  // 定义通知方法
  const msgSuccess = useCallback((content: string) => {
    messageApi.open({
      type: 'success',
      content,
    });
  }, [messageApi]);

  const msgError = useCallback((content: string) => {
    messageApi.open({
      type: 'error',
      content,
    });
  }, [messageApi]);

  const msgWarn = useCallback((content: string) => {
    messageApi.open({
      type: 'warning',
      content,
    });
  }, [messageApi]);

  // 提供通知方法给整个应用
  return (
    <NotificationContext.Provider value={{ msgSuccess, msgError, msgWarn }}>
      {contextHolder}
      {children}
    </NotificationContext.Provider>
  );
};

// 自定义 hook，用于方便在任何地方使用通知
const useNotification = () => {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotification must be used within a NotificationProvider');
  }
  return context;
};

export { NotificationProvider, useNotification };
