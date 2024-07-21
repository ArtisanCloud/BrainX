"use client";

// DatasetContext.tsx
import React, {createContext, useState} from 'react';
import {RequestPagination, ResponsePagination} from "@/app/api";
import {ActionFetchDatasetList, Dataset, ResponseFetchDatasetList} from "@/app/api/knowledge/dataset";
import {defaultPage, pageSize} from "@/app/config/constant";

export interface FetchDatasetListContextType {
	datasetList: Dataset[]; // 数据类型根据实际情况进行替换
	setDatasetList: React.Dispatch<React.SetStateAction<Dataset[] | null | undefined>>;
	fetchDatasetList: (pagination: RequestPagination) => Promise<ResponseFetchDatasetList>;
	pagination: ResponsePagination
	setPagination: React.Dispatch<React.SetStateAction<ResponsePagination>>;
}

export const FetchDatasetListContext = createContext<FetchDatasetListContextType>({} as FetchDatasetListContextType);

export const FetchDatasetListProvider: React.FC<{ children: React.ReactNode }> = ({children}) => {
	const [datasetList, setDatasetList] = useState<any>();
	const [pagination, setPagination] = useState<ResponsePagination>({
		page: defaultPage,
		per_page: pageSize,
		sort: false,
		total_rows: 0,
		total_pages: 0,
	});

	const fetchDatasetList = async (pagination: RequestPagination) => {
		// console.log(pagination.page, pagination.page_size)
		const res = await ActionFetchDatasetList(pagination);
		// console.log(res)
		return res
	};

	return (
		<FetchDatasetListContext.Provider
			value={{
				datasetList, setDatasetList,
				fetchDatasetList,
				pagination,setPagination
		}}
		>
			{children}
		</FetchDatasetListContext.Provider>
	);
};
