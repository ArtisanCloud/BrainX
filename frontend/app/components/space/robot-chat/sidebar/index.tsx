import ChatBot from "@/app/components/space/robot-chat/bot-group/app/chatbot";
import BotGroup, {defaultApp} from "@/app/components/space/robot-chat/bot-group";
import styles from "./index.module.scss";
import Conversation from "@/app/components/space/robot-chat/conversation";
import React, {useContext} from "react";
import {Divider} from 'antd';
import {LeftOutlined, RightOutlined} from '@ant-design/icons';
import  {
	RobotChatUIContext,
	RobotChatUIContextType
} from "@/app/components/space/robot-chat/provider/robot-chat-provider";

const Sidebar = () => {
	const {showChatSidebar, setShowChatSidebar} = useContext(RobotChatUIContext) as RobotChatUIContextType;

	const handleClickHandler = () => {
		setShowChatSidebar(!showChatSidebar)
		// console.log(showChatSidebar)
	}

	return (
		<div className={styles.container}>
			<div className={`${styles.list} ${showChatSidebar ? styles.show : styles.hide}`}>
				<div className={styles.defaultChat}>
					<ChatBot key={0} app={defaultApp}/>
				</div>
				<Divider orientation="left" className={styles.separate}>智能代理</Divider>
				<BotGroup/>
				<Divider orientation="left" className={styles.separate}>聊天记录</Divider>
				<Conversation/>
			</div>
			<div className={styles.handleContainer} onClick={handleClickHandler}>
				<div className={styles.handle}>
					{showChatSidebar ? <LeftOutlined
						style={{fontSize: '8px'}}
					/> : <RightOutlined
						style={{fontSize: '8px'}}
					/>}
				</div>
			</div>
		</div>

	);
}

export default Sidebar;
