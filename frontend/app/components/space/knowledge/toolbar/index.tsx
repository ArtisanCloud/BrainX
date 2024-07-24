"use client";

import styles from './index.module.scss'
import {Button, message, Modal,Input} from "antd"
import CreateDataset from "@/app/components/space/knowledge/create-dataset";
import {useContext, useState} from "react";
import {CreateDatasetContext, CreateDatasetContextType} from "@/app/components/space/knowledge/provider/create-dataset-provider";
import {FetchDatasetListContext} from "@/app/components/space/knowledge/provider/fetch-dataset-list-provider";
import {ActionCreateDataset, DatasetImportType, ResponseCreateDataset} from "@/app/api/knowledge/dataset";
import {GetOssUrl} from "@/app/lib/url";
import {appPageSize} from "@/app/components/space/app/list";

const {Search} = Input;


const ToolBar = () => {

	const { setDatasetList, fetchDatasetList} = useContext(FetchDatasetListContext);

	const {
		name, description, avatarUrl,
	} = useContext(CreateDatasetContext) as CreateDatasetContextType;

	const [messageApi, contextHolder] = message.useMessage();
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

		const res: ResponseCreateDataset = await ActionCreateDataset({
			name: name!,
			description: description!,
			avatar_url: avatarUrl!,
			import_type: DatasetImportType.LOCAL_DOCUMENT,
		})

		setLoading(false);

		if (res.error && res.error !== "") {
			messageApi.error('生成机器人失败:' + res.error);
		} else {
			messageApi.info('生成机器人成功');
		}

		setIsModalOpen(false);

		fetchDatasetList({
			page: 1,
			page_size: appPageSize,
		}).then((res) => {
			// console.log(res.data)
			setDatasetList(res.data)
		})

	};

	const handleCancel = () => {
		setIsModalOpen(false);
	};

	return (
		<div className={styles.container}>
			<div className={styles.tool}>
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
					type="primary">创建知识库</Button>
				{contextHolder}
				<Modal
					style={{top: 120}}
					title="创建知识库"
					open={isModalOpen}
					onOk={handleOk}
					onCancel={handleCancel}
				>
					<CreateDataset/>
				</Modal>
			</div>
		</div>
	);
}

export default ToolBar;
