"use client";

import styles from "@/app/components/space/question-answer/index.module.scss";
import History from "@/app/components/space/question-answer/history";
import {QuestionAnswerProvider} from "@/app/components/space/question-answer/question-answer-provider";
import {ProfileProvider} from "@/app/components/space/profile/provider/profile-provider";
import QuestionAnswerTab from "@/app/components/space/question-answer/tab";
import Profile from "@/app/components/space/profile";
import QANav from "@/app/components/space/question-answer/nav";
import React from "react";
import SelectLLMProvider from "@/app/components/space/provider/llm";

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
									<Profile/>
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
