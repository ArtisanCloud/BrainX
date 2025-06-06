import styles from "./index.module.scss";
import React, {useEffect, useMemo} from "react";
import useSettingsStore from "@/app/store/setting";
import {useNotification} from "@/app/components/notification";
import useLoadingStore from "@/app/store/global-loading";
import {
  ActionFetchProviderSchemaList, Provider,
  ResponseFetchProviderList,
} from "@/app/api/model-provider/provider";
import SystemModelSetting from "@/app/(workspace)/space/settings/model-provider/system-model-setting";
import ToConfigProviders
  from "@/app/(workspace)/space/settings/model-provider/system-model-setting/to-config-providers";
import ConfiguredProviders
  from "@/app/(workspace)/space/settings/model-provider/system-model-setting/configured-providers";
import ModalSaveProvider
  from "@/app/(workspace)/space/settings/model-provider/system-model-setting/modal-save-provider";
import ModalSaveModel from "@/app/(workspace)/space/settings/model-provider/system-model-setting/modal-save-model";

const ModelProviderComponent: React.FC = () => {
  const {setProviders, toRefreshProviders,currentProvider} = useSettingsStore();
  const {loading, setLoading} = useLoadingStore();
  const {msgError} = useNotification();

  useEffect(() => {
    const fetchProviders = async () => {
      if (loading) {
        return;
      } else {
        setLoading(true);
      }
      try {
        // 调用 ActionFetchProviderSchemaList 获取数据
        const response: ResponseFetchProviderList =
          await ActionFetchProviderSchemaList();
        setProviders(response.data); // 将数据保存到 zustand store
        // console.log(response.data)
      } catch (error) {
        msgError("加载提供者列表失败");
      } finally {
        setLoading(false);
      }
    };

    fetchProviders();
  }, [toRefreshProviders]);

  return (
    <div className={styles.container}>
      <div className={styles.configuredModelProvidersBox}>
        <div className={styles.systemModelSettingBox}>
          <span className="text-gray-800 font-medium text-sm">模型列表</span>
          <SystemModelSetting/>
        </div>
        <div className={styles.configuredModelProviders}>
          <ConfiguredProviders/>
        </div>
      </div>
      <div className={styles.toConfigModelProvidersBox}>
        <div className={styles.labelAddModel}>
          <span className="text-xs font-semibold text-gray-500">+添加模型</span>
          <span className="grow ml-3 h-[1px] bg-gradient-to-r from-[#f3f4f6]"></span>
        </div>
        <ToConfigProviders/>
      </div>
      <ModalSaveProvider provider={currentProvider!}/>
      <ModalSaveModel provider={currentProvider!}/>
    </div>
  );
};
export default ModelProviderComponent;
