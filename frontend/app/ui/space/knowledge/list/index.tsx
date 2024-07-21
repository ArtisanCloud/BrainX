"use client";

import styles from './index.module.scss';
import React, {useContext, useEffect} from "react";
import {Table, Space, Button, TableProps, Switch} from "antd";
import {DeleteOutlined} from "@ant-design/icons";
import {
	FetchDatasetListContext,
	FetchDatasetListContextType
} from "@/app/ui/space/knowledge/provider/fetch-dataset-list-provider";
import {defaultPage, pageSize} from "@/app/config/constant";
import {Dataset, ResponseFetchDatasetList} from "@/app/api/knowledge/dataset";
import Image from "next/image";
import {GetPublicUrl} from "@/app/lib/url";

const columns: TableProps<Dataset>['columns'] = [
	{
		title: '名称',
		dataIndex: 'name',
		key: 'name',
		render: (_, dataset: Dataset) =>
			<div className={'flex flex-row'}>
				<Image
					priority
					width={68}
					height={68}
					alt={'app avatar'}
					className={'rounded-lg border-1'}
					src={GetPublicUrl(dataset.avatar_url!)}/>
				<div className={'flex flex-col justify-center ml-3 border-0'}>
					<span className={'border-0'} style={{fontWeight: 'bold'}}>{dataset.name}</span>
					<span style={{fontSize: '12px', color: 'gray'}}>{dataset.description}</span>
				</div>
			</div>
	},
	{
		title: '类型',
		key: 'type',
		render: (_, record) => (
			<Space size="middle">

			</Space>
		),
	},
	{
		title: '尺寸',
		dataIndex: 'size',
		key: 'size',
	},
	{
		title: '启动',
		key: 'is_published',
		render: (_, record) => (
			<Space size="middle">
				<Switch
					checkedChildren="开启"
					unCheckedChildren="关闭"
					defaultChecked/>

			</Space>
		),
	},
	{
		title: '操作',
		key: 'action',
		render: (_, record) => (
			<Space size="middle">
				<Button
					size={"small"}
					style={{border: 'none'}}
					icon={<DeleteOutlined/>}/>
			</Space>
		),
	},
];

const DatasetList = () => {
	const {
		datasetList, setDatasetList,
		fetchDatasetList,
		pagination, setPagination
	} = useContext(FetchDatasetListContext) as FetchDatasetListContextType;


	useEffect(() => {
		// console.log(pagination)
		let _page = pagination?.page ?? defaultPage
		let _pageSize = pagination?.per_page ?? pageSize

		fetchDatasetList({
			page: _page,
			page_size: _pageSize,
		}).then((res: ResponseFetchDatasetList) => {
			// console.log(res)
			setDatasetList(res.data)
			setPagination(res.pagination)
		})

	}, [
		pagination?.page, pagination?.per_page,
		fetchDatasetList,
		setDatasetList,
		setPagination,
	]);

	const onChange = (page: number, pageSize: number) => {
		// console.log("onChange", page, pageSize)
		setPagination({
			...pagination,
			page: page,
		})

	}

	return (
		<div className={styles.container}>
			<Table columns={columns} dataSource={datasetList} rowKey="id"/>
		</div>
	);
}

export default DatasetList;
