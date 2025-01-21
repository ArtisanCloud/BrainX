"use client";

import styles from "./index.module.scss";
import ChatNav from "./chat-nav";
import Profile from "../../(mine)/profile";
import Box from "./box";
import ChatSidebar from "./sidebar";

import {
	ChatBotProvider,
} from "@/app/(workspace)/space/workspace/robot-chat/provider/robot-chat-provider";
import React from "react";
import ProfileProvider from "@/app/(workspace)/space/(mine)/profile/provider/profile-provider";
import SelectLLMProvider from "@/app/(workspace)/space/(mine)/provider/llm";
import Navbar from "../../(mine)/navbar";

const RobotChat = () => {

	return (
		<>
			<ChatBotProvider>
				<ProfileProvider>
					<div className={styles.container}>
						<Navbar/>
						<div className={styles.content}>
							<ChatSidebar/>
							<SelectLLMProvider>
								<div className={styles.main}>
									<ChatNav/>
									<div className={styles.chatBody}>
										<Box/>
										<Profile/>
									</div>
								</div>
							</SelectLLMProvider>
						</div>
					</div>
				</ProfileProvider>
			</ChatBotProvider>
		</>
	)
}

export default RobotChat
