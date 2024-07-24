import styles from "@/app/components/index.module.scss"
import Footer from "@/app/components/footer/footer"
import Menu from "@/app/components/menu";
import SidebarProvider from "@/app/components/menu/provider/sidebar-provider";

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
