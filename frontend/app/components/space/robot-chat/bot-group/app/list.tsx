import AppBot from "@/app/components/space/robot-chat/bot-group/app/index";
import React from "react";
import {App} from "@/app/api/app";
import styles from './list.module.scss';

interface AppListProps {
	list: App[];
}

const AppList: React.FC<AppListProps> = ({list}) => {
	return (
		<div className={styles.container}>
			{list && list.map((app) => (
				<AppBot key={app.uuid} app={app}/>
			))}
		</div>
	);
};

export default AppList;
