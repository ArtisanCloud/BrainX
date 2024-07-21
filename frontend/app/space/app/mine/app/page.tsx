import styles from '@/app/ui/space/app/index.module.scss';
import Toolbar from "@/app/ui/space/app/toolbar";
import AppList from "@/app/ui/space/app/list";
import {FetchAppListProvider} from "@/app/ui/space/app/provider/fetch-app-list-provider";
import CreateAppProvider from "@/app/ui/space/app/provider/create-app-provider";

const AppPage = () => {
	return (
		<div className={styles.container}>
			<FetchAppListProvider>
				<CreateAppProvider>
					<Toolbar/>
					<AppList/>
				</CreateAppProvider>
			</FetchAppListProvider>
		</div>
	);
}

export default AppPage;
