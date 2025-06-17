import {create} from "zustand";
import {ParameterRule, ProviderModelWithStatusEntity} from "@/app/api/model-provider/model";


interface ModelConfigState {
  params: ParameterRule[];  // 参数数组
  isPanelOpen: boolean;     // 控制面板显示
  providerModel: ProviderModelWithStatusEntity | null;

  setParams: (newParams: ParameterRule[]) => void; // 设置整个参数数组
  updateParamValue: (name: string, value: any) => void; // 根据 name 更新某个参数的 value

  setProviderModel: (provider: ProviderModelWithStatusEntity) => void;

  setPanelOpen: (open: boolean) => void;
  togglePanel: () => void;
}

export const useModelConfigStore = create<ModelConfigState>((set) => ({
  params: [],
  isPanelOpen: false,
  providerModel: null,
  setParams: (newParams) => set(() => ({params: newParams})),

  updateParamValue: (name, value) =>
    set((state) => ({
      params: state.params.map((p) =>
        p.name === name ? {...p, value} : p
      )
    })),

  setPanelOpen: (open) => set(() => ({isPanelOpen: open})),

  setProviderModel: (providerModel: ProviderModelWithStatusEntity) => set(() => ({providerModel})),

  togglePanel: () => set((state) => ({isPanelOpen: !state.isPanelOpen}))
}));
