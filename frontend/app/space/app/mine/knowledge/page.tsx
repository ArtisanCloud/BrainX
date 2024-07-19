import styles from '@/app/ui/space/knowledge/index.module.scss';
import Toolbar from "@/app/ui/space/knowledge/toolbar";
import KnowledgeList from "@/app/ui/space/knowledge/list";

const KnowledgePage = () => {
	return (
		<div className={styles.container}>
			<Toolbar/>
			<KnowledgeList/>
		</div>
	);
}

export default KnowledgePage;
