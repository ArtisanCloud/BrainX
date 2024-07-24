import styles from '../index.module.scss';
import Toolbar from "@/app/components/space/knowledge/toolbar";
import DatasetList from "@/app/components/space/knowledge/list";
import {FetchDatasetListProvider} from "@/app/components/space/knowledge/provider/fetch-dataset-list-provider";
import CreateDatasetProvider from "@/app/components/space/knowledge/provider/create-dataset-provider";
import Navbar from "@/app/components/space/navbar";

const KnowledgePage = () => {
	return (
		<div className={styles.container}>
			<Navbar/>
			<div className={styles.main}>
				<FetchDatasetListProvider>
					<CreateDatasetProvider>
						<Toolbar/>
						<DatasetList/>
					</CreateDatasetProvider>
				</FetchDatasetListProvider>
			</div>
		</div>
	);
}

export default KnowledgePage;
