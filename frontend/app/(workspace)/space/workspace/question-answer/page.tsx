"use client";

import styles from "@/app/(workspace)/space/workspace/question-answer/index.module.scss";
import History from "./history";
import {QuestionAnswerProvider} from "@/app/(workspace)/space/workspace/question-answer/question-answer-provider";
import {ProfileProvider} from "@/app/(workspace)/space/(mine)/profile/provider/profile-provider";
import QuestionAnswerTab from "./tab";
import Profile from "../../(mine)/profile";
import QANav from "./nav";
import React from "react";
import SelectLLMProvider from "@/app/(workspace)/space/(mine)/provider/llm";

const QuestionAnswerPage = () => {
	return (
		<QuestionAnswerProvider>
			<ProfileProvider>
				<div className={styles.container}>
					<div className={styles.navbar}>
						<span className={styles.title}>智能问答</span>
					</div>
					<div className={styles.content}>
						<div className={styles.sidebar}>
							<History/>
						</div>
						<SelectLLMProvider>
							<div className={styles.main}>
								<QANav/>
								<div className={styles.qaBody}>
									<QuestionAnswerTab/>
									{/* <Profile/> */}
								</div>
							</div>
						</SelectLLMProvider>
					</div>
				</div>
			</ProfileProvider>
		</QuestionAnswerProvider>
	);
}

export default QuestionAnswerPage;
