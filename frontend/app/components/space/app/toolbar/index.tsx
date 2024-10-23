"use client";

import styles from './index.module.scss'
import {Button, Select, Input, Modal, message} from "antd"
import {useContext, useState} from "react";
import CreateApp from "../create-app";
import {CreateAppContext, CreateAppContextType} from "@/app/components/space/app/provider/create-app-provider";
import {ActionCreateApp, ResponseCreateApp} from "@/app/api/app";
import {GetOssUrl} from "@/app/lib/url";
import {FetchAppListContext} from "@/app/components/space/app/provider/fetch-app-list-provider";
import {appPageSize} from "@/app/components/space/app/list";
import {useNotification} from "@/app/components/notification";

const {Search} = Input;


const ToolBar = () => {

	const {setAppList, fetchAppList} = useContext(FetchAppListContext);

	const {
		name, description, avatarUrl,
	} = useContext(CreateAppContext) as CreateAppContextType;

	const {msgSuccess, msgWarn, msgError} = useNotification();
	const [loading, setLoading] = useState(false);


	const [isModalOpen, setIsModalOpen] = useState(false);

	const handleChangeType = (value: string) => {
		console.log(value);
	}
	const handleOnSearch = (value: string) => {
		console.log(value);
	}

	const showModal = () => {
		setIsModalOpen(true);
	};

	const handleOk = async () => {
		// console.log(name, description, avatarUrl)

		if (loading) {
			return
		}

		if (!name) {
			msgWarn("需要输入名字")
			return
		}
		if (!description) {
			msgWarn("需要输入描述")
			return
		}

		const res: ResponseCreateApp = await ActionCreateApp({
			name: name!,
			description: description!,
			avatar_url: GetOssUrl(avatarUrl!),
		})

		setLoading(false);

		if (res.error && res.error !== "") {
			msgError('生成机器人失败:' + res.error);
		} else {
			msgSuccess('生成机器人成功');
		}

		setIsModalOpen(false);

		fetchAppList({
			page: 1,
			page_size: appPageSize,
		}).then((res) => {
			// console.log(res.data)
			setAppList(res.data)
		})

	};

	const handleCancel = () => {
		setIsModalOpen(false);
	};


	return (
		<div className={styles.container}>
			<div className={styles.tool}>
				<span className={styles.typeLabel}>类型 :</span>
				<div className={styles.type}>
					<Select
						defaultValue="All"
						style={{
							flex: 1,
							borderRadius: '4px',
							border: 'none'
						}}
						size="small"
						onChange={handleChangeType}
						options={[
							{value: 'all', label: 'All'},
							{value: 'published', label: 'published'},
							{value: 'myFavourite', label: 'My Favourite'},
						]}
						getPopupContainer={(triggerNode) => triggerNode.parentNode}
						dropdownStyle={{
							position: 'absolute',
							width: 'auto',
							minWidth: 120,
						}}
					/>
				</div>
				<div className={styles.search}>
					<Search
						style={{
							border: '1px solid #eee',
							width: 200,
							backgroundColor: 'white',
							borderRadius: '4px'
						}}
						size="small"
						// variant="borderless"
						placeholder="搜索"
						onSearch={handleOnSearch}
					/>
				</div>


			</div>
			<div className={styles.create}>
				<Button
					onClick={showModal}
					type="primary">创建机器人</Button>
				{/*{contextHolder}*/}
				<Modal
					style={{top: 120}}
					title="创建机器人"
					open={isModalOpen}
					onOk={handleOk}
					onCancel={handleCancel}
				>
					<CreateApp/>
				</Modal>
			</div>
		</div>
	);
}

export default ToolBar;
