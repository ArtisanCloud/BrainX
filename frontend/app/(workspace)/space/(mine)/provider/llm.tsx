"use client";

import React, { createContext, useState } from 'react';

// 如果 selectedProvider 和 selectedModel 是字符串类型（如 providerId, modelId），直接用 string；
// 若你想传整个对象，请调整类型定义
export interface SelectLLMContextType {
	selectedProvider: string | null;
	setSelectedProvider: React.Dispatch<React.SetStateAction<string | null>>;
	selectedModel: string | null;
	setSelectedModel: React.Dispatch<React.SetStateAction<string | null>>;
}

// 创建上下文对象
export const SelectLLMContext = createContext<SelectLLMContextType | null>(null);

// 创建上下文的 Provider 组件
export const SelectLLMProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
	const [selectedProvider, setSelectedProvider] = useState<string | null>(null);
	const [selectedModel, setSelectedModel] = useState<string | null>(null);

	return (
		<SelectLLMContext.Provider value={{
			selectedProvider,
			setSelectedProvider,
			selectedModel,
			setSelectedModel,
		}}>
			{children}
		</SelectLLMContext.Provider>
	);
};

export default SelectLLMProvider;
