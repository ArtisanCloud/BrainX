import { create } from "zustand";
import {CustomConfigurationStatusEnum, Provider} from "@/app/api/model-provider/provider";
import {Token} from "@/app/api/auth";
import {ProviderModel} from "@/app/api/model-provider/model";

// 定义 store 状态类型
interface SettingsState {
  providers: Record<string, Provider>;
  language: string;
  configuredProviders: Provider[];
  notConfiguredProviders: Provider[];
  configuredProviderModels: Record<string, ProviderModel[]> ;
  toRefresh: number;
  setConfiguredProviderModels: (providerId: string, models: ProviderModel[]) => void;
  setToRefresh: () => void;
  setLanguage: (language: string) => void;
  setProviders: (providers: Record<string, Provider>) => void;
}

// 创建 zustand store
const useSettingsStore = create<SettingsState>((set) => ({
  providers: {}, // 初始化为一个空对象
  configuredProviders: [],
  notConfiguredProviders: [] ,
  configuredProviderModels: {},
  setConfiguredProviderModels: (providerId, models) => {
    set((state) => ({
      configuredProviderModels: {
        ...state.configuredProviderModels,
        [providerId]: models
      }
    }));
  },
  toRefresh: 0,
  setToRefresh: () => {
    set(state => ({
      toRefresh: state.toRefresh + 1
    }))
  },
  language: "zh/CN",
  setLanguage: (language: string) => set({ language }),
  setProviders: (providers: Record<string, Provider>) => {
    const configured: Provider[] = []
    const notConfigured: Provider[] = []

    Object.values(providers).forEach(provider => {
      if (
        provider.custom_configuration?.status === CustomConfigurationStatusEnum.active ||
        (
          provider.system_configuration?.enabled === true &&
          provider.system_configuration.quota_configurations?.find((item:any) =>
            item.quota_type === provider.system_configuration.current_quota_type
          )
        )
      ) {
        configured.push(provider)
      } else {
        notConfigured.push(provider)
      }
    })

    set({
      providers,
      configuredProviders: configured,
      notConfiguredProviders: notConfigured
    })
  }
}));

export default useSettingsStore;
