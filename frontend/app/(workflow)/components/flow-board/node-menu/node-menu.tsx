// NodeMenu.jsx
import React from 'react';
import styles from './index.module.scss'; // 请根据实际路径导入样式
import NodeMenuItem from './node-menu-item'; // 导入 NodeMenuItem 组件

const NodeMenu = ({ nodeList, iconMapping }) => {
  return (
    <div className={styles.nodeList}>
      {nodeList.map((node) => {
        const iconInfo = iconMapping[node.icon];
        return (
          <div key={node.id} className={styles.container}>
            <div className={styles.nodeItemBox}>
              <NodeMenuItem node={node} iconInfo={iconInfo} />
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default NodeMenu;
