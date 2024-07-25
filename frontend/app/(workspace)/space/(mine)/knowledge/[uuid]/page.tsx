"use client";

import Link from 'next/link'
import {useParams} from 'next/navigation';
import React, {useEffect, useState} from 'react';
import styles from "./index.module.scss";
import {Breadcrumb, Input, Button, Tag, Select, Empty, Space, Dropdown, MenuProps, SelectProps} from "antd";
import {ActionGetDataset, Dataset, DatasetImportType} from "@/app/api/knowledge/dataset";
import Image from "next/image";
import {GetOssUrl} from "@/app/lib/url";
import {
	BlockOutlined,
	FormOutlined,
	FieldTimeOutlined,
	FileAddOutlined,
	ReloadOutlined,
	LinkOutlined,
	DeleteOutlined,
	FileTextOutlined,
	UploadOutlined,
	GlobalOutlined
} from "@ant-design/icons";
import {ActionFetchDocumentList, RequestFetchDocumentList} from "@/app/api/knowledge/document";

import {Document} from "@/app/api/knowledge/document";

type LabelRender = SelectProps['labelRender'];

const {Search} = Input;

const DatasetDetailPage = () => {
	const params = useParams<{ uuid: string }>();
	const [currentDataset, setCurrentDataset] = useState<Dataset>();
	const [documents, setDocuments] = useState<Document[]>([]);

	const pathItems = [
		{
			title: <a href="/space/knowledge">知识库</a>,
		},
		{
			title: currentDataset?.name,
		},
	]

	useEffect(() => {
		const fetchDatasetData = async () => {
			try {
				const res = await ActionGetDataset({
					uuid: params.uuid
				});
				if (res.data) {

					setCurrentDataset(res.data)
					const _ = fetchDocumentsData();
				}
				// 处理返回的数据
			} catch (error) {
				console.error('Error fetching dataset:', error);
			}
		};

		const fetchDocumentsData = async () => {
			try {
				const res = await ActionFetchDocumentList({
					dataset_uuid: params.uuid
				} as RequestFetchDocumentList);
				if (res.data) {
					setDocuments(res.data)
				}
				// 处理返回的数据
			} catch (error) {
				console.error('Error fetching dataset:', error);
			}
		};

		const _ = fetchDatasetData();
	}, [params.uuid]);

	const handleOnSearch = (value: string) => {
		console.log(value);
	}

	const mergedOptions = [
		{label: 'All', value: 'all'},
		...(documents?.length > 0
			? documents.map(doc => ({
				label: doc.title,
				value: doc.id
			}))
			: [])
	];

	const labelRender: LabelRender = (props) => {
		const {label, value} = props;

		if (label) {
			return label;
		}
		return <span>当前 value 没有对应的选项</span>;
	};


	const handleClickAction: MenuProps['onClick'] = (e) => {
		console.log(e)
		// if (e.key == 'edit') {
		// 	handleEdit(currentDataset)
		// } else if (e.key == 'delete') {
		// 	handleDelete(currentDataset)
		// }
	};

	const items: MenuProps['items'] = [
		{
			label: <>
				<Link href={currentDataset?.uuid + "/upload"}>本地文档</Link>
			</>,
			key: DatasetImportType.LOCAL_DOCUMENT,
			icon: <UploadOutlined/>,
		},
		{
			label: '在线数据',
			key: DatasetImportType.ONLINE_DATA,
			icon: <GlobalOutlined/>,
		},
		{
			label: 'Notion',
			key: DatasetImportType.NOTION,
			// icon: <EditIcon/>,
		},
		{
			label: 'Google文档',
			key: DatasetImportType.GOOGLE_DOC,
			// icon: <EditIcon/>,
		},
		{
			label: '飞书',
			key: DatasetImportType.LARK,
			// icon: <EditIcon/>,
		},
		{
			label: '自定义',
			key: DatasetImportType.CUSTOM,
			icon: <FileTextOutlined/>,
		}

	]

	const menuProps = {
		items,
		onClick: handleClickAction,
	};


	return (

		<div className={styles.container}>
			<div className={styles.path}>
				<Breadcrumb
					items={pathItems}
				/>
			</div>
			<div className={styles.toolbar}>
				<div className={styles.left}>
					{currentDataset?.avatar_url ? (<Image
							priority
							width={48}
							height={48}
							alt={'app avatar'}
							className={'rounded-lg border-1'}
							src={GetOssUrl(currentDataset?.avatar_url)}/>
					) : (
						<div className={'w-12 h-12 flex'}>
							<BlockOutlined
								style={{fontSize: '28px', color: 'white', backgroundColor: '#5295e5'}}
								className="place-content-center rounded-lg border-1 w-full h-full"
							/>
						</div>
					)}
					<div className={styles.info}>
						<div className={styles.upper}>
							<span className={styles.name}>{currentDataset?.name}</span>
							<FormOutlined className={styles.edit}/>
						</div>
						<Tag className={styles.tag} color="#eee">auto-segment</Tag>
					</div>

				</div>
				<div className={styles.right}>
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
					<div className={styles.add}>
						<Space size="middle">
							<Dropdown
								menu={menuProps}
								placement="bottom"
								arrow={{pointAtCenter: true}}
								trigger={['click']}
							>
								<Button type="primary" className={styles.btn}>添加内容</Button>
							</Dropdown>

						</Space>
					</div>
				</div>
			</div>
			<div className={styles.main}>
				<div className={styles.content}>
					<div className={styles.filterLayer}>
						<div className={styles.filter}>
							<Select
								labelRender={labelRender}
								defaultValue="all"
								options={mergedOptions}
							/>
							<div className={styles.filterTags}>
								<Tag className={styles.tag} color="#eee">Online</Tag>
								<Tag className={styles.tag} color="#eee">Do not update</Tag>
							</div>
						</div>
						<div className={styles.action}>
							<FieldTimeOutlined/>
							<FileAddOutlined/>
							<ReloadOutlined/>
							<LinkOutlined/>
							<DeleteOutlined/>
						</div>
					</div>
					<div className={styles.documentLayer}>
						{documents.length === 0 ? (
							<Empty description="No documents available"/>
						) : (
							<div className={styles.documentsList}>
								{/* 这里渲染非空文档的内容 */}
							</div>
						)}
					</div>

				</div>
			</div>
		</div>

	);
};


export default DatasetDetailPage;
