"use client";


import React, {createContext, useState} from 'react';
import {App} from "@/app/api/app";
import {Conversation} from "@/app/api/robot-chat/conversation";

export interface AppContextType {
	selectedApp: App | null | undefined;
	setSelectedApp: React.Dispatch<React.SetStateAction<App | null | undefined>>;
	currentAppConversations: Conversation[] | null | undefined;
	setCurrentAppConversations: React.Dispatch<React.SetStateAction<Conversation[] | null | undefined>>;
	currentConversation: Conversation;
	setCurrentConversation: React.Dispatch<React.SetStateAction<Conversation>>;
	isCurrentAppBusy: Boolean | null | undefined;
	setIsCurrentAppBusy: React.Dispatch<React.SetStateAction<Boolean>>;
}

export interface RobotChatUIContextType {
	showChatSidebar: Boolean;
	setShowChatSidebar: React.Dispatch<React.SetStateAction<Boolean>>;
}


export const welcomeConversation: Conversation = {
	currentPrompt: '',
	items: [
		{question: '', answer: '您好，请问有什么可以帮助到您？'},
	],
}


// 创建上下文对象
export const SelectedAppContext = createContext<AppContextType | null>(null)

export const RobotChatUIContext = createContext<RobotChatUIContextType | null>(null)


// 创建上下文的 Provider 组件
export const ChatBotProvider: React.FC<{
	children: React.ReactNode
}> = ({children}) => {
	// 定义共享状态
	const [currentLLM, setCurrentLLM] = useState(null);
	const [selectedApp, setSelectedApp] = useState<App | null>();


	const [currentAppConversations, setCurrentAppConversations] = useState<Conversation[] | null>();
	const [currentConversation, setCurrentConversation] = useState<Conversation>(welcomeConversation);
	const [isCurrentAppBusy, setIsCurrentAppBusy] = useState<Boolean>(false);

	const [showChatSidebar, setShowChatSidebar] = useState<Boolean>(true);

	return (
		<RobotChatUIContext.Provider value={{showChatSidebar, setShowChatSidebar}}>
			<SelectedAppContext.Provider value={{
				selectedApp, setSelectedApp,
				currentAppConversations, setCurrentAppConversations,
				currentConversation, setCurrentConversation,
				isCurrentAppBusy, setIsCurrentAppBusy,
			}}>
				{children}
			</SelectedAppContext.Provider>
		</RobotChatUIContext.Provider>

	);
};
export default ChatBotProvider;
