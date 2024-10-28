import {create} from 'zustand';

interface LoadingStore {
  loading: boolean;
  setLoading: (loading: boolean) => void; // 添加 setLoading 方法的类型定义
}


// 创建全局加载状态的 Store
const useLoadingStore = create<LoadingStore>((set) => ({
  loading: false,
  setLoading: (loading: boolean) => set({ loading }),
}));

export default useLoadingStore;
