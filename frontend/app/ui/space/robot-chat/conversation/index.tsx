import styles from './index.module.scss';
import React from "react";

const Conversation = () => {

	const data = [
		{
			name: '聊天记录1',
			createdAt: '2021-09-01',
		},
		{
			name: '聊天记录2',
			createdAt: '2021-09-01',
		},
		{
			name: '聊天记录3',
			createdAt: '2021-09-01',
		},
		{
			name: '聊天记录4',
			createdAt: '2021-09-01',
		},
		{
			name: '聊天记录5',
			createdAt: '2021-09-01',
		},

	];

	return (
		<div className={styles.container}>
			<ul className={styles.list}>
				{data.map((item,index) => (
					<li key={index} className={styles.item}>
						<div className={styles.name}>{item.name}</div>
						<div className={styles.date}>{item.createdAt}</div>
					</li>
				))}
			</ul>
		</div>
	);
};

export default Conversation;