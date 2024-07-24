"use client";

import styles from "@/app/components/space/robot-chat/index.module.scss";
import ChatNav from "@/app/components/space/robot-chat/nav";
import Profile from "@/app/components/space/profile";
import Box from "@/app/components/space/robot-chat/box";
import ChatSidebar from "@/app/components/space/robot-chat/sidebar";

import {
	ChatBotProvider,
} from "@/app/components/space/robot-chat/provider/robot-chat-provider";
import React from "react";
import ProfileProvider from "@/app/components/space/profile/provider/profile-provider";
import SelectLLMProvider from "@/app/components/space/provider/llm";
import Navbar from "@/app/components/space/navbar";

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
