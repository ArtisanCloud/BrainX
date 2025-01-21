import styles from '../index.module.scss';
import Toolbar from "./toolbar";
import AppList from "./list";
import {FetchAppListProvider} from "@/app/(workspace)/space/(mine)/app/provider/fetch-app-list-provider";
import CreateAppProvider from "@/app/(workspace)/space/(mine)/app/provider/create-app-provider";
import Navbar from "../navbar";

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
