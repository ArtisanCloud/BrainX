"use client"

import React, {useContext, useEffect, useState} from 'react';
import {Collapse, CollapseProps} from 'antd';
import styles from './index.module.scss'
import {ActionFetchAppList, App, maxPageSize, pageSize, ResponseFetchAppList} from "@/app/api/robot-chat/app";
import {
	AppContextType,
	SelectedAppContext
} from "@/app/ui/space/robot-chat/provider/robot-chat-provider";
import AppList from "@/app/ui/space/robot-chat/bot-group/app/list";
import {GetAppFromUUID} from "@/app/lib/app";


export const defaultApp: App = {
	user_id: 1,
	name: '纯聊天',
	description: '您可以先体验一下，尝试与机器人对话，随后可以创建自己的代理机器人',
	avatar_url: 'agent.png',
}

const Index = () => {
	const {selectedApp, setSelectedApp} = useContext(SelectedAppContext) as AppContextType;
	const [list, setList] = useState<App[]>([]);

	const items: CollapseProps['items'] = [
		{
			key: 'group1',
			label: '自定义分组',
			children: <AppList list={list}/>,
		},
		{
			key: 'default-group',
			label: '默认分组',
			children: [],
		},
	];

	useEffect(() => {
		// console.log("useEffect call")
		ActionFetchAppList({
			page: 1,
			page_size: maxPageSize,
		}).then((res: ResponseFetchAppList) => {
			// console.log(res)
			setList(res.data)

			let data = window.location.search;
			const params = new URLSearchParams(data);
			const appUuid = params.get('appUuid');

			if (appUuid) {
				// console.log(appUuid,list)
				const app = GetAppFromUUID(appUuid as string, res.data)
				// console.log(app)
				setSelectedApp(app)
				// console.log(selectedApp)
			} else {
				setSelectedApp(defaultApp)
			}
		})
	}, [setSelectedApp]);


	return (
		<div className={styles.container}>
			<Collapse
				className={styles.group}
				items={items}
				style={{paddingLeft: '12px', paddingRight: '12px'}}
				bordered={false}
				defaultActiveKey={['group1']}
			/>
		</div>
	);
}

export default Index
