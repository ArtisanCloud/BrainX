"use client";

import styles from './index.module.scss';
import {LeftOutlined, PlusOutlined} from '@ant-design/icons';
import {useEffect, useState} from "react";
import {ActionFetchNodeList, NodeTypeInfo} from "@/app/api/workflow/node";
import {iconMapping} from '@/app/(workflow)/components/icon'; // 导入图标映射对象
import '@xyflow/react/dist/style.css';
import FlowGround from "@/app/(workflow)/components/flow-board/flow-ground";
import {
  DndContext,
  useDroppable,
  useDraggable,
} from '@dnd-kit/core';
import NodeMenu from "@/app/(workflow)/components/flow-board/node-menu/node-menu";

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

  const handleDragEnd = (event) => {
    const {active, over} = event;

    if (over) {
      // 将拖动的节点添加到 flowGroundNodes
      const newNode = {
        id: active.id,
        name: active.data.current.name,
        icon: active.data.current.icon,
      };
      // setFlowGroundNodes((prev) => [...prev, newNode]);
    }
  };

  return (
    <DndContext onDragEnd={handleDragEnd}>

      <div className={styles.container}>
        {/* 侧边栏 */}
        <div className={styles.sidebar}>
          <div className={styles.labelBox}>
            <span className={styles.label}>选择节点</span>
            <div className={styles.buttonBox}>
              <button className={styles.hideSidebarButton}>
                <LeftOutlined style={{fontSize: '8px', color: "#6b6b75"}}/>
              </button>
            </div>
          </div>

          {/* 渲染节点列表 */}
          <NodeMenu nodeList={nodeList} iconMapping={iconMapping} />

        </div>

        {/* 拖放的目标区域 */}
        <div className={styles.content}>
          <FlowGround nodes={flowGroundNodes}/>
        </div>
      </div>
    </DndContext>
  );
};

export default FlowBoard;
