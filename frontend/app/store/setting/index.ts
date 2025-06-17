import {create} from "zustand";
import {CustomConfigurationStatusEnum, Provider} from "@/app/api/model-provider/provider";
import {
  DefaultModelResponse, fetchDefaultModels,
  fetchModelsByType,
  ProviderModel,
  ProviderWithModels
} from "@/app/api/model-provider/model";
import {useState} from "react";
import {ModelTypeEnum} from "@/app/api/model-provider";

// 定义 store 状态类型
interface SettingsState {
  // 所有的模型列表
  providers: Record<string, Provider>;
  setProviders: (providers: Record<string, Provider>) => void;
  currentProvider: Provider | null;
  setCurrentProvider: (provider: Provider) => void;
  currentModel: ProviderModel | null;
  setCurrentModel: (model: ProviderModel) => void;
  // 配置好的模型列表
  configuredProviders: Provider[];
  notConfiguredProviders: Provider[];
  configuredProviderModels: Record<string, ProviderModel[]>;
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
  formValues: Record<string, any>;
  setFormValues: (formValues: Record<string, any>) => void;
  // 系统模型选择设置
  workspaceModels: Record<ModelTypeEnum, ProviderWithModels[]>,
  setWorkspaceModels: (updater: (prev: Record<ModelTypeEnum, ProviderWithModels[]>) => Record<ModelTypeEnum, ProviderWithModels[]>) => void,
  fetchWorkspaceModels: () => void;
  workspaceDefaultModels: Record<ModelTypeEnum, DefaultModelResponse>,
  setWorkspaceDefaultModels: (
    updater: (prev: Record<ModelTypeEnum, DefaultModelResponse>) => Record<ModelTypeEnum, DefaultModelResponse>
  ) => void;
  fetchAllDefaultModels: () => void;
}

// 创建 zustand store
const useSettingsStore = create<SettingsState>((set, get) => ({
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
          provider.system_configuration.quota_configurations?.find((item: any) =>
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
  setCurrentProvider: (provider: Provider) => set({currentProvider: provider}),
  currentModel: null,
  setCurrentModel: (model: ProviderModel) => set({currentModel: model}),
  // 配置好的模型列表
  configuredProviders: [],
  notConfiguredProviders: [],
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
  // 系统模型选择设置
  workspaceModels: {} as Record<ModelTypeEnum, ProviderWithModels[]>,
  setWorkspaceModels: (updater: (prev: Record<ModelTypeEnum, ProviderWithModels[]>) => Record<ModelTypeEnum, ProviderWithModels[]>) => {
    set(state => ({
      workspaceModels: updater(state.workspaceModels)
    }));
  },
  workspaceDefaultModels: {} as Record<ModelTypeEnum, DefaultModelResponse>,
  setWorkspaceDefaultModels: (updater: (prev: Record<ModelTypeEnum, DefaultModelResponse>) => Record<ModelTypeEnum, DefaultModelResponse>) => {
    set(state => ({
      workspaceDefaultModels: updater(state.workspaceDefaultModels)
    }));
  },

  fetchWorkspaceModels: async () => {
    const currentWorkspaceModels = get().workspaceModels; // 👈 Get current state

    // Check if the data is already populated.
    // Assuming if the object has any keys, it's considered populated.
    if (Object.keys(currentWorkspaceModels).length > 0) {
      console.log("Workspace models already fetched, returning existing data.");
      return; // Data already exists, so exit
    }

    try {
      const types = Object.values(ModelTypeEnum);
      const results = await Promise.all(
        types.map(modelType =>
          fetchModelsByType(modelType).then(res => ({modelType, data: res.data}))
        )
      );

      const modelsMap: Partial<Record<ModelTypeEnum, ProviderWithModels[]>> = {};
      results.forEach(({modelType, data}) => {
        if (data) modelsMap[modelType] = data;
      });

      set(state => ({
        workspaceModels: {
          ...state.workspaceModels,
          ...modelsMap
        }
      }));

    } catch (e) {
      console.log(e)
    }
  },

  fetchAllDefaultModels: async () => {
    const currentWorkspaceDefaultModels = get().workspaceDefaultModels; // 👈 Get current state

    // Check if the data is already populated.
    // Assuming if the object has any keys, it's considered populated.
    if (Object.keys(currentWorkspaceDefaultModels).length > 0) {
      console.log("Default models already fetched, returning existing data.");
      return; // Data already exists, so exit
    }

    try {
      const types = Object.values(ModelTypeEnum);
      const results = await Promise.all(
        types.map(modelType =>
          fetchDefaultModels(modelType).then(res => ({modelType, data: res.data}))
        )
      );

      const modelsMap: Partial<Record<ModelTypeEnum, DefaultModelResponse>> = {};
      results.forEach(({modelType, data}) => {
        if (data) modelsMap[modelType] = data;
      });

      set(state => ({ // 使用 state 参数来访问当前状态
        workspaceDefaultModels: {
          ...state.workspaceDefaultModels, // 展开当前状态的 workspaceDefaultModels
          ...modelsMap // 合并新的数据
        }
      }));

    } catch (e) {
      console.log(e)
    }
  },


  // 语言
  language: "zh/CN",
  setLanguage: (language: string) => set({language}),
  // 展示保存模型弹窗
  isOpenSaveModelModal: false,
  setIsOpenSaveModelModal: (isOpen: boolean) => {
    // console.log("setIsOpenSaveModelModal:",isOpen)
    set({isOpenSaveModelModal: isOpen})
  },

  // 展示保存供应商配置弹窗
  isOpenSaveProviderModal: false,
  setIsOpenSaveProviderModal: (isOpen: boolean) => {
    // console.log("setIsOpenSaveProviderModal:",isOpen)
    set({isOpenSaveProviderModal: isOpen});
  },
  // 表单值
  formValues: {},
  setFormValues: (formValues: Record<string, any>) => {
    set({formValues})
    // console.log(formValues);
  }
}));

export default useSettingsStore;
