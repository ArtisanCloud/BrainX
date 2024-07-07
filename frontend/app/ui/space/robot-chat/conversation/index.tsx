import styles from './index.module.scss';
import React, {useContext} from "react";
import {AppContextType, SelectedAppContext} from "@/app/ui/space/robot-chat/provider/robot-chat-provider";

const Conversation = () => {

	const {currentAppConversations} = useContext(SelectedAppContext) as AppContextType;

	const handleClickConversation = (conversation: any) => {
		// console.log(conversation)
	}

	return (
		<div className={styles.container}>
			<ul className={styles.list}>
				{currentAppConversations && currentAppConversations.map((item, index) => (
					<li key={index} className={styles.item} onClick={() => handleClickConversation(item)}>
						<div className={styles.name}>{item.name}</div>
						<div className={styles.date}>{item.createdAt}</div>
					</li>
				))}
			</ul>
		</div>
	);
};

export default Conversation;
