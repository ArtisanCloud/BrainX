import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
} from "@heroui/react";
import {Provider} from "@/app/api/model-provider/provider";
import styles
  from "@/app/(workspace)/space/settings/model-provider/system-model-setting/to-config-providers/index.module.scss";
import {PlusIcon} from "@heroicons/react/24/outline";

// 定义 Props 接口
interface ModelSettingProviderProps {
  provider: Provider; // 根据实际类型替换 any
  isOpen?: boolean;
}

export default function ModelAddModels(
  {
    provider,
    isOpen,
  }: ModelSettingProviderProps) {

  const onOpenChange = ()=>{
    console.log("changed", provider)
  }

  return (
    <>
      <Button
        key={provider.provider}
        className={styles.btnFun}
        startContent={<PlusIcon style={{ width: '18px', color: 'gray' }} />}
        onPress={()=>isOpen=true}
      >
        添加模型
      </Button>
      <Modal isOpen={isOpen} onOpenChange={onOpenChange}>
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">Modal Title</ModalHeader>
              <ModalBody>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam pulvinar risus non
                  risus hendrerit venenatis. Pellentesque sit amet hendrerit risus, sed porttitor
                  quam.
                </p>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam pulvinar risus non
                  risus hendrerit venenatis. Pellentesque sit amet hendrerit risus, sed porttitor
                  quam.
                </p>
                <p>
                  Magna exercitation reprehenderit magna aute tempor cupidatat consequat elit dolor
                  adipisicing. Mollit dolor eiusmod sunt ex incididunt cillum quis. Velit duis sit
                  officia eiusmod Lorem aliqua enim laboris do dolor eiusmod. Et mollit incididunt
                  nisi consectetur esse laborum eiusmod pariatur proident Lorem eiusmod et. Culpa
                  deserunt nostrud ad veniam.
                </p>
              </ModalBody>
              <ModalFooter>
                <Button color="danger" variant="light" onPress={onClose}>
                  Close
                </Button>
                <Button color="primary" onPress={onClose}>
                  Action
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </>
  );
}
