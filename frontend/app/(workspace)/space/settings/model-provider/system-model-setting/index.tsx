import styles from "./index.module.scss";
import {
  Button,
  Input,
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@heroui/react";
import { Cog6ToothIcon } from "@heroicons/react/24/outline";
import { useState } from "react";
import { useTranslation } from "react-i18next";
import SelectionSystemModel from "./selection-system-model";

const SystemModelSetting: React.FC = () => {
  const [formValues, setFormValues] = useState<Record<string, string>>();
  const { t } = useTranslation();
  const systemModelSelections = [
    {
      label: t("common.modelProvider.systemReasoningModel.key"),
      component: (
        <SelectionSystemModel
          label={t("common.modelProvider.systemReasoningModel.key")}
        />
      ),
    },
    {
      label: t("common.modelProvider.embeddingModel.key"),
      component: (
        <SelectionSystemModel
          label={t("common.modelProvider.embeddingModel.key")}
        />
      ),
    },
    {
      label: t("common.modelProvider.speechToTextModel.key"),
      component: (
        <SelectionSystemModel
          label={t("common.modelProvider.speechToTextModel.key")}
        />
      ),
    },
    {
      label: t("common.modelProvider.ttsModel.key"),
      component: (
        <SelectionSystemModel label={t("common.modelProvider.ttsModel.key")} />
      ),
    },
    {
      label: t("common.modelProvider.rerankModel.key"),
      component: (
        <SelectionSystemModel
          label={t("common.modelProvider.rerankModel.key")}
        />
      ),
    },
  ];

  return (
    <div className={styles.container}>
      <Popover showArrow offset={10} placement="bottom">
        <PopoverTrigger>
          <Button
            className="flex items-center px-2 h-6 text-xs text-gray-700 cursor-pointer bg-gray-50 rounded-md border-[0.5px] border-gray-200 shadow-xs hover:bg-gray-100 hover:shadow-none false "
            color="default"
            startContent={<Cog6ToothIcon className="size-4 text-gray-400" />}
          >
            设置系统模型
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[240px]">
          {(titleProps) => (
            <div className="px-1 py-2 w-full">
              {systemModelSelections.map((item, index) => (
                <div key={index} className="mb-2">
                  {item.component}
                </div>
              ))}
            </div>
          )}
        </PopoverContent>
      </Popover>
    </div>
  );
};
export default SystemModelSetting;
