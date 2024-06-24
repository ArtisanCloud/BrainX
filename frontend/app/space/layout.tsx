import styles from "../ui/index.module.scss"
import Footer from "@/app/ui/footer/footer"
import Menu from "@/app/ui/menu";
import SidebarProvider from "@/app/ui/menu/provider/sidebar-provider";

export default function Layout({children}: { children: React.ReactNode }) {
	return (
		<SidebarProvider>
			<div className={styles.container}>
				<Menu/>
				<div className={styles.content}>
					<div className={styles.main}>{children}</div>
					<Footer/>
				</div>
			</div>
		</SidebarProvider>
	);
}
