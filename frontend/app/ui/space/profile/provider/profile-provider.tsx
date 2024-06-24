"use client";


import React, {createContext, useState} from 'react';

export interface ProfileContextType {
	showProfile: Boolean;
	setShowProfile: React.Dispatch<React.SetStateAction<Boolean>>;
}


// 创建上下文对象
export const ProfileContext = createContext<ProfileContextType | null>(null)


// 创建上下文的 Provider 组件
export const ProfileProvider: React.FC<{ children: React.ReactNode }> = ({children}) => {
	// 定义共享状态
	const [showProfile, setShowProfile] = useState<Boolean>(true);

	return (
		<ProfileContext.Provider value={{showProfile, setShowProfile}}>
				{children}
		</ProfileContext.Provider>

	);
};
export default ProfileProvider;