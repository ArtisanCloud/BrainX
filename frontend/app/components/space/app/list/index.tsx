"use client";

import styles from './index.module.scss';
import React, {useContext, useEffect} from "react";
import AppBot from "@/app/components/space/app/agent-bot";
import {App, ResponseFetchAppList} from "@/app/api/app";
import {Pagination} from 'antd';
import {FetchAppListContext, FetchAppListContextType} from "@/app/components/space/app/provider/fetch-app-list-provider";
import {defaultPage, pageSize} from "@/app/config/constant";


export const appPageSize = 9

const AppList = () => {

	const {
		appList, setAppList,
		fetchAppList,
		pagination, setPagination
	} = useContext(FetchAppListContext) as FetchAppListContextType;


	useEffect(() => {

		let _page = pagination?.page ?? defaultPage
		let _pageSize = pagination?.per_page ?? pageSize
		fetchAppList({
			page: _page,
			page_size: _pageSize,
		}).then((res: ResponseFetchAppList) => {
			// console.log(res)
			setAppList(res.data)
			setPagination(res.pagination)
		})

	}, [pagination?.page, pagination?.per_page	]);

	const onChange = (page: number, pageSize: number) => {
		// console.log("onChange", page, pageSize)
		setPagination({
			...pagination,
			page: page,
		})

	}

	return (
		<div className={styles.container}>
			<div className={styles.list}>
				{appList?.map((app:App) => (
					<AppBot key={app.uuid} app={app}/>
				))}
			</div>
			{appList?.length > 0 && (
				<div className={styles.pagination}>
					<Pagination
						showQuickJumper
						// showSizeChanger
						defaultCurrent={pagination.page}
						total={pagination.total_rows}
						onChange={onChange}/>
				</div>
			)}

		</div>
	);
}

export default AppList;
