import styles from '../index.module.scss';
import Navbar from "@/app/components/space/navbar";

const PluginPage = () => {
	return (
		<div className={styles.container}>
			<Navbar/>
			<div className={styles.main}>
			<h1>Plugin Page</h1>
		</div>
		</div>
	);
}

export default PluginPage;
