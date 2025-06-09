import {
  Modal,
  ModalContent,
  Button,

  ModalBody,

} from "@heroui/react";

import {
  ActionDeleteProvider,
  ActionSaveProvider,
  ConfigurateMethod,
  CustomConfigurationStatusEnum,
  Provider, ResponseDeleteProvider,
  ResponseSaveProvider
} from "@/app/api/model-provider/provider";
import styles from "./index.module.scss";
import {
  ArrowTopRightOnSquareIcon,
} from "@heroicons/react/24/outline";
import {useState} from "react";
import {ProviderIcon} from "../../components/provider-icon";
import DynamicForm from "../../components/dynamic-form";
import useLoadingStore from "@/app/store/global-loading";
import {useNotification} from "@/app/components/notification";
import {useGlobalPanel} from "@/app/store/global-panel";
import useSettingsStore from "@/app/store/setting";
// 定义 Props 接口
interface ModalSaveProviderProps {
  provider: Provider; // 根据实际类型替换 any
}

export default function ModalSaveProvider({
                                provider,
}: ModalSaveProviderProps) {
  const [requiredFilled, setRequiredFilled] = useState(false); // 控制Modal开关的状态

  const {
    formValues,setFormValues,
    setToRefresh,
    setIsOpenSaveProviderModal, isOpenSaveProviderModal
  } = useSettingsStore();
  const {loading, setLoading} = useLoadingStore();
  const showPanel = useGlobalPanel((s) => s.showPanel);

  const {msgSuccess, msgError} = useNotification();

  const onClose = () => setIsOpenSaveProviderModal(false);

  const onDelete = async() =>{
    showPanel({
      title: "删除确认",
      message: "确定要删除这个供应商配置吗？此操作不可撤销。",
      confirmButtonColor: "danger", // 控制按钮样式
      onConfirm: () => {
        onSubmitDelete()
      },
      onCancel: () => {
        // console.log("用户取消操作");
      },
    });
  }

  // 监听 Modal 打开状态变化
  const onOpenChange = (newIsOpen: boolean) => {
    // console.log(newIsOpen); // 打开状态的变化
    setIsOpenSaveProviderModal(newIsOpen);
  };

  const onSubmitDelete = async () =>{
    if (loading) {
      return;
    } else {
      setLoading(true);
    }
    try {
      const res: ResponseDeleteProvider = await ActionDeleteProvider({
        provider: provider.provider,
      });

      if (res.result) {
        msgSuccess("删除成功");
        setToRefresh()
      }else{
        msgError("删除失败");
      }

    } catch (error: any) {
      msgError(error.message);
    } finally {
      setLoading(false);
      setIsOpenSaveProviderModal(false); // 关闭Modal
    }
  }

  const onSubmit = async () => {
    // console.log("form:", formValues); // 表单变化时触发的回调函数
    if (loading) {
      return;
    } else {
      setLoading(true);
    }
    try {
      const res: ResponseSaveProvider = await ActionSaveProvider({
        config_from: ConfigurateMethod.PREDEFINED_MODEL,
        provider: provider.provider,
        credentials: formValues,
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
      setLoading(false);
      setIsOpenSaveProviderModal(false); // 关闭Modal
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
      <Modal
        size="3xl"
        backdrop="opaque"
        isOpen={isOpenSaveProviderModal}
        onOpenChange={onOpenChange}
      >
        <ModalContent>
          {(onClose) => (
            <ModalBody>
              <div>
                <div className="px-8 pt-8">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-xl font-semibold text-gray-900">
                      设置 {provider.provider}
                    </span>
                    <ProviderIcon providerName={provider.provider}/>
                  </div>
                  <div>
                    <DynamicForm
                      credentialSchemas={
                        provider.provider_credential_schema
                          ?.credential_form_schemas!
                      }
                      value={formValues}
                      onFilledRequired={onFilledRequired}
                      onChange={onFormChanged}
                    />
                  </div>
                </div>
              </div>
              <div
                className="sticky bottom-0 flex justify-between items-center mt-2 -mx-2 pt-4 px-2 pb-6 flex-wrap gap-y-2 bg-white">
                <div className="inline-flex items-center text-xs text-primary-600">
                  {provider.help?.label?.en_US + " "}
                  <a
                    href={provider.help?.url.en_US || "#"}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <ArrowTopRightOnSquareIcon width={14}/>
                  </a>
                </div>
                <div className="flex flex-row gap-1">
                  {provider.custom_configuration.status === CustomConfigurationStatusEnum.active && (
                    <Button color="danger" onPress={onDelete}>
                      删除
                    </Button>
                  )}
                  <Button  onPress={onClose}>
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
