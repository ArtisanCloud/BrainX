import {Tabs} from 'antd';
import {EyeOutlined, QuestionCircleOutlined, SearchOutlined} from '@ant-design/icons';
import QuestionAnswer from "@/app/ui/space/question-answer/qa";
import VisualQuestionAnswer from "../v-qa";
import styles from './index.module.scss';
import VisualSearch from "@/app/ui/space/question-answer/v-search";

const QuestionAnswerTab = () => {

	const items = [
		{
			key: 'qa',
			icon: <QuestionCircleOutlined/>,
			name: "QA",
			children: <QuestionAnswer/>
		},
		{
			key: 'vsearch',
			icon: <SearchOutlined/>,
			name: "Visual Search",
			children: <VisualSearch/>
		},
		{
			key: 'vqa',
			icon: <EyeOutlined/>,
			name: "Visual QA",
			children: <VisualQuestionAnswer/>
		},
	]

	return (
		<div className={styles.container}>
			<Tabs
				defaultActiveKey="qa"
				items={items.map((item, i) => {
					const id = String(i + 1);
					return {
						key: item.key,
						label: item.name,
						children: item.children,
						icon: item.icon,
					};
				})}
			/>
		</div>
	);
}
export default QuestionAnswerTab;