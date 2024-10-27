"use client";

import React from 'react';
import {Spin} from 'antd'; // 假设你使用 antd 的 Spin 组件
import styles from './index.module.scss';
import useLoadingStore from "@/app/store/global-loading"; // 可选，样式文件

const GlobalLoader: React.FC = () => {
  const {loading} = useLoadingStore(); // 获取 loading 状态
  return (
    <>
      {loading && <div className={styles.globalLoader}>
        <Spin size="large"/>
      </div>}
    </>
  );
};

export default GlobalLoader;
