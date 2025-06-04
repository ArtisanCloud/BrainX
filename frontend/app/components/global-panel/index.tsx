"use client";

import { useGlobalPanel } from "@/app/store/global-panel";
import { Modal, ModalBody, ModalContent, ModalFooter, ModalHeader, Button } from "@heroui/react";

export default function GlobalPanel() {
  const {
    isVisible,
    title = "提示",
    message = "确认要执行该操作吗？",
    confirmButtonColor = "primary",
    onConfirm,
    onCancel,
    hidePanel,
  } = useGlobalPanel();

  const handleConfirm = () => {
    onConfirm?.();
    hidePanel();
  };

  const handleCancel = () => {
    onCancel?.();
    hidePanel();
  };

  return (
    <Modal isOpen={isVisible} onClose={hidePanel}>
      <ModalContent>
        <>
          <ModalHeader className="flex flex-col gap-1">{title}</ModalHeader>
          <ModalBody>
            <p className="text-sm text-gray-600 whitespace-pre-line">{message}</p>
          </ModalBody>
          <ModalFooter>
            <Button color="default" variant="light" onPress={handleCancel}>
              取消
            </Button>
            <Button color={confirmButtonColor} onPress={handleConfirm}>
              确认
            </Button>
          </ModalFooter>
        </>
      </ModalContent>
    </Modal>
  );
}
