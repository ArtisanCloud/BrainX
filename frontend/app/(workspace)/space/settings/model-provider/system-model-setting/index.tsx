import styles from "./index.module.scss";
import {
  Button, Divider,
  Input,
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@heroui/react";
import {Cog6ToothIcon} from "@heroicons/react/24/outline";
import React, {useState} from "react";
import {useTranslation} from "react-i18next";
import SelectionModels from "../components/selection-system-model";
import useSettingsStore from "@/app/store/setting";
import {ModelTypeEnum} from "@/app/api/model-provider";
import {
  ProviderModelWithStatusEntity,
  ProviderWithModels,
  saveDefaultModels,
  UpdateDefaultModel
} from "@/app/api/model-provider/model";
import {useNotification} from "@/app/components/notification";
import useLoadingStore from "@/app/store/global-loading";

const SystemModelSetting: React.FC = () => {
  const [formValues, setFormValues] = useState<Record<string, string>>();
  const {t} = useTranslation();
  const {msgSuccess, msgError} = useNotification();
  const {loading, setLoading} = useLoadingStore()
  const [isPopoverOpen, setIsPopoverOpen] = useState(false);

  const {
    workspaceModels,
    workspaceDefaultModels,setWorkspaceDefaultModels
  } = useSettingsStore();

  const onSave = async () => {
    if (loading) {
      return;
    }
    setLoading(true);
    try {

      let formValues: UpdateDefaultModel[] = []
      for (const [key, value] of Object.entries(workspaceDefaultModels)) {
        // console.log(key,value)
        formValues.push({
          model_type: key as ModelTypeEnum,
          provider: value.provider.provider ?? "",
          model: value.model ?? "",
        })
      }
      const res = await saveDefaultModels({
        model_settings: formValues,
      })

      if (res.result) {
        msgSuccess("保存成功")
      }
    } catch (error) {
      msgError("保存失败")

    } finally {
      setLoading(false);
      setIsPopoverOpen(false);

    }
  }

  const onSelectModel = (key: ModelTypeEnum, provider: ProviderWithModels, model: ProviderModelWithStatusEntity) => {
    // console.log(key, model);
    setWorkspaceDefaultModels(prev => ({
      ...prev,
      [key]: {
        ...prev[key],
        provider: provider,       // ✅ 直接是字符串
        model: model.model,       // ✅ 直接是模型名称字符串
      },
    }));
  };

  const systemModelSelections = [
    {
      label: t("common.modelProvider.systemReasoningModel.key"),
      component: (
        <SelectionModels
          providersWithModels={workspaceModels[ModelTypeEnum.textGeneration]}
          label={t("common.modelProvider.systemReasoningModel.key")}
          currentSelectValue={workspaceDefaultModels[ModelTypeEnum.textGeneration]?.model}
          onSelect={(provider,model)=>{onSelectModel(ModelTypeEnum.textGeneration,provider,model)}}
        />
      ),
    },
    {
      label: t("common.modelProvider.embeddingModel.key"),
      component: (
        <SelectionModels
          providersWithModels={workspaceModels[ModelTypeEnum.textEmbedding]}
          label={t("common.modelProvider.embeddingModel.key")}
          currentSelectValue={workspaceDefaultModels[ModelTypeEnum.textEmbedding]?.model}
          onSelect={(provider,model)=>{onSelectModel(ModelTypeEnum.textEmbedding,provider,model)}}
        />
      ),
    },
    {
      label: t("common.modelProvider.speechToTextModel.key"),
      component: (
        <SelectionModels
          providersWithModels={workspaceModels[ModelTypeEnum.speech2text]}
          label={t("common.modelProvider.speechToTextModel.key")}
          currentSelectValue={workspaceDefaultModels[ModelTypeEnum.speech2text]?.model}
          onSelect={(provider,model)=>{onSelectModel(ModelTypeEnum.speech2text,provider,model)}}
        />
      ),
    },
    {
      label: t("common.modelProvider.ttsModel.key"),
      component: (
        <SelectionModels
          providersWithModels={workspaceModels[ModelTypeEnum.tts]}
          label={t("common.modelProvider.ttsModel.key")}
          currentSelectValue={workspaceDefaultModels[ModelTypeEnum.tts]?.model}
          onSelect={(provider,model)=>{onSelectModel(ModelTypeEnum.tts,provider,model)}}
        />
      ),
    },
    {
      label: t("common.modelProvider.rerankModel.key"),
      component: (
        <SelectionModels
          providersWithModels={workspaceModels[ModelTypeEnum.rerank]}
          label={t("common.modelProvider.rerankModel.key")}
          currentSelectValue={workspaceDefaultModels[ModelTypeEnum.rerank]?.model}
          onSelect={(provider,model)=>{onSelectModel(ModelTypeEnum.rerank,provider,model)}}
        />
      ),
    },
  ];

  return (
    <div className={styles.container}>
      <Popover isOpen={isPopoverOpen}
               onOpenChange={(open) => setIsPopoverOpen(open)}
               showArrow offset={10}
               placement="bottom"
      >
        <PopoverTrigger>
          <Button
            className="flex items-center px-2 h-6 text-xs text-gray-700 cursor-pointer bg-gray-50 rounded-md border-[0.5px] border-gray-200 shadow-xs hover:bg-gray-100 hover:shadow-none false "
            color="default"
            startContent={<Cog6ToothIcon className="size-4 text-gray-400"/>}
          >
            设置系统模型
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[360px]">
          {(titleProps) => (
            <div className="flex flex-col justify-center content-center ga-4 px-1 py-2 w-full">
              {systemModelSelections.map((item, index) => (
                <div key={index} className="mb-6">
                  {item.component}
                </div>
              ))}
              <Divider/>
              <div className="flex flex-row justify-end p-4">
                <Button color="default"
                        size={"sm"}
                        variant="bordered"
                        className="mr-2"
                        onPress={() => setIsPopoverOpen(false)}
                >取消</Button>
                <Button color="primary"
                        size={"sm"}
                        onPress={onSave}
                >保存</Button>
              </div>
            </div>
          )}
        </PopoverContent>
      </Popover>
    </div>
  );
};
export default SystemModelSetting;
