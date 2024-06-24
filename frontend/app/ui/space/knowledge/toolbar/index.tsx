"use client";

import styles from './index.module.scss'
import {Button, Select, Input} from "antd"

const {Search} = Input;


const ToolBar = () => {

	const handleChangeType = (value: string) => {
		console.log(value);

	}
	const handleOnSearch = (value: string) => {
		console.log(value);
	}

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
				<Button type="primary">创建知识库</Button>
			</div>
		</div>
	);
}

export default ToolBar;