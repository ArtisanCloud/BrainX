"use client";

import styles from './index.module.scss';
import { LeftOutlined, PlusOutlined } from '@ant-design/icons';
import { useEffect, useState } from "react";
import { ActionFetchNodeList, NodeTypeInfo } from "@/app/api/workflow/node";
import { iconMapping } from '@/app/(workflow)/components/icon'; // 导入图标映射对象
import '@xyflow/react/dist/style.css';
import FlowGround from "@/app/(workflow)/components/flow-board/flow-ground";

// 导入 dnd-kit 的相关 API
import { DndContext, useDroppable } from '@dnd-kit/core';

const FlowBoard = () => {
  const [nodeList, setNodeList] = useState<NodeTypeInfo[]>([]);
  const [flowGroundNodes, setFlowGroundNodes] = useState<NodeTypeInfo[]>([]);

  useEffect(() => {
    const fetchNodeList = async () => {
      try {
        const res = await ActionFetchNodeList();
        setNodeList(res.data);
      } catch (error) {
        console.error("Error fetching node list:", error);
      }
    };
    fetchNodeList();
  }, []);

  const handleDrop = (event) => {
    const { active, over } = event;

    if (over) {
      // 将拖动的节点添加到 flowGroundNodes
      const newNode = {
        id: active.id,
        name: active.data.current.name,
        icon: active.data.current.icon,
      };
      setFlowGroundNodes((prev) => [...prev, newNode]);
    }
  };

  return (
    <DndContext onDragEnd={handleDrop}>
      <div className={styles.container}>
        {/* 侧边栏 */}
        <div className={styles.sidebar}>
          <div className={styles.labelBox}>
            <span className={styles.label}>选择节点</span>
            <div className={styles.buttonBox}>
              <button className={styles.hideSidebarButton}>
                <LeftOutlined style={{ fontSize: '8px', color: "#6b6b75" }} />
              </button>
            </div>
          </div>

          {/* 渲染节点列表 */}
          <div className={styles.nodeList}>
            {nodeList.map((node) => (
              <DraggableNode key={node.id} node={node} />
            ))}
          </div>
        </div>

        {/* 拖放的目标区域 */}
        <div className={styles.content}>
          <DroppableArea nodes={flowGroundNodes} />
        </div>
      </div>
    </DndContext>
  );
};

// 创建可拖拽节点组件
const DraggableNode = ({ node }) => {
  const iconInfo = iconMapping[node.icon];
  const {
    component: IconComponent,
    size = 24,
    backgroundColor = 'transparent'
  } = iconInfo || {};

  // 使用 useDraggable 创建可拖动的节点
  const { attributes, listeners, setNodeRef } = useDraggable({
    id: node.id,
    data: { name: node.name, icon: node.icon }
  });

  return (
    <div ref={setNodeRef} {...listeners} {...attributes} className={styles.nodeContainer}>
      <div className={styles.nodeBox}>
        <div className={styles.nodeItem}>
          <div className={styles.imgBox}>
            {IconComponent ? (
              <IconComponent
                style={{
                  width: `${size}px`,
                  height: `${size}px`,
                  backgroundColor: backgroundColor,
                }}
                className={styles.nodeIcon}
              />
            ) : (
              <div className={styles.nodeIcon}>
                <span>?</span>
              </div>
            )}
          </div>
          <span className={styles.nodeName}>{node.name}</span>
          <button className={styles.addButton}>
            <PlusOutlined style={{ fontSize: '16px', color: "#4d53e8" }} />
          </button>
        </div>
      </div>
    </div>
  );
};

// 创建 DroppableArea 组件
const DroppableArea = ({ nodes }) => {
  const { setNodeRef } = useDroppable({ id: 'droppable' });

  return (
    <div ref={setNodeRef} className={styles.droppableArea}>
      {/* 渲染放置的节点 */}
      {nodes.map((node) => (
        <div key={node.id} className={styles.droppedNode}>
          {node.name} {/* 你可以根据需要添加图标 */}
        </div>
      ))}
    </div>
  );
};

export default FlowBoard;
