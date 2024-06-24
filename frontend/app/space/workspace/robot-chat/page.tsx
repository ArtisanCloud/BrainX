"use client";

import styles from "@/app/ui/space/robot-chat/index.module.scss";
import ChatNav from "@/app/ui/space/robot-chat/nav";
import Profile from "@/app/ui/space/profile";
import Box from "@/app/ui/space/robot-chat/box";
import ChatSidebar from "@/app/ui/space/robot-chat/sidebar";

import {
	ChatBotProvider,
} from "@/app/ui/space/robot-chat/provider/robot-chat-provider";
import React from "react";
import ProfileProvider from "@/app/ui/space/profile/provider/profile-provider";
import SelectLLMProvider from "@/app/ui/space/provider/llm";
import Navbar from "@/app/ui/space/navbar";

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
