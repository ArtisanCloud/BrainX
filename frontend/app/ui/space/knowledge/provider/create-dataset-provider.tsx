"use client";


import React, {createContext, useState} from 'react';

export interface CreateDatasetContextType {
	name: string | null | undefined;
	setName: React.Dispatch<React.SetStateAction<string | null | undefined>>;
	description: string | null | undefined;
	setDescription: React.Dispatch<React.SetStateAction<string | null | undefined>>;
	avatarUrl: string | null | undefined;
	setAvatarUrl: React.Dispatch<React.SetStateAction<string | null | undefined>>;
	persona: string | null | undefined;
	setPersona: React.Dispatch<React.SetStateAction<string | null | undefined>>;
}


// 创建上下文对象
export const CreateDatasetContext = createContext<CreateDatasetContextType | null>({} as CreateDatasetContextType);

// 创建上下文的 Provider 组件
export const CreateDatasetProvider: React.FC<{ children: React.ReactNode }> = ({children}) => {
	// 定义共享状态
	const [name, setName] = useState<string | null >();
	const [description, setDescription] = useState<string | null>();
	const [avatarUrl, setAvatarUrl] = useState<string | null>();
	const [persona, setPersona] = useState<string | null>();

	return (
		<CreateDatasetContext.Provider
			value={{
				name,
				setName,
				description,
				setDescription,
				avatarUrl,
				setAvatarUrl,
				persona,
				setPersona
			} as CreateDatasetContextType}>
			{children}
		</CreateDatasetContext.Provider>
	);
};
export default CreateDatasetProvider;
