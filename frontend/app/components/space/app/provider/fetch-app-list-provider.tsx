"use client";

// AppContext.tsx
import React, {createContext, useState} from 'react';
import {RequestPagination, ResponsePagination} from "@/app/api";
import {ActionFetchAppList, App, ResponseFetchAppList} from "@/app/api/app";
import {defaultPage} from "@/app/config/constant/index";
import {appPageSize} from "@/app/components/space/app/list";

export interface FetchAppListContextType {
	appList: App[]; // 数据类型根据实际情况进行替换
	setAppList: React.Dispatch<React.SetStateAction<App[] | null | undefined>>;
	fetchAppList: (pagination: RequestPagination) => Promise<ResponseFetchAppList>;
	pagination: ResponsePagination
	setPagination: React.Dispatch<React.SetStateAction<ResponsePagination>>;
}

export const FetchAppListContext = createContext<FetchAppListContextType>({} as FetchAppListContextType);

export const FetchAppListProvider: React.FC<{ children: React.ReactNode }> = ({children}) => {
	const [appList, setAppList] = useState<any>();
	const [pagination, setPagination] = useState<ResponsePagination>({
		page: defaultPage,
		per_page: appPageSize,
		sort: false,
		total_rows: 0,
		total_pages: 0,
	});

	const fetchAppList = async (pagination: RequestPagination) => {
		// console.log(pagination.page, pagination.page_size)
		const res = await ActionFetchAppList(pagination);
		// console.log(res)
		return res
	};

	return (
		<FetchAppListContext.Provider
			value={{
				appList, setAppList,
				fetchAppList,
				pagination, setPagination
			}}
		>
			{children}
		</FetchAppListContext.Provider>
	);
};
