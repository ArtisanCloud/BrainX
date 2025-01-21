"use client";


import React, {createContext, useState} from 'react';
import {baidu_ernie_lite_8k} from "@/app/config/llm";

export interface SelectLLMContextType {
	selectedLlm: string | null | undefined;
	setSelectedLlm: React.Dispatch<React.SetStateAction<string | null | undefined>>;

}


// 创建上下文对象
export const SelectLLMContext = createContext<SelectLLMContextType | null>({} as SelectLLMContextType);

// 创建上下文的 Provider 组件
export const SelectLLMProvider: React.FC<{ children: React.ReactNode }> = ({children}) => {
	// 定义共享状态
	const [selectedLlm, setSelectedLlm] = useState<string | null>(baidu_ernie_lite_8k);

	return (
		<SelectLLMContext.Provider
			value={{
				selectedLlm,
				setSelectedLlm

			} as SelectLLMContextType}>
			{children}
		</SelectLLMContext.Provider>
	);
};
export default SelectLLMProvider;
