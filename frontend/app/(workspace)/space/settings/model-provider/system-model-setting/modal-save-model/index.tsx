import {
  Modal,
  ModalContent,
  Button,
  ModalBody,
} from "@heroui/react";
import {
  Provider,
  ResponseSaveProvider
} from "@/app/api/model-provider/provider";

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
import {ActionDeleteModel, ActionSaveProviderModelSetting, ResponseDeleteModel} from "@/app/api/model-provider/model";
import {FetchFrom, FormType} from "@/app/api/model-provider";
import {useGlobalPanel} from "@/app/store/global-panel";

// 定义 Props 接口
interface ModalSaveModelProps {
  provider: Provider; // 根据实际类型替换 any
}

export default function ModalSaveModel({provider}: ModalSaveModelProps) {
  const [requiredFilled, setRequiredFilled] = useState(false); // 控制Modal开关的状态

  const {
    formValues,setFormValues,
    setToRefresh,currentModel,
    isOpenSaveModelModal,setIsOpenSaveModelModal
  } = useSettingsStore();
  const {loading, setLoading} = useLoadingStore();
  const {msgSuccess, msgError} = useNotification();
  const showPanel = useGlobalPanel((s) => s.showPanel);

  // 手动控制Modal开关
  const onOpen =async  () => {
    setIsOpenSaveModelModal(true);
  }
  const onClose = () => setIsOpenSaveModelModal(false);

  const onDelete = ( ) =>{
    showPanel({
      title: "删除确认",
      message: "确定要删除这个模型配置吗？此操作不可撤销。",
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
    setIsOpenSaveModelModal(newIsOpen);
  };

  const onSubmitDelete = async () =>{
    if (loading) {
      return;
    } else {
      setLoading(true);
    }
    try {
      const res: ResponseDeleteModel = await ActionDeleteModel({
        provider: provider.provider,
        model_type: currentModel?.model_type!,
        model: currentModel?.model!,
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
      setIsOpenSaveModelModal(false); // 关闭Modal
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
      setIsOpenSaveModelModal(false); // 关闭Modal
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
      <Modal
        size="3xl"
        scrollBehavior={"inside"}
        backdrop="opaque"
        isOpen={isOpenSaveModelModal}
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
                    <ProviderIcon providerName={provider.provider} />
                  </div>
                  <div>
                    <DynamicForm
                      credentialSchemas={
                        BuildMergedCredentialSchemas(provider)
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
                  {currentModel?.fetch_from === FetchFrom.CUSTOMIZED && (
                    <Button color="danger" onPress={onDelete}>
                      删除
                    </Button>
                  )}
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
