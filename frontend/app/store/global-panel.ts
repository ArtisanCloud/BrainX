import { create } from 'zustand';

type GlobalPanelState = {
  isVisible: boolean;
  title?: string;
  message?: string;
  confirmButtonColor?: 'primary' | 'danger' | 'warning' | 'success' | 'default'; // 可扩展
  onConfirm?: () => void;
  onCancel?: () => void;
  showPanel: (options: Omit<GlobalPanelState, 'isVisible' | 'showPanel' | 'hidePanel'>) => void;
  hidePanel: () => void;
};

export const useGlobalPanel = create<GlobalPanelState>((set) => ({
  isVisible: false,
  title: '提示',
  message: '',
  confirmButtonColor: 'primary',
  onConfirm: undefined,
  onCancel: undefined,
  showPanel: (options) =>
    set({
      ...options,
      isVisible: true,
    }),
  hidePanel: () => set({ isVisible: false }),
}));
