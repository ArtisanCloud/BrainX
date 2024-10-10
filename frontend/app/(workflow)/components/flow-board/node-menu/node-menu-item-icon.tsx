// node-menu-item-icon.tsx

import React from 'react';
import styles from './icon.module.scss';
import {IconInfo} from "@/app/(workflow)/components/icon"; // 请根据实际路径导入样式


// 定义组件的 Props 接口
interface NodeMenuItemIconProps {
  iconInfo?: IconInfo;
}

// 定义 NodeMenuItemIcon 组件
const NodeMenuItemIcon: React.FC<NodeMenuItemIconProps> = ({ iconInfo }) => {
  const {
    component: IconComponent,
    size = 24,
    backgroundColor = 'transparent'
  } = iconInfo || {};

  return (
    <div className={styles.imgBox}>
      {IconComponent ? (
        <IconComponent
          style={{
            width: `${size}px`,
            height: `${size}px`,
            backgroundColor: backgroundColor,
          }}
          className={styles.nodeItemIcon}
        />
      ) : (
        <div className={styles.nodeItemIcon}>
          <span>?</span>
        </div>
      )}
    </div>
  );
};

export default NodeMenuItemIcon;
