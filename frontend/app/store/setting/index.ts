import {create} from 'zustand';

// 定义 store 状态类型
interface SettingsState {
  language:string;
}

// 创建 zustand store
const useSettingsStore = create<SettingsState>((set) => ({
  language: 'zh/CN',
  setLanguage: (language) => set({ language }),
}));

export default useSettingsStore
