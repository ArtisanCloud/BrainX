"use client";


import React, {createContext, useState} from 'react';

export interface CreateAppContextType {
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
export const CreateAppContext = createContext<CreateAppContextType | null>({} as CreateAppContextType);

// 创建上下文的 Provider 组件
export const CreateAppProvider: React.FC<{ children: React.ReactNode }> = ({children}) => {
	// 定义共享状态
	const [name, setName] = useState<string | null >();
	const [description, setDescription] = useState<string | null>();
	const [avatarUrl, setAvatarUrl] = useState<string | null>();
	const [persona, setPersona] = useState<string | null>();

	return (
		<CreateAppContext.Provider
			value={{
				name,
				setName,
				description,
				setDescription,
				avatarUrl,
				setAvatarUrl,
				persona,
				setPersona
			} as CreateAppContextType}>
			{children}
		</CreateAppContext.Provider>
	);
};
export default CreateAppProvider;
