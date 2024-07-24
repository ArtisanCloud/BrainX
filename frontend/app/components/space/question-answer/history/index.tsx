import styles from './index.module.scss';
import React from "react";

import {Divider} from "antd";

const History = () => {
	const data = [
		{
			name: '询问记录1',
			createdAt: '2021-09-01',
		},
		{
			name: '询问记录2',
			createdAt: '2021-09-01',
		},
		{
			name: '询问记录3',
			createdAt: '2021-09-01',
		},
		{
			name: '询问记录4',
			createdAt: '2021-09-01',
		},
		{
			name: '询问记录5',
			createdAt: '2021-09-01',
		},

	];

	return (
		<div className={styles.container}>
			<Divider orientation="left" className={styles.separate}>历史查询记录</Divider>
			<ul className={styles.list}>
				{data.map((item, index) => (
					<li key={index} className={styles.item}>
						<div className={styles.name}>{item.name}</div>
						<div className={styles.date}>{item.createdAt}</div>
					</li>
				))}
			</ul>
		</div>
	);
};

export default History;