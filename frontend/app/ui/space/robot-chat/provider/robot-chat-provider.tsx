"use client";


import React, {createContext, useState} from 'react';
import {App} from "@/app/api/robot-chat/app";

export interface AppContextType {
	selectedApp: App | null | undefined;
	setSelectedApp: React.Dispatch<React.SetStateAction<App | null | undefined>>;
}

export interface RobotChatUIContextType {
	showChatSidebar: Boolean;
	setShowChatSidebar: React.Dispatch<React.SetStateAction<Boolean>>;
}


// 创建上下文对象
export const CurrentLLMContext: React.Context<any> = createContext(null);
export const SelectedAppContext = createContext<AppContextType | null>(null)
export const CurrentConversationContext: React.Context<any> = createContext(null);

export const RobotChatUIContext = createContext<RobotChatUIContextType | null>(null)


// 创建上下文的 Provider 组件
export const ChatBotProvider: React.FC<{ children: React.ReactNode }> = ({children}) => {
	// 定义共享状态
	const [currentLLM, setCurrentLLM] = useState(null);
	const [selectedApp, setSelectedApp] = useState<App | null>();


	const [currentConversation, setCurrentConversation] = useState(null);

	const [showChatSidebar, setShowChatSidebar] = useState<Boolean>(true);

	return (
		<RobotChatUIContext.Provider value={{showChatSidebar, setShowChatSidebar}}>
			<SelectedAppContext.Provider value={{selectedApp, setSelectedApp}}>
				{children}
			</SelectedAppContext.Provider>
		</RobotChatUIContext.Provider>

	);
};
export default ChatBotProvider;
