import styles from '../index.module.scss';
import Toolbar from "./toolbar";
import DatasetList from "./list";
import {FetchDatasetListProvider} from "@/app/(workspace)/space/(mine)/knowledge/provider/fetch-dataset-list-provider";
import CreateDatasetProvider from "@/app/(workspace)/space/(mine)/knowledge/provider/create-dataset-provider";
import Navbar from "../navbar";

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
