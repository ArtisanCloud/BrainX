"use client";

import styles from './index.module.scss';
import {LeftOutlined} from '@ant-design/icons';
import React, { useEffect, useState} from "react";
import {ActionFetchNodeList, NodeTypeInfo} from "@/app/api/workflow/node";
import {iconMapping} from '@/app/(workflow)/components/icon'; // 导入图标映射对象
import '@xyflow/react/dist/style.css';
import FlowGround from "@/app/(workflow)/components/flow-board/flow-ground";
import {
  DndContext,
} from '@dnd-kit/core';
import Droppable from "@/app/components/drag-and-drop/droppable";
import Draggable from "@/app/components/drag-and-drop/draggable";
import NodeMenuItem from "@/app/(workflow)/components/flow-board/node-menu/node-menu-item";

const FlowBoard = () => {
  const [nodeMenuList, setNodeMenuList] = useState<NodeTypeInfo[]>([]);
  const [containerRefs, setContainerRefs] = useState<>({}); // 本地状态管理 refs

  useEffect(() => {
    const fetchNodeMenuList = async () => {
      try {
        const res = await ActionFetchNodeList();
        setNodeMenuList(res.data);

      } catch (error) {
        console.error("Error fetching node list:", error);
      }
    };
    fetchNodeMenuList();
  }, []);

  // 初始化 containerRefs
  useEffect(() => {
    const refs = {}; // 创建一个新的 refs 对象
    nodeMenuList.forEach(node => {
      refs[node.id] = React.createRef(); // 为每个节点创建一个 ref
    });
    setContainerRefs(refs); // 更新状态
  }, [nodeMenuList]);

  const handleDragEnd = (event) => {
    const {active, over} = event;
    console.log(active, over)
    // if (over) {
    //   // 将拖动的节点添加到 flowGroundNodes
    //   const newNode = {
    //     id: active.id,
    //     name: active.data.current.name,
    //     icon: active.data.current.icon,
    //   };
    // }
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

          <div
            className={styles.nodeMenuList}>
            {nodeMenuList.map((node, index) => {
              const iconInfo = iconMapping[node.icon];

              // 计算每个节点的 top 位置，假设每个 node 的高度是 100px
              const nodeTop = index * 64; // 动态设置 top，根据需要调整间距

              return (

                <div
                  key={node.id} className={styles.nodeContainer} ref={containerRefs[node.id]}
                  style={{top: `${nodeTop}px`}} // 动态设置 top
                >
                  {/*<Draggable id={node.id}*/}
                  {/*           nodeTop={nodeTop}*/}
                  {/*           style={{zIndex: `999`}} // 动态设置 top*/}
                  {/*           containerRef={containerRefs[node.id]?.current}*/}
                  {/*>*/}
                    <div className={styles.nodeItemBox}>
                      <NodeMenuItem node={node} iconInfo={iconInfo}/>
                    </div>
                  {/*</Draggable>*/}
                </div>
              );
            })}
          </div>

        </div>

        {/* 拖放的目标区域 */}
        {/*<Droppable>*/}
          <div className={styles.content}>
            <FlowGround/>
          </div>
        {/*</Droppable>*/}
      </div>
    </DndContext>
  );
};

export default FlowBoard;
