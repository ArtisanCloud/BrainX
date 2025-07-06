import styles from './index.module.scss';
import SelectionSystemModel from "@/app/(workspace)/space/settings/model-provider/components/selection-system-model";
import {ModelTypeEnum} from "@/app/api/model-provider";
import {useTranslation} from "react-i18next";
import useSettingsStore from "@/app/store/setting";
import {getModelParameterRule, ProviderModelWithStatusEntity, ProviderWithModels} from "@/app/api/model-provider/model";
import ConfigModelPanel from "@/app/(workspace)/space/settings/model-provider/app-config-models/config-model-panel";
import {useModelConfigStore} from "@/app/store/app/model-config";
import SelectLLMProvider, {SelectLLMContext, SelectLLMContextType} from "@/app/(workspace)/space/(mine)/provider/llm";
import {useContext} from "react";

const AppConfigModels: React.FC = () => {

  const { setSelectedModel,setSelectedProvider } = useContext(SelectLLMContext) as SelectLLMContextType;
  const {t} = useTranslation();
  const {setPanelOpen, setProviderModel, setParams, isPanelOpen} = useModelConfigStore();
  const {
    workspaceModels,
    workspaceDefaultModels, setWorkspaceDefaultModels
  } = useSettingsStore();
  const onSelectModel = (modelType: ModelTypeEnum, provider: ProviderWithModels, model: ProviderModelWithStatusEntity) => {
    // console.log(modelType, provider, model)
    setSelectedProvider(provider.provider)
    setSelectedModel(model.model)
  }
  const onToConfigModel = async (provider: ProviderWithModels, model: ProviderModelWithStatusEntity) => {
    const res = await getModelParameterRule({
      provider: provider.provider,
      model: model.model
    })

    if (res?.data?.length > 0) {
      setParams(res.data)
      setPanelOpen(true)
      setProviderModel(model)
    }

  }

  return (
    <div className={styles.container}>
      <SelectLLMProvider>
      <div className="relative">
        <SelectionSystemModel
          providersWithModels={workspaceModels[ModelTypeEnum.textGeneration]}
          currentSelectValue={workspaceDefaultModels[ModelTypeEnum.textGeneration]?.model}
          onSelect={(provider, model) => {
            onSelectModel(ModelTypeEnum.textGeneration, provider, model)
          }}
          initShowConfig={true}
          onToConfig={(provider, model) => {
            onToConfigModel(provider, model)
          }}
        />
      </div>
      <div className={styles.configModel} style={{display: isPanelOpen ? 'flex' : 'none'}}>
        <ConfigModelPanel/>
      </div>
      </SelectLLMProvider>
    </div>
  )
}
export default AppConfigModels
