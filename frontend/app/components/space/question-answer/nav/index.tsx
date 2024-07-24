import styles from './index.module.scss';
import React, {useContext} from "react";
import {Button, Select} from 'antd';
import {MenuOutlined, MenuFoldOutlined, MenuUnfoldOutlined} from '@ant-design/icons';
import {ProfileContext, ProfileContextType} from "@/app/components/space/profile/provider/profile-provider";
import {SelectLLMContext, SelectLLMContextType} from "@/app/components/space/provider/llm";
import {
	baidu_ernie_lite_8k,
	label_baidu_ernie_lite_8k,
	label_ollama_gemma_2b,
	label_openai_gpt_3_d_5_turbo,
	ollama_gemma_2b,
	openai_gpt_3_d_5_turbo
} from "@/app/config/llm";

const QANav = () => {

	const {showProfile, setShowProfile} = useContext(ProfileContext) as ProfileContextType;
	const {setSelectedLlm} = useContext(SelectLLMContext) as SelectLLMContextType;

	const toggleProfile = () => {
		// console.log("toggleProfile", showProfile)
		setShowProfile(!showProfile)
	}

	const openSetting = () => {
		console.log("openSetting")
	}

	const handleChangeLLM = (e: any) => {
		// console.log("handleChangeLLM", e.value)
		setSelectedLlm(e.value)

	}

	return (
		<div className={styles.container}>

			<div className={styles.titleBox}>
				<div className={styles.title}>
					请选择模型
				</div>
				<Select
					className={styles.selectLLM}
					labelInValue
					style={{border: "none"}}
					defaultValue={{value: label_baidu_ernie_lite_8k, label: baidu_ernie_lite_8k}}
					onChange={handleChangeLLM}
					options={[
						{
							value: openai_gpt_3_d_5_turbo,
							label: label_openai_gpt_3_d_5_turbo,
						},
						{
							label: label_baidu_ernie_lite_8k,
							value: baidu_ernie_lite_8k,
						},
						{
							value: ollama_gemma_2b,
							label: label_ollama_gemma_2b,
						},
					]}
				/>
			</div>

			<div className={styles.action}>
				<Button
					className={styles.showSetting}
					onClick={toggleProfile}
					size="small"
					icon={showProfile ? <MenuUnfoldOutlined/> : <MenuFoldOutlined/>}
				/>

				<Button
					className={styles.openSetting}
					onClick={openSetting}
					size="small"
					icon={<MenuOutlined/>}/>
			</div>

		</div>
	)
}
export default QANav
