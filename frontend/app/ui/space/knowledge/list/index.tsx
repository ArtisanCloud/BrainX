"use client";

import styles from './index.module.scss';
import {Knowledge} from "@/app/api/knowledge";
import {useState} from "react";
import {Table, Space, Button, TableProps} from "antd";
import {DeleteOutlined} from "@ant-design/icons";

const columns: TableProps<Knowledge>['columns'] = [
	{
		title: 'Name',
		dataIndex: 'name',
		key: 'name',
		render: (_, knowledge: Knowledge) =>
			<div>
				<span style={{fontWeight: 'bold'}}>{knowledge.name}</span>
				<br/>
				<span style={{fontSize: '12px', color: 'gray'}}>{knowledge.description}</span>
			</div>
	},
	{
		title: '单元',
		dataIndex: 'units',
		key: 'units',
	},
	{
		title: '尺寸',
		dataIndex: 'size',
		key: 'size',
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

const KnowledgeList = () => {

	const [list, setList] = useState<Knowledge[]>([
		{
			id: 1,
			name: "PowerWechat",
			description: "赞助我们#、返佣商品#、评论数据管理#、自动回复#、数据统计与分析#、客服消息#",
			units: 82,
			size: "192.21 kB",
			updatedAt: "2021-09-01 12:00:00",
		},
		{
			id: 2,
			name: "营销知识",
			description: "关于营销方面的知识库",
			units: 0,
			size: " kB",
			updatedAt: "2021-09-01 12:00:00",
		},
		{
			id: 3,
			name: "PowerX",
			description: "私域相关的知识",
			units: 1,
			size: "473 kB",
			updatedAt: "2021-09-01 12:00:00",
		}
	]);

	return (
		<div className={styles.container}>
			<Table columns={columns} dataSource={list} rowKey="id"/>
		</div>
	);
}

export default KnowledgeList;
