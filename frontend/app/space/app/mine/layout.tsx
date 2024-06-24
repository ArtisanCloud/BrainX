import styles from "./index.module.scss"
import Index from "@/app/ui/space/navbar";

export default function Layout({children}: { children: React.ReactNode }) {
	return (
		<div className={styles.container}>
			<Index/>
			<div className={styles.main}>
				{children}
			</div>
		</div>
	);
}
