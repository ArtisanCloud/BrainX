import {
  Modal,
  ModalContent,
  Button,
  Input,
  ModalBody,
  ModalFooter,
} from "@heroui/react";
import { Provider } from "@/app/api/model-provider/provider";
import styles from "./index.module.scss";
import {
  ArrowTopRightOnSquareIcon,
  CogIcon,
  PlusIcon,
} from "@heroicons/react/24/outline";
import { useState } from "react";
import { ProviderIcon } from "./provider-icon";
import DynamicForm from "../../components/dynamic-form";

// 定义 Props 接口
interface ModelSettingProviderProps {
  provider: Provider; // 根据实际类型替换 any
}

export default function ModelSettingProvider({
  provider,
}: ModelSettingProviderProps) {
  const [isOpen, setIsOpen] = useState(false); // 控制Modal开关的状态
  const [requiredFilled, setRequiredFilled] = useState(false); // 控制Modal开关的状态
  const [formValues, setFormValues] = useState<Record<string, any>>({});

  // 手动控制Modal开关
  const onOpen = () => setIsOpen(true);
  const onClose = () => setIsOpen(false);

  // 监听 Modal 打开状态变化
  const onOpenChange = (newIsOpen: boolean) => {
    // console.log(newIsOpen); // 打开状态的变化
    setIsOpen(newIsOpen);
  };

  const onSubmit = () => {
    console.log("form:", formValues); // 表单变化时触发的回调函数
    setIsOpen(false); // 关闭Modal
  };

  const onFormChanged = (formValues: Record<string, any>) => {
    // console.log("form changed", formValues); // 表单变化时触发的回调函数
    setFormValues(formValues); // 更新表单值
  };

  const onFilledRequired = (filled: boolean) => {
    console.log(filled);
    setRequiredFilled(filled);
  };

  return (
    <>
      <Button
        key={provider.provider}
        className={styles.btnFun}
        startContent={<CogIcon style={{ width: "18px", color: "gray" }} />}
        onPress={onOpen}
      >
        设置
      </Button>
      <Modal
        size="3xl"
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
                      设置 {provider.provider}
                    </span>
                    <ProviderIcon providerName={provider.provider} />
                  </div>
                  <div>
                    <DynamicForm
                      credentialSchemas={
                        provider.provider_credential_schema
                          ?.credential_form_schemas!
                      }
                      onFilledRequired={onFilledRequired}
                      onChange={onFormChanged}
                    />
                  </div>
                </div>
              </div>
              <div className="sticky bottom-0 flex justify-between items-center mt-2 -mx-2 pt-4 px-2 pb-6 flex-wrap gap-y-2 bg-white">
                <div className="inline-flex items-center text-xs text-primary-600">
                  {provider.help.title.zh_CN + " "}
                  <a
                    href={provider.help?.url.en_US || "#"}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <ArrowTopRightOnSquareIcon width={14} />
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
