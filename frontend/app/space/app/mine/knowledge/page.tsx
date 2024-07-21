import styles from '@/app/ui/space/knowledge/index.module.scss';
import Toolbar from "@/app/ui/space/knowledge/toolbar";
import DatasetList from "@/app/ui/space/knowledge/list";
import {FetchDatasetListProvider} from "@/app/ui/space/knowledge/provider/fetch-dataset-list-provider";
import CreateDatasetProvider from "@/app/ui/space/knowledge/provider/create-dataset-provider";

const KnowledgePage = () => {
	return (
		<div className={styles.container}>
			<FetchDatasetListProvider>
				<CreateDatasetProvider>
					<Toolbar/>
					<DatasetList/>
				</CreateDatasetProvider>
			</FetchDatasetListProvider>
		</div>
	);
}

export default KnowledgePage;
