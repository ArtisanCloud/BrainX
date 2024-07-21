import styles from "./index.module.scss"
import Navbar from "@/app/ui/space/navbar";

export default function Layout({children}: { children: React.ReactNode }) {
	return (
		<div className={styles.container}>
			<Navbar/>
			<div className={styles.main}>
				{children}
			</div>
		</div>
	);
}
