import { create } from "zustand";
import {CustomConfigurationStatusEnum, Provider} from "@/app/api/model-provider/provider";
import {ProviderModel} from "@/app/api/model-provider/model";
import {useState} from "react";

// 定义 store 状态类型
interface SettingsState {
  // 所有的模型列表
  providers: Record<string, Provider>;
  setProviders: (providers: Record<string, Provider>) => void;
  currentProvider: Provider|null;
  setCurrentProvider: (provider: Provider) => void;
  currentModel: ProviderModel|null;
  setCurrentModel: (model:ProviderModel) => void;
  // 配置好的模型列表
  configuredProviders: Provider[];
  notConfiguredProviders: Provider[];
  configuredProviderModels: Record<string, ProviderModel[]> ;
  setConfiguredProviderModels: (providerId: string, models: ProviderModel[]) => void;
  // 刷新模型列表
  toRefreshProviders: number;
  setToRefresh: () => void;
  // 语言
  language: string;
  setLanguage: (language: string) => void;
  // 展示保存模型弹窗
  isOpenSaveModelModal: boolean;
  setIsOpenSaveModelModal: (isOpen: boolean) => void;
  // 展示保存供应商配置弹窗
  isOpenSaveProviderModal: boolean;
  setIsOpenSaveProviderModal: (isOpen: boolean) => void;
  // 表单值
  formValues:Record<string, any>;
  setFormValues: (formValues: Record<string, any>) => void;

}

// 创建 zustand store
const useSettingsStore = create<SettingsState>((set) => ({
  // 所有的模型列表
  providers: {}, // 初始化为一个空对象
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
  },
  currentProvider: null,
  setCurrentProvider: (provider: Provider) => set({ currentProvider: provider }),
  currentModel: null,
  setCurrentModel: (model:ProviderModel) => set({ currentModel: model }),
  // 配置好的模型列表
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
  // 刷新模型列表
  toRefreshProviders: 0,
  setToRefresh: () => {
    set(state => ({
      toRefreshProviders: state.toRefreshProviders + 1
    }))
  },
  // 语言
  language: "zh/CN",
  setLanguage: (language: string) => set({ language }),
  // 展示保存模型弹窗
  isOpenSaveModelModal: false,
  setIsOpenSaveModelModal: (isOpen: boolean) =>{
    // console.log("setIsOpenSaveModelModal:",isOpen)
    set({ isOpenSaveModelModal: isOpen })
  },

  // 展示保存供应商配置弹窗
  isOpenSaveProviderModal: false,
  setIsOpenSaveProviderModal: (isOpen: boolean) => {
    // console.log("setIsOpenSaveProviderModal:",isOpen)
    set({ isOpenSaveProviderModal: isOpen });
  },
  // 表单值
  formValues: {},
  setFormValues: (formValues: Record<string, any>) => {set({ formValues })}
}));

export default useSettingsStore;
