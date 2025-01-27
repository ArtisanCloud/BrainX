import { create } from "zustand";
import { Provider } from "@/app/api/model-provider/provider";

// 定义 store 状态类型
interface SettingsState {
  providers: Record<string, Provider>;
  language: string;
  setLanguage: (language: string) => void;
  setProviders: (providers: Record<string, Provider>) => void;
}

// 创建 zustand store
const useSettingsStore = create<SettingsState>((set) => ({
  providers: {}, // 初始化为一个空对象
  language: "zh/CN",
  setLanguage: (language: string) => set({ language }),
  setProviders: (providers: Record<string, Provider>) => set({ providers }),
}));

export default useSettingsStore;
