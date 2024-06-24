import styles from './index.module.scss';
import React, {useContext} from "react";
import {Button, Select} from 'antd';
import {MenuOutlined, MenuFoldOutlined, MenuUnfoldOutlined} from '@ant-design/icons';
import {
	AppContextType,
	SelectedAppContext,

} from "@/app/ui/space/robot-chat/provider/robot-chat-provider";
import {GetPublicUrl} from "@/app/lib/url";
import {ProfileContext, ProfileContextType} from "@/app/ui/space/profile/provider/profile-provider";
import Image from "next/image";
import {SelectLLMContext, SelectLLMContextType} from "@/app/ui/space/provider/llm";
import {
	baidu_ernie_lite_8k,
	baidu_ernie_speed_128k,
	baidu_qianfan_bloomz_7b_compressed,
	baidu_qianfan_ernie_3_d_5_8k,
	baidu_qianfan_ernie_4_d_0_8k, label_baidu_ernie_lite_8k,
	label_baidu_ernie_speed_128k,
	label_baidu_qianfan_bloomz_7b_compressed,
	label_baidu_qianfan_ernie_3_d_5_8k,
	label_baidu_qianfan_ernie_4_d_0_8k,
	label_ollama_13b_alpaca_16k,
	label_ollama_gemma_2b,
	label_openai_gpt_3_d_5_turbo,
	ollama_13b_alpaca_16k,
	ollama_gemma_2b,
	openai_gpt_3_d_5_turbo
} from "@/app/config/llm";

const ChatNav = () => {
	const {setSelectedLlm} = useContext(SelectLLMContext) as SelectLLMContextType;
	const {selectedApp} = useContext(SelectedAppContext) as AppContextType;
	const {showProfile, setShowProfile} = useContext(ProfileContext) as ProfileContextType;


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
			<div className={styles.info}>
				<div className={styles.avatar}>
					<Image width={42} height={42} alt={'avatar'} className={styles.avatarImage}
								 src={GetPublicUrl(selectedApp?.avatar_url!)}/>
				</div>
				<div className={styles.content}>
					<div className={styles.titleBox}>
						<div className={styles.title}>{selectedApp?.name}</div>
						<div className={styles.title}>
							<Select
								className={styles.selectLLM}
								labelInValue
								style={{border: "none"}}
								defaultValue={{value: openai_gpt_3_d_5_turbo, label: label_openai_gpt_3_d_5_turbo}}
								onChange={handleChangeLLM}
								options={[
									{
										label: label_openai_gpt_3_d_5_turbo,
										value: openai_gpt_3_d_5_turbo,
									},
									{
										label: label_baidu_qianfan_ernie_4_d_0_8k,
										value: baidu_qianfan_ernie_4_d_0_8k
									},
									{
										label: label_baidu_qianfan_ernie_3_d_5_8k,
										value: baidu_qianfan_ernie_3_d_5_8k
									},

									{
										label: label_baidu_qianfan_bloomz_7b_compressed,
										value: baidu_qianfan_bloomz_7b_compressed,
									},
									{
										label: label_baidu_ernie_speed_128k,
										value: baidu_ernie_speed_128k,
									},
									{
										label: label_baidu_ernie_lite_8k,
										value: baidu_ernie_lite_8k,
									},
									{
										label: label_ollama_13b_alpaca_16k,
										value: ollama_13b_alpaca_16k,
									},
									{
										label: label_ollama_gemma_2b,
										value: ollama_gemma_2b,
									},
								]}
							/>
						</div>
					</div>
					<div className={styles.description}>{selectedApp?.description}</div>
				</div>
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
export default ChatNav
