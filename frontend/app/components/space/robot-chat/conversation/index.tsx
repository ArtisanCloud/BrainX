import styles from './index.module.scss';
import React, {useContext} from "react";
import {AppContextType, SelectedAppContext} from "@/app/components/space/robot-chat/provider/robot-chat-provider";
import {ActionFetchCachedMessageList, RequestFetchCachedMessageList} from "@/app/api/robot-chat/conversation";
import {convertDataToConversationItems} from "@/app/utils/conversation";

const Conversation = () => {

	const {currentAppConversations, currentConversation,setCurrentConversation} = useContext(SelectedAppContext) as AppContextType;

	const handleClickConversation = async (conversation: any) => {
		// console.log(conversation)
		const res = await ActionFetchCachedMessageList({
			conversation_uuid: conversation.uuid
		} as RequestFetchCachedMessageList)

		// console.log(res)
		const items = convertDataToConversationItems(res.data)
		// console.log(items)
		// 转化成conversation items
		setCurrentConversation({
			...conversation,
			messages: res.data,
			items: items,
		})
	}

	return (
		<div className={styles.container}>
			<ul className={styles.list}>
				{currentAppConversations && currentAppConversations.map((item, index) => (
					<li
						key={index}
						className={`${styles.item} ${item.uuid == currentConversation.uuid ? styles.selected : ''}`}
						onClick={() => handleClickConversation(item)}
					>
						<div className={styles.name}>{item.name}</div>
						<div className={styles.date}>{item.createdAt}</div>
					</li>
				))}
			</ul>
		</div>
	);
};

export default Conversation;
