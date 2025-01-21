"use client";


import React, {createContext, useState} from 'react';
import {App} from "@/app/api/app";

export interface QuestionAnswerContextType {
	selectedQAMode: number | null | undefined;
	setSelectedQAMode: React.Dispatch<React.SetStateAction<number | null | undefined>>;
	selectedCurrentQA: string | null | undefined;
	setSelectedCurrentQA: React.Dispatch<React.SetStateAction<string | null | undefined>>;

}


// 创建上下文对象
export const QuestionAnswerContext = createContext<QuestionAnswerContextType | null>(null)

// 创建上下文的 Provider 组件
export const QuestionAnswerProvider: React.FC<{ children: React.ReactNode }> = ({children}) => {
	// 定义共享状态
	const [selectedQAMode, setSelectedQAMode] = useState<number | null>();
	const [selectedCurrentQA, setSelectedCurrentQA] = useState<string | null>();
	const [showQAProfile, setShowQAProfile] = useState<Boolean>(true);


	return (
		<QuestionAnswerContext.Provider
			value={{selectedQAMode, setSelectedQAMode, selectedCurrentQA, setSelectedCurrentQA}}>
			{children}
		</QuestionAnswerContext.Provider>

	);
};
export default QuestionAnswerProvider;
