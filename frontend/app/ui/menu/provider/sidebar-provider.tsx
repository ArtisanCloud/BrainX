"use client";

import React, { createContext, useState, useEffect } from 'react';
import Cookies from 'js-cookie';

// 定义接口
export interface SidebarContextType {
	hideSidebar: boolean;
	setHideSidebar: React.Dispatch<React.SetStateAction<boolean>>;
}

// 创建上下文对象
export const HideSidebarContext = createContext<SidebarContextType>({} as SidebarContextType);

// 创建上下文的 Provider 组件
export const SidebarProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
	// 初始状态设置为 false，用于确保服务器端和客户端一致的渲染输出
	const [hideSidebar, setHideSidebar] = useState<boolean>(false);
	const [isLoaded, setIsLoaded] = useState<boolean>(false);

	// 使用 useEffect 在客户端环境中读取 cookie 并更新状态
	useEffect(() => {
		const hideSidebarCookie = Cookies.get('hideSidebar');
		if (hideSidebarCookie !== undefined) {
			setHideSidebar(hideSidebarCookie === 'true');
		}
		setIsLoaded(true);
	}, []);

	// 将 hideSidebar 的值保存到 cookie 中
	useEffect(() => {
		if (isLoaded) {
			Cookies.set('hideSidebar', hideSidebar.toString(), { path: '/' });
		}
	}, [hideSidebar, isLoaded]);

	if (!isLoaded) {
		// 在 cookie 值加载前，不渲染子组件
		return null;
	}

	return (
		<HideSidebarContext.Provider value={{ hideSidebar, setHideSidebar }}>
			{children}
		</HideSidebarContext.Provider>
	);
};

export default SidebarProvider;
