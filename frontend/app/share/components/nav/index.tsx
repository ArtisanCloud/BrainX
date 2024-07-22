import styles from './index.module.scss';
import React from "react";
import {Select} from 'antd';
import {
	baidu_ernie_lite_8k, baidu_qianfan_ernie_3_d_5_8k,
	label_openai_gpt_3_d_5_turbo,
} from "@/app/config/llm";

type LLMSelectedHandler = (value: string) => void;

const ShareNav = ({onSelectedLLM, onDeselectedLLM}: {
	onSelectedLLM: LLMSelectedHandler,
	onDeselectedLLM?: LLMSelectedHandler
}) => {
	const handleChangeLLM = (e: any) => {
		// console.log("handleChangeLLM", e.value)
		onSelectedLLM(e.value)

	}

	return (
		<div className={styles.container}>

			<div className={styles.titleBox}>
				<div className={styles.title}>
					version:
				</div>
				<Select
					className={styles.selectLLM}
					labelInValue
					style={{border: "none"}}
					// defaultValue={{value: baidu_qianfan_ernie_3_d_5_8k, label: '3.5'}}
					defaultValue={{value: baidu_ernie_lite_8k, label: 'lite'}}
					onChange={handleChangeLLM}
					options={[
						{
							label: '3.5',
							value: baidu_qianfan_ernie_3_d_5_8k,
						},
						{
							label: 'lite',
							value: baidu_ernie_lite_8k,
						},
						{
							label: 'turbo',
							value: label_openai_gpt_3_d_5_turbo,
						},


					]}
				/>
			</div>
		</div>
	)
}
export default ShareNav
