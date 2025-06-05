import {
  Modal,
  ModalContent,
  Button,
  Input,
  ModalBody,
  ModalFooter,
} from "@heroui/react";
import {
  ActionSaveProvider,
  ConfigurateMethod,
  CustomConfigurationStatusEnum,
  Provider,
  ResponseSaveProvider
} from "@/app/api/model-provider/provider";
import { FaCirclePlus } from "react-icons/fa6";

import styles from "./index.module.scss";
import {
  ArrowTopRightOnSquareIcon,
} from "@heroicons/react/24/outline";
import {useState} from "react";
import {ProviderIcon} from "../provider-icon";
import DynamicForm from "../../components/dynamic-form";
import useLoadingStore from "@/app/store/global-loading";
import {useNotification} from "@/app/components/notification";
import useSettingsStore from "@/app/store/setting";
import {BuildMergedCredentialSchemas} from "@/app/utils/provider";
import {ActionSaveProviderModelSetting} from "@/app/api/model-provider/model";

// 定义 Props 接口
interface ModalAddModelsProps {
  provider: Provider; // 根据实际类型替换 any
}

export default function ModalAddModels({provider}: ModalAddModelsProps) {
  const [isOpen, setIsOpen] = useState(false); // 控制Modal开关的状态
  const [requiredFilled, setRequiredFilled] = useState(false); // 控制Modal开关的状态
  const [formValues, setFormValues] = useState<Record<string, any>>({});

  const { setToRefresh } = useSettingsStore();
  const {loading, setLoading} = useLoadingStore();
  const {msgSuccess, msgError} = useNotification();


  // 手动控制Modal开关
  const onOpen =async  () => {
    setIsOpen(true);
  }
  const onClose = () => setIsOpen(false);

  // 监听 Modal 打开状态变化
  const onOpenChange = (newIsOpen: boolean) => {
    // console.log(newIsOpen); // 打开状态的变化
    setIsOpen(newIsOpen);
  };

  const onSubmit = async () => {
    // console.log("form:", formValues); // 表单变化时触发的回调函数
    if (loading) {
      return;
    } else {
      setLoading(true);
    }
    try {
      const res: ResponseSaveProvider = await ActionSaveProviderModelSetting({
        model_type:formValues["__model_type"],
        model: formValues["model"],
        provider: provider.provider,
        credentials: formValues,
        load_balancing: {
          enable: false,
        },
      });

      if (res.result) {
        msgSuccess("保存成功");
        setToRefresh()
      }else{
        msgError("保存失败");
      }

    } catch (error: any) {
      msgError(error.message);
    } finally {
      setIsOpen(false); // 关闭Modal
      setLoading(false);
    }
  };

  const onFormChanged = (formValues: Record<string, any>) => {
    // console.log("form changed", formValues); // 表单变化时触发的回调函数
    setFormValues(formValues); // 更新表单值
  };

  const onFilledRequired = (filled: boolean) => {
    // console.log(filled);
    setRequiredFilled(filled);
  };

  return (
    <>
      <Button
        key={provider.provider}
        className={
          provider.custom_configuration.status === CustomConfigurationStatusEnum.noConfigure
            ? styles.btnFun
            : styles.btnFunActive
        }
        startContent={<FaCirclePlus style={{width: "12px", color: "gray"}}/>}
        onPress={onOpen}
      >
        添加模型
      </Button>
      <Modal
        size="3xl"
        scrollBehavior={"inside"}
        backdrop="opaque"
        isOpen={isOpen}
        onOpenChange={onOpenChange}
      >
        <ModalContent>
          {(onClose) => (
            <ModalBody>
              <div>
                <div className="px-8 pt-8">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-xl font-semibold text-gray-900">
                      添加 {provider.provider} 模型
                    </span>
                    <ProviderIcon providerName={provider.provider}/>
                  </div>
                  <div>
                    <DynamicForm
                      credentialSchemas={
                        BuildMergedCredentialSchemas(provider)
                      }
                      onFilledRequired={onFilledRequired}
                      onChange={onFormChanged}
                    />
                  </div>
                </div>
              </div>
              <div
                className="sticky bottom-0 flex justify-between items-center mt-2 -mx-2 pt-4 px-2 pb-6 flex-wrap gap-y-2 bg-white">
                <div className="inline-flex items-center text-xs text-primary-600">
                  {provider.help?.label?.zh_Hans ||
                    provider.help?.label?.en_US + " "}
                  <a
                    href={
                      provider.help?.url.zh_Hans ||
                      provider.help?.url.en_US ||
                      "#"
                    }
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <ArrowTopRightOnSquareIcon width={14}/>
                  </a>
                </div>
                <div className="flex flex-row gap-1">
                  <Button variant="light" onPress={onClose}>
                    取消
                  </Button>
                  <Button
                    isDisabled={!requiredFilled}
                    color="primary"
                    onPress={onSubmit}
                  >
                    保存
                  </Button>
                </div>
              </div>
            </ModalBody>
          )}
        </ModalContent>
      </Modal>
    </>
  );
}
