import {create} from 'zustand';

// 创建全局加载状态的 Store
const useLoadingStore = create((set) => ({
  loading: false,
  setLoading: (loading: boolean) => set({ loading }),
}));

export default useLoadingStore;
