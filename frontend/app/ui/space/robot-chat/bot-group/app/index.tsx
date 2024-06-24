import React, {useContext} from 'react';
import Image from "next/image";
import styles from "./app.module.scss"
import {Button} from 'antd';
import {MoreOutlined} from '@ant-design/icons';
import {GetPublicUrl} from "@/app/lib/url";
import {AppContextType, SelectedAppContext} from "@/app/ui/space/robot-chat/provider/robot-chat-provider";
import {AppItemProps} from "@/app/ui/space/robot-chat/bot-group/app/chatbot";


const AppBot: React.FC<AppItemProps> = ({app}) => {
	const {selectedApp, setSelectedApp} = useContext(SelectedAppContext) as AppContextType;

	const containerClassName = `${styles.container} ${selectedApp === app ? styles.selected : ''}`;

	const clickApp = () => {
		// console.log("clickApp", app)
		setSelectedApp(app)
	};

	const handleEdit = () => {
		console.log("handleEdit", app)
	};

	return (
		<li className={containerClassName} onClick={clickApp}>
			<div className={styles.avatar}>
				<Image width={42} height={42} alt={'avatar'} className={styles.avatarImage} src={GetPublicUrl(app.avatar_url!)}/>
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
