// NodeMenuItem.jsx
import React from 'react';
import { PlusOutlined } from '@ant-design/icons'; // 确保正确导入图标
import styles from './item.module.scss'; // 请根据实际路径导入样式
import NodeMenuItemIcon from './node-menu-item-icon';
import {NodeTypeInfo} from "@/app/api/workflow/node";
import {IconInfo} from "@/app/(workflow)/components/icon"; // 导入 NodeIcon 组件

interface NodeMenuItemProps {
  node: NodeTypeInfo;
  iconInfo?: IconInfo;
}

const NodeMenuItem: React.FC<NodeMenuItemProps>  = ({ node, iconInfo }) => {
  return (
    <div className={styles.nodeItem}>
      <NodeMenuItemIcon iconInfo={iconInfo} />
      <span className={styles.nodeItemName}>{node.name}</span>
      <button className={styles.addButton}>
        <PlusOutlined style={{ fontSize: '16px', color: "#4d53e8" }} />
      </button>
    </div>
  );
};

export default NodeMenuItem;
