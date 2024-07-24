import styles from '../index.module.scss';
import Toolbar from "@/app/components/space/app/toolbar";
import AppList from "@/app/components/space/app/list";
import {FetchAppListProvider} from "@/app/components/space/app/provider/fetch-app-list-provider";
import CreateAppProvider from "@/app/components/space/app/provider/create-app-provider";
import Navbar from "@/app/components/space/navbar";

const AppPage = () => {
	return (
		<div className={styles.container}>
			<Navbar/>
			<div className={styles.main}>
				<FetchAppListProvider>
				<CreateAppProvider>
					<Toolbar/>
					<AppList/>
				</CreateAppProvider>
			</FetchAppListProvider>
			</div>
		</div>
	);
}

export default AppPage;
