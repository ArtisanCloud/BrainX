import React, {useContext} from 'react';
import {App} from "@/app/api/robot-chat/app";
import styles from "./app.module.scss"
import {GetPublicUrl} from "@/app/lib/url";
import {
	AppContextType,
	SelectedAppContext,
	welcomeConversation
} from "@/app/ui/space/robot-chat/provider/robot-chat-provider";
import Image from "next/image";

export interface AppItemProps {
	app: App;
}

const AppBot: React.FC<AppItemProps> = ({app}) => {
	const {selectedApp, setSelectedApp,setCurrentConversation} = useContext(SelectedAppContext) as AppContextType;

	const containerClassName = `${styles.container} ${selectedApp === app ? styles.selected : ''}`;

	const clickApp = () => {
		// console.log("clickApp", app)
		setSelectedApp(app)
		setCurrentConversation(welcomeConversation)
	};

	return (
		<li className={containerClassName} onClick={clickApp}>
			<div className={styles.avatar}>
				<Image width={42} height={42} alt={'avatar'} className={styles.avatarImage} src={GetPublicUrl(app.avatar_url!)}/>
			</div>
			<div className={styles.content}>
				<div className={styles.title}>{app.name}</div>
				{/*<div className={styles.description}>{app.description}</div>*/}
			</div>
			<div></div>
		</li>
	);
};

export default AppBot;
