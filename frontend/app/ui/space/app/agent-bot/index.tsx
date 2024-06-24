"use client";

import styles from './index.module.scss'
import React, {useContext, useEffect, useState} from "react";
import {GetPublicUrl} from "@/app/lib/url";
import {Button, Dropdown, MenuProps, Popconfirm, PopconfirmProps, message} from 'antd';
import {EllipsisOutlined} from '@ant-design/icons';
import {AppItemProps} from "@/app/ui/space/robot-chat/bot-group/app/chatbot";
import Image from "next/image";
import Link from "next/link";
import {defaultPage, routeRobotChat} from "@/app/config/constant/index";
import {FetchAppListContext} from "@/app/ui/space/app/provider/fetch-app-list-provider";
import {appPageSize} from "@/app/ui/space/app/list";
import {ActionDeleteApp} from "@/app/api/robot-chat/app";
import {sleep} from "@/app/lib/utils";


const AppBot: React.FC<AppItemProps> = ({app}) => {
	const [messageApi, contextHolder] = message.useMessage();

	const {
		appList, setAppList,
		fetchAppList,
	} = useContext(FetchAppListContext);

	const handleClickAnalytics = (e: any,) => {
		e.preventDefault()
		// console.log("analytics", app.name)
	}

	const confirmDelete: PopconfirmProps['onConfirm'] = async (e: any) => {
		e.preventDefault()
		// console.log(e);

		// delete app
		const res = await ActionDeleteApp(app.uuid!)
		if (res.result){
			messageApi.info('删除机器人成功');

			await sleep(500)
			fetchAppList({
				page: defaultPage,
				page_size: appPageSize,
			}).then((res) => {
				setAppList(res.data);
			});

		} else {
			messageApi.error('删除机器人失败');
		}

	};

	const cancelDelete: PopconfirmProps['onCancel'] = (e: any) => {
		e.preventDefault()
		// console.log(e);
	};

	const items: MenuProps['items'] = [
		// {
		// 	key: 'analytics',
		// 	label:(
		// 		<span onClick={handleClickAnalytics}>分析</span>
		// 	),
		// },
		{
			key: 'delete',
			label: (
				<Popconfirm
					title="删除机器人"
					description="确定要删除该机器人么?"
					onConfirm={confirmDelete}
					onCancel={cancelDelete}
					okText="Yes"
					cancelText="No"
				>
					<a onClick={(e) => {
						e.preventDefault()
					}}>
						<span style={{color: "red"}}>删除</span>
					</a>
				</Popconfirm>
			),
		},
	];

	return (
		<div className={styles.container}>
			{contextHolder}
			<Link
				key={app.id}
				href={{
					pathname: routeRobotChat,
					query: {
						appUuid: app.uuid
					}
				}}
			>
				<div className={styles.main}>
					<div className={styles.avatar}>
						<Image
							priority
							width={68}
							height={68}
							alt={'app avatar'}
							className={styles.avatarImage}
							src={GetPublicUrl(app.avatar_url!)}/>
					</div>
					<div className={styles.content}>
						<div className={styles.appInfo}>
							<div className={styles.title}>{app.name}</div>
							<div className={styles.action}>
								<div className={styles.favourite}></div>
								<div className={styles.button}>
									<Dropdown menu={{items}} placement="bottomLeft" arrow={{pointAtCenter: true}}>
										<Button
											className={styles.buttonTool}
											size="small"
											onClick={(e) => {
												e.preventDefault();
											}}
											icon={<EllipsisOutlined/>}/>
									</Dropdown>
								</div>
								<div></div>
							</div>
						</div>
						<span className={styles.sema}></span>
						<div className={styles.llm}>
							<span className={styles.span}>GPT3.5</span>
						</div>
					</div>
				</div>
				<div className={styles.separate}></div>
				<div className={styles.footer}>
					<div className={styles.userInfo}>User info</div>
					<div className={styles.date}>修改日期：{app.updatedAt ?? "0000-00-00"}</div>
				</div>

			</Link>
		</div>
	);
}
export default AppBot;
