import styles from '../index.module.scss';
import Navbar from "@/app/components/space/navbar";

const WorkflowPage = () => {
	return (
		<div className={styles.container}>
			<Navbar/>
			<div className={styles.main}>
				<h1>Workflow Page</h1>
			</div>
		</div>
	);
}

export default WorkflowPage;
