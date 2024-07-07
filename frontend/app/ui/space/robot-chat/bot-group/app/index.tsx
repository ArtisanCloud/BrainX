import React, {useContext} from 'react';
import Image from "next/image";
import styles from "./app.module.scss"
import {Button} from 'antd';
import {MoreOutlined} from '@ant-design/icons';
import {GetPublicUrl} from "@/app/lib/url";
import {AppContextType, SelectedAppContext} from "@/app/ui/space/robot-chat/provider/robot-chat-provider";
import {AppItemProps} from "@/app/ui/space/robot-chat/bot-group/app/chatbot";
import {ActionFetchConversationList, RequestFetchConversationList} from "@/app/api/robot-chat/conversation";


const AppBot: React.FC<AppItemProps> = ({app}) => {
	const {
		selectedApp, setSelectedApp,
		setCurrentAppConversations,
	} = useContext(SelectedAppContext) as AppContextType;

	const containerClassName = `${styles.container} ${selectedApp === app ? styles.selected : ''}`;

	const clickApp = async () => {
		// console.log("clickApp", app.uuid)
		setSelectedApp(app)

		// 如果app_uuid 不为空，则请求获取对话列表
		if (app.uuid != "") {
			const res = await ActionFetchConversationList({
				app_uuid: app.uuid,
			} as RequestFetchConversationList)
			// console.log("res", res)
			// 设置当前对话列表，进入context
			if (res.data.length > 0) {
				setCurrentAppConversations(res.data)
			}
		}
	};

	const handleEdit = () => {
		console.log("handleEdit", app)
	};

	return (
		<li className={containerClassName} onClick={clickApp}>
			<div className={styles.avatar}>
				<Image width={42} height={42} alt={'avatar'} className={styles.avatarImage}
							 src={GetPublicUrl(app.avatar_url!)}/>
			</div>
			<div className={styles.content}>
				<div className={styles.title}>{app.name}</div>
				<div className={styles.description}>{app.description}</div>
			</div>
			<div className={styles.action}>
				<Button
					className={styles.button}
					onClick={handleEdit}
					size="small"
					icon={<MoreOutlined/>}/>
			</div>
		</li>
	);
};

export default AppBot;
